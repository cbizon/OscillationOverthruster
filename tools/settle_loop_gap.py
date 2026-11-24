"""Gap between the way up and the way down for a settle-then-step loop (E0090),
compared with the fixed-rate loops in evidence/E0069-results.json.

usage: settle_loop_gap.py LOOPDIR EXPERIMENT_ID OUT_JSON

Per step (one step directory each, frames at 32 per cycle, frame 0 dropped):
  A_step   corrected band amplitude over all the step's frames (the registered
           measure, same formula as settle_ramp.corrected_amplitude)
  A_last100  same over the last 100 cycles only (the window the stopping rule
           judged settled)
  A_by_25_cycles  same over consecutive 25-cycle blocks (the step's time course)
  drift    A over the last quarter minus A over the first quarter (as E0069)
  thickness  mean layer thickness over the step and over the last 100 cycles
Gap: way down minus way up at the same Gamma.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

BAND_LO = 3
FPC = 32

loop = Path(sys.argv[1])
exp_id = sys.argv[2]
out_path = Path(sys.argv[3])
SEQ = Path(__file__).resolve().parent.parent


def amp(spec):
    band = spec[:, BAND_LO - 1:]
    P = band.mean(axis=0)
    return float(np.sqrt(max(P.sum() - len(P) * np.median(P), 0.0)))


ramp = [json.loads(l) for l in (loop / "ramp.jsonl").read_text().splitlines() if l.strip()]
steps_root = loop / "loop" if (loop / "loop").is_dir() else loop
rows = []
files = []
for r in ramp:
    k, g = r["step"], r["gamma"]
    d = next(steps_root.glob("step-%03d-g*" % k))
    fz = d / "fields.npz"
    qz = d / "quantities.npz"
    for f in (fz, qz):
        files.append(dict(path=str(f.relative_to(loop)), bytes=f.stat().st_size,
                          sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
    spec = np.load(fz)["spec"].astype(float)
    th = np.load(qz)["thickness"].astype(float)
    n = r["cycles"]
    spec = spec[1:1 + n * FPC]
    th = th[1:1 + n * FPC]
    assert len(spec) == n * FPC, (k, len(spec), n)
    q = len(spec) // 4
    rows.append(dict(
        step=k, gamma=g, branch=None, cycles=n, settled=r["settled"],
        A_step=round(amp(spec), 4),
        A_last100=round(amp(spec[-100 * FPC:]), 4),
        drift=round(amp(spec[-q:]) - amp(spec[:q]), 4),
        thickness_step=round(float(th.mean()), 4),
        thickness_last100=round(float(th[-100 * FPC:].mean()), 4),
        cpu_hours=round(r["cpu_seconds"] / 3600, 3),
        A_by_25_cycles=[round(amp(spec[c * FPC:(c + 25) * FPC]), 3)
                        for c in range(0, n - 24, 25)]))

top = int(np.argmax([r["gamma"] for r in rows]))
for r in rows:
    r["branch"] = "up" if r["step"] <= top else "down"

fixed = json.loads((SEQ / "evidence" / "E0069-results.json").read_text())
fixed_by_g = {round(t["gamma"], 2): t for t in fixed["table"]}

table = []
for g in sorted({r["gamma"] for r in rows}):
    up = [r for r in rows if r["gamma"] == g and r["branch"] == "up"]
    dn = [r for r in rows if r["gamma"] == g and r["branch"] == "down"]
    if not up or not dn:
        continue
    up, dn = up[0], dn[0]
    entry = dict(gamma=g,
                 settled={"up_A": up["A_step"], "down_A": dn["A_step"],
                          "gap": round(dn["A_step"] - up["A_step"], 4),
                          "up_cycles": up["cycles"], "down_cycles": dn["cycles"],
                          "up_drift": up["drift"], "down_drift": dn["drift"]},
                 settled_last100={"up_A": up["A_last100"], "down_A": dn["A_last100"],
                                  "gap": round(dn["A_last100"] - up["A_last100"], 4)},
                 thickness_gap_last100=round(dn["thickness_last100"] - up["thickness_last100"], 4))
    ft = fixed_by_g.get(round(g, 2), {})
    for rate in ("25", "100", "400"):
        if rate in ft:
            entry["gap_%s" % rate] = ft[rate]["gap"]
    table.append(entry)


def summ(key):
    gaps = [t[key]["gap"] for t in table]
    i = int(np.argmax(gaps))
    return dict(largest_gap=gaps[i], at_gamma=table[i]["gamma"],
                gamma_where_gap_over_0p05=[t["gamma"] for t in table if t[key]["gap"] > 0.05])


res = dict(
    experiment=exp_id,
    interim=False,
    what=("Settle-then-step loop at f* 0.44 (Gamma 1.9 to 2.6 and back, stopping rule D0056): "
          "cycles each step took, and the gap (way down minus way up) in the corrected band "
          "amplitude A, over the whole step (registered measure) and over the last 100 cycles "
          "(the window judged settled). Compared with the 25, 100 and 400 cycles-per-step gaps "
          "from evidence/E0069-results.json. Script tools/settle_loop_gap.py."),
    steps=rows,
    table=table,
    summary=dict(
        steps=len(rows), settled=sum(r["settled"] for r in rows),
        cycles_total=sum(r["cycles"] for r in rows),
        cycles_by_step=[r["cycles"] for r in rows],
        steps_by_cycles={str(c): sum(r["cycles"] == c for r in rows)
                         for c in sorted({r["cycles"] for r in rows})},
        max_cycles=max(r["cycles"] for r in rows),
        cpu_hours_steps=round(sum(r["cpu_hours"] for r in rows), 2),
        slow_episodes=sum(r["slow_episodes"] for r in ramp),
        audit_failures=sum(r["audit_failures"] for r in ramp),
        worst_energy_residual=max(r["worst_energy_residual"] for r in ramp),
        whole_step=summ("settled"),
        last100=summ("settled_last100"),
        fixed_rate_largest_gap={k: v["largest_gap"] for k, v in fixed["summary_by_cycles_per_step"].items()},
    ),
    files=files,
)
out_path.write_text(json.dumps(res, indent=1) + "\n")
print(json.dumps(res["summary"], indent=1))
for t in table:
    print(t["gamma"], t["settled"]["up_cycles"], t["settled"]["down_cycles"],
          t["settled"]["up_A"], t["settled"]["down_A"], "gap", t["settled"]["gap"],
          "last100", t["settled_last100"]["gap"],
          "| 25/100/400:", t.get("gap_25"), t.get("gap_100"), t.get("gap_400"))
