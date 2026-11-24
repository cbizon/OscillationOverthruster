"""Per-step cost table for an E0089 nudge loop, from step-to-step counter differences.

The engine's checkpoints carry the event counters, and tools/ramp.py starts each
step from a copy of the previous step's checkpoint, so counters.json (and the
referee's events_per_particle_cycle in summary.json) are running totals for the
whole loop. This script takes the difference between each step's counters.json
and the previous step's, and divides by that step's completed cycles.

Usage: python tools/e0089_step_table.py <mirror job dir> <f_star> <out.json> [--from 4.3]
       [--ball evidence/E0089-interim-f0.57.json]  (ball-model columns, keyed by Gamma)
"""
import argparse
import hashlib
import json
import os
import re

N = 60000


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job_dir")
    ap.add_argument("f_star", type=float)
    ap.add_argument("out")
    ap.add_argument("--from", dest="g_from", type=float, default=4.3)
    ap.add_argument("--ball", default=None)
    a = ap.parse_args()

    loop = os.path.join(a.job_dir, "out", "loop")
    steps = sorted(d for d in os.listdir(loop) if re.match(r"step-\d{3}-g[\d.]+$", d))
    ball = {}
    if a.ball:
        for r in json.load(open(a.ball))["rows"]:
            ball[r["gamma"]] = {k: r[k] for k in r if k.startswith("ball_model")}

    rows, files = [], []
    prev = None
    for i, s in enumerate(steps):
        sp = os.path.join(loop, s, "summary.json")
        cp = os.path.join(loop, s, "counters.json")
        if not (os.path.exists(sp) and os.path.exists(cp)):
            prev = None
            continue
        summ, cnt = json.load(open(sp)), json.load(open(cp))
        # Up-branch only: the loop goes down to 1.7 and back up; keep the last visit.
        if prev is not None and summ["gamma"] >= a.g_from and summ["gamma"] > prev[0]["gamma"]:
            if int(s[5:8]) != int(prev[2][5:8]) + 1:
                raise SystemExit(f"non-consecutive steps {prev[2]} -> {s}")
            c, c0 = cnt["counters"], prev[1]["counters"]
            d = {k: c[k] - c0[k] for k in c}
            if d["C_EVENTS"] <= 0:
                raise SystemExit(f"counters did not increase at {s}")
            cyc = summ["cycles_completed"]
            cpu = summ["cpu_seconds"]
            host = "hatteras" if summ["engine"]["path"].startswith("/projects/") else "local Mac (E0065)"
            row = {
                "step": s,
                "previous_step": prev[2],
                "gamma": summ["gamma"],
                "outcome": summ["outcome"],
                "cycles": cyc,
                "host": host,
                "cpu_seconds": round(cpu, 1),
                "cpu_seconds_per_cycle": round(cpu / cyc, 1),
                "collisions_per_particle_cycle": round((d["C_PP"] + d["C_WALL"] + d["C_PLATE"]) / N / cyc, 1),
                "events_per_particle_cycle": round(d["C_EVENTS"] / N / cyc, 1),
                "plate_collisions_per_particle_cycle": round(d["C_PLATE"] / N / cyc, 1),
                "pp_collisions_per_particle_cycle": round(d["C_PP"] / N / cyc, 1),
                "cpu_microseconds_per_event": round(cpu / d["C_EVENTS"] * 1e6, 3),
                "pair_checks_per_event": round(d["C_PAIRS"] / d["C_EVENTS"], 2),
                "root_calls_per_event": round(d["C_ROOTCALL"] / d["C_EVENTS"], 3),
                "referee_events_per_particle_cycle_running_total": round(summ["events_per_particle_cycle"], 1),
                "worst_energy_residual": summ["worst_energy_residual"],
                "audit_failures": len(summ["audit_failures"]),
                "energy_gains": summ["energy_gains"],
                "slow_episodes": len(summ["slow_episodes"]),
            }
            row.update(ball.get(summ["gamma"], {}))
            rows.append(row)
            for p in (sp, cp, os.path.join(loop, prev[2], "counters.json")):
                files.append({"path": os.path.abspath(p), "bytes": os.path.getsize(p), "sha256": sha(p)})
        prev = (summ, cnt, s)

    # ratios between consecutive up-branch steps
    for r0, r1 in zip(rows, rows[1:]):
        r1["ratio_vs_previous_step"] = {
            "events_per_cycle": round(r1["events_per_particle_cycle"] / r0["events_per_particle_cycle"], 2),
            "plate_collisions_per_cycle": round(r1["plate_collisions_per_particle_cycle"] / r0["plate_collisions_per_particle_cycle"], 2),
            "cpu_per_cycle": round(r1["cpu_seconds_per_cycle"] / r0["cpu_seconds_per_cycle"], 2),
            "cpu_per_event": round(r1["cpu_microseconds_per_event"] / r0["cpu_microseconds_per_event"], 2),
            "same_machine": r0["host"] == r1["host"],
        }
    seen, uniq = set(), []
    for f in files:
        if f["path"] not in seen:
            seen.add(f["path"])
            uniq.append(f)
    out = {"f_star": a.f_star, "job_dir": os.path.abspath(a.job_dir), "rows": rows, "input_files": uniq}
    json.dump(out, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
