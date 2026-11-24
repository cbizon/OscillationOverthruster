"""E0100/E0101: bulk judge of grapenuts (E0099, E0101) against sequel's unmodified engine.

For each finished E0100 baseline job (referee/long_contact.py, 1020 cycles),
fetch its quantities.npz, build the 10-block baseline (bulk.py baseline
--from-cycle 20 --cycles 100 --blocks 10), then fetch every finished E0099
run at the same condition (the tc run and the hard control), measure it
(bulk.py measure --from-cycle 20 --cycles 100) and judge it (bulk.py judge).
Writes evidence/E0100-results.json.  Fetched files are scratch
(tmp/fetch, emptied by the run).

    uv run python tools/grapenuts_judge.py
"""

import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
DATA = Path("~/Projects/experiments/sequel-data").expanduser()
PROGRAM = ["uv", "run", "--project", str(Path("~/Projects/experiments/research-programs").expanduser()),
           "program"]


def jobs(experiment):
    out = []
    for f in sorted((HERE / "evidence" / experiment).glob("hatteras-*.json")):
        rec = json.loads(f.read_text())
        if rec.get("state") != "COMPLETED" or not rec.get("artifact_id"):
            continue
        cmd = rec["command"][2]
        arg = lambda name: re.search(rf"--{name} (\S+)", cmd).group(1)
        mode = re.search(r"--mode (\S+)", cmd)
        k = re.search(r"--stiffness (\S+)", cmd)
        out.append(dict(job=f.stem, artifact=rec["artifact_id"],
                        cond=(float(arg("gamma")), float(arg("fstar")), float(arg("depth"))),
                        mode=(mode.group(1) + (" k=" + k.group(1) if k else "")) if mode else "sequel-main",
                        experiment=experiment))
    return out


def fetch(artifact):
    subprocess.run(PROGRAM + ["fetch", f"{artifact}:out/run/quantities.npz"],
                   cwd=HERE, check=True, capture_output=True)
    return DATA / "tmp" / "fetch" / artifact / "out" / "run" / "quantities.npz"


def load_bulk():
    import importlib.util
    spec = importlib.util.spec_from_file_location("bulk", HERE / "referee" / "bulk.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    bulk = load_bulk()
    methods = jobs("E0099") + jobs("E0101")
    rows = []
    unavailable = []
    for base in jobs("E0100"):
        summary = json.loads((DATA / "mirror" / "E0100" / base["job"] / "out" / "run"
                              / "summary.json").read_text())
        if summary["outcome"] != "completed":
            unavailable.append(dict(job=base["job"], artifact=base["artifact"],
                                    condition=base["cond"], outcome=summary["outcome"],
                                    error=summary.get("error"),
                                    cycles_completed=summary["cycles_completed"]))
            print(base["cond"], "baseline unavailable:", summary["outcome"], flush=True)
            continue
        b = bulk.baseline(fetch(base["artifact"]), 20, 100, 10, 2)
        for m in (m for m in methods if m["cond"] == base["cond"]):
            meas = bulk.measure(fetch(m["artifact"]), 20, 100, 2)
            verdict = bulk.judge(b, meas)
            rows.append(dict(
                condition=dict(zip(("gamma", "f_star", "depth"), base["cond"])),
                baseline_job=base["job"], baseline_artifact=base["artifact"],
                method_experiment=m["experiment"], method_job=m["job"], method_artifact=m["artifact"], method_mode=m["mode"],
                threshold_sd=b["threshold"], baseline_blocks=b["blocks"],
                passes=all(r["passes"] for r in verdict.values()),
                worst_sigmas=max(abs(r["sigmas"]) for r in verdict.values()),
                quantities=verdict,
                drifting=[k for k, v in meas["quantities"].items()
                          if isinstance(v, dict) and v.get("drifting")]))
            print(base["cond"], m["mode"], "pass" if rows[-1]["passes"] else "FAIL",
                  "worst %.2f sd" % rows[-1]["worst_sigmas"],
                  {k: round(v["sigmas"], 2) for k, v in verdict.items()}, flush=True)
    out = dict(experiment_id="E0100", tool="tools/grapenuts_judge.py",
               rule="referee/bulk.py judge: 100-cycle mean (cycles 20-120) within the "
                    "threshold of block sd of a 10-block baseline (cycles 20-1020)",
               baselines_unavailable=unavailable, comparisons=rows)
    (HERE / "evidence" / "E0100-results.json").write_text(
        json.dumps(out, indent=1, default=float) + "\n")


if __name__ == "__main__":
    main()
