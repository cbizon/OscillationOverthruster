"""Collect E0099 (grapenuts survival and energy pilot) from the Hatteras mirror.

Reads every mirror/E0099/hatteras-*/out/run/{summary,audit}.json and the job
records evidence/E0099/hatteras-*.json (artifact ids), and writes
evidence/E0099-results.json.

    python3 tools/grapenuts_collect.py
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
MIRROR = Path("~/Projects/experiments/sequel-data/mirror/E0099").expanduser()


def run_row(job_dir: Path) -> dict | None:
    run = job_dir / "out" / "run"
    if not (run / "summary.json").exists():
        return None
    s = json.loads((run / "summary.json").read_text())
    audit = json.loads((run / "audit.json").read_text())
    job = job_dir.name.split("-", 1)[1]
    record = HERE / "evidence" / "E0099" / f"hatteras-{job}.json"
    rec = json.loads(record.read_text()) if record.exists() else {}
    soft = sum(r["soft_dissipation"] for r in audit)
    gain = sum(r["friction_gain"] for r in audit)
    residuals = [r["energy_residual_rel"] for r in audit]
    cycles = s["cycles_completed"]
    return {
        "job": f"hatteras-{job}", "job_state": rec.get("state", "RUNNING"),
        "artifact": rec.get("artifact_id") or rec.get("artifact"),
        "mode": s["contact"]["contact_mode"], "stiffness": s["contact"].get("stiffness"),
        "dim": s["dim"], "gamma": s["gamma"], "f_star": s["f_star"], "depth": s["depth"],
        "N": s["particle_count"], "L": s["width"], "seed": s["seed"],
        "outcome": s["outcome"], "cycles_completed": cycles,
        "slow_episodes": len(s["slow_episodes"]),
        "energy_gains": s["energy_gains"],
        "worst_residual_with_springs": s["worst_energy_residual"],
        "mean_residual_with_springs": sum(residuals) / len(residuals) if residuals else None,
        "largest_positive_residual": max([x for x in residuals if x > 0], default=0.0),
        "positive_residual_cycles": s["positive_residual_cycles"],
        "worst_referee_residual": s["worst_referee_residual"],
        "worst_momentum_residual": s["worst_momentum_residual"],
        "audit_failures_at_1e-8": len(s["audit_failures"]),
        "soft_dissipation_total": soft,
        "friction_gain_total": gain,
        "plate_work_total": sum(r["plate_work"] for r in audit),
        "springs_made": s["soft"]["springs_made"],
        "springs_made_cycle1": audit[0]["springs_made"] if audit else None,
        "max_pair_overlap": s["soft"]["max_pair_overlap"],
        "max_plate_overlap": s["soft"]["max_plate_overlap"],
        "max_spring_speed": s["soft"]["max_spring_speed"],
        "hard_collisions_per_particle_cycle": (
            sum(2 * r["hard_pair"] + r["hard_plate"] for r in audit) / s["particle_count"] / cycles
            if cycles else None),
        "cpu_seconds": s["cpu_seconds"],
        "cpu_seconds_per_cycle": s["cpu_seconds"] / cycles if cycles else None,
        "engine": s["engine"],
    }


def main():
    rows = [r for d in sorted(MIRROR.glob("hatteras-*")) if (r := run_row(d))]
    out = {
        "experiment_id": "E0099",
        "source": "mirror/E0099 (program jobs), summary.json and audit.json per run; "
                  "tools/grapenuts_collect.py",
        "notes": [
            "energy_residual_rel counts the springs' booked dissipation (EN_SOFT_DISS) and "
            "nudge energy; referee residual is the referee's sum, which leaves them out.",
            "Rows with job_state RUNNING are interim: the run's latest checkpoint summary.",
            "Hard (mode never) residuals are round-off (1e-12), so their positive-cycle "
            "counts are noise.",
        ],
        "runs": rows,
    }
    path = HERE / "evidence" / "E0099-results.json"
    path.write_text(json.dumps(out, indent=1) + "\n")
    for r in rows:
        print(r["job"], r["job_state"], r["mode"], r["dim"], r["gamma"], r["f_star"],
              r["depth"], r["outcome"], r["cycles_completed"],
              "%.1e %.1e %.1e" % (r["worst_residual_with_springs"],
                                  r["largest_positive_residual"],
                                  r["worst_referee_residual"]),
              "gain/soft %.3f" % (r["friction_gain_total"] / r["soft_dissipation_total"]
                                   if r["soft_dissipation_total"] else 0),
              "%.1f s/cyc" % r["cpu_seconds_per_cycle"])


if __name__ == "__main__":
    main()
