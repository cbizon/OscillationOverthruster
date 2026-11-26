"""Collect ended width-200 loops (E0074, E0075) from mirrored step summaries.

Usage: python tools/collect_width200_loops.py OUT.json E0075:164675 E0074:164665 ...
Reads sequel-data/mirror/<exp>/hatteras-<job>/out/step-*/summary.json and the job
records in evidence/<exp>/; compares with evidence/E0065-results.json (nudge) or
evidence/E0060-results.json (no friction) at width 100.
"""
import json, hashlib, re, sys, statistics
from pathlib import Path

M = Path.home() / "Projects/experiments/sequel-data/mirror"
EV = Path(__file__).resolve().parent.parent / "evidence"
OUT = sys.argv[1]
jobs = [(e, int(j)) for e, j in (a.split(":") for a in sys.argv[2:])]

e65 = {l["f_star"]: l for l in json.load(open(EV / "E0065-results.json"))["loops"]}
e60 = {l["f_star"]: l for l in json.load(open(EV / "E0060-results.json"))["loops"]}

out = []
for exp, job in jobs:
    rec = json.load(open(EV / exp / f"hatteras-{job}.json"))
    cmd = rec["command"][-1]
    fstar = re.search(r"--fstar (\S+)", cmd).group(1)
    gammas = [float(g) for g in re.search(r"--gammas (\S+)", cmd).group(1).split(",")]
    top_i = gammas.index(7.0)
    low_i = gammas.index(1.7)
    d = M / exp / f"hatteras-{job}" / "out"
    steps = []
    for sd in sorted(p for p in d.iterdir() if p.is_dir() and p.name.startswith("step-")):
        i = int(sd.name.split("-")[1])
        f = sd / "summary.json"
        s = json.load(open(f))
        if exp == "E0075":
            leg = "down" if i <= low_i else ("up" if i <= top_i else "down2")
        else:
            leg = "up" if i <= top_i else "down"
        steps.append(dict(step=i, gamma=s["gamma"], leg=leg, outcome=s["outcome"],
                          error=s.get("error"), cycles=s["cycles_completed"],
                          requested=s["cycles_requested"], cap_cpu_h=s["max_cpu_hours"],
                          cpu_h=round(s["cpu_seconds"] / 3600, 3),
                          cpu_s_per_cycle=round(s["cpu_seconds"] / max(s["cycles_completed"], 1), 1),
                          energy_gains=s["energy_gains"], audit_failures=len(s["audit_failures"]),
                          slow=len(s["slow_episodes"]),
                          sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
    stops = [s for s in steps if s["outcome"] != "completed"]
    comp = [s for s in steps if s["outcome"] == "completed"]
    L = dict(experiment=exp, job=job, artifact=None, fstar=fstar,
             slurm_state=rec.get("state"), elapsed=rec.get("elapsed"),
             job_cpu_hours=rec.get("cpu_hours"), steps_present=len(steps),
             steps_completed=len(comp), steps_planned=len(gammas),
             stops=[{k: s[k] for k in ("step", "gamma", "leg", "outcome", "cycles", "requested", "cap_cpu_h", "cpu_h")} for s in stops],
             energy_gains_any_step=sum(s["energy_gains"] for s in steps),
             audit_failures_any_step=sum(s["audit_failures"] for s in steps),
             slow_episodes_any_step=sum(s["slow"] for s in steps),
             cpu_h_sum_of_steps=round(sum(s["cpu_h"] for s in steps), 2))
    if exp == "E0075":
        down = [s for s in steps if s["leg"] == "down"]
        up = [s for s in steps if s["leg"] == "up"]
        dstop = next((s for s in down if s["outcome"] != "completed"), None)
        ustop = next((s for s in up if s["outcome"] != "completed"), None)
        dc = [s for s in down if s["outcome"] == "completed"]
        uc = [s for s in up if s["outcome"] == "completed"]
        L["down_floor"] = dc[-1]["gamma"] if dc else None
        L["down_stop"] = dstop and {k: dstop[k] for k in ("gamma", "outcome", "cycles", "requested", "cpu_h")}
        L["up_ceiling"] = uc[-1]["gamma"] if uc else None
        L["up_stop"] = ustop and {k: ustop[k] for k in ("gamma", "outcome", "cycles", "requested", "cpu_h")}
        w = e65.get(float(fstar))
        if w:
            L["width100_same_model"] = dict(source=f"evidence/E0065-results.json loop {w['name']} (N 60000, L 100, caps 0.5 CPU-h a step)",
                                            steps_completed=w["steps_completed"], floor=w["floor_gamma"],
                                            top=w["gamma_reached"] if w["steps_completed"] else None,
                                            stops=w["steps_not_completed"])
            ref = {}
            for s in w["steps"]:
                if s["outcome"] == "completed" and s["cycles"] == 25:
                    ref.setdefault((s["direction"], s["gamma"]), s["cpu_seconds"])
            ratios = {"down": [], "up": []}
            for s in comp:
                if s["requested"] != 25 or s["leg"] not in ratios:
                    continue
                r = ref.get((s["leg"], s["gamma"]))
                if r:
                    ratios[s["leg"]].append([s["gamma"], round(s["cpu_h"] * 3600 / r, 2)])
            L["cost_ratio_width200_over_width100"] = {k: dict(n=len(v), median=round(statistics.median([x[1] for x in v]), 2) if v else None, pairs=v) for k, v in ratios.items()}
    else:
        w = e60.get(float(fstar))
        L["all_steps_completed"] = len(comp) == len(gammas)
        if w:
            L["width100_same_model"] = dict(source=f"evidence/E0060-results.json loop {w['name']} (N 60000, L 100)",
                                            state=w["state"], steps_completed=w["steps_completed"], cpu_hours=w["cpu_hours"])
            ref = {}
            for s in w["steps"]:
                if s["outcome"] == "completed":
                    ref.setdefault((s["direction"], s["gamma"]), s["cpu_seconds"])
            ratios = {"down": [], "up": []}
            for s in comp:
                r = ref.get((s["leg"], s["gamma"]))
                if r:
                    ratios[s["leg"]].append([s["gamma"], round(s["cpu_h"] * 3600 / r, 2)])
            L["cost_ratio_width200_over_width100"] = {k: dict(n=len(v), median=round(statistics.median([x[1] for x in v]), 2) if v else None, min=min(x[1] for x in v) if v else None, max=max(x[1] for x in v) if v else None) for k, v in ratios.items()}
        cs = sorted(comp, key=lambda s: -s["cpu_h"])[:3]
        L["costliest_steps"] = [{k: s[k] for k in ("step", "gamma", "leg", "cpu_h", "cpu_s_per_cycle")} for s in cs]
    L["steps"] = steps
    out.append(L)

json.dump(out, open(OUT, "w"), indent=1)
for L in out:
    print(json.dumps({k: v for k, v in L.items() if k not in ("steps",) and not (k == "cost_ratio_width200_over_width100" and L["experiment"] == "E0075")}, default=str)[:1800])
    if "cost_ratio_width200_over_width100" in L and L["experiment"] == "E0075":
        print("  ratios", {k: (v["n"], v["median"]) for k, v in L["cost_ratio_width200_over_width100"].items()})
    print()
