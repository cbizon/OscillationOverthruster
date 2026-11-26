"""Per-cycle cost of the E0089 nudge loops near the wall, from each step's audit.json.

The per-step table (tools/e0089_step_table.py) spreads a step's events evenly over
its cycles. Near Gamma 4.5 to 4.6 the layer alternates between a cheap cycle and an
expensive one (period doubling), so a per-cycle average depends on where the step
stopped. This script reads the events per particle of every completed cycle from
audit.json (the referee's per-cycle audit; these are per cycle, not running totals),
and reports for each step:

  - the completed cycles' events, split into the cheap and expensive halves of the
    alternation by parity (odd and even positions in the step; the parity class
    with the smaller mean is 'cheap');
  - the mean per pair of cycles (one cheap + one expensive), over complete pairs only;
  - for a step stopped on the CPU cap, the unfinished cycle: step total (counters.json
    difference with the previous step) minus the completed cycles, with the fraction of
    the cycle it covered (event_time / drive period). This is the events of one partial
    cycle, so it is a lower bound on what that cycle would have cost;
  - tiny collisions (approach speed below the engine's 1e-10 threshold, counters
    C_TINYPP for sphere pairs, C_TINYPL for the plate), per particle, for the step.

Usage: python tools/e0089_cycle_table.py <out.json> <f*>=<mirror job dir> [...] [--steps 2]
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


def loop_table(f_star, job_dir, nsteps, files):
    loop = os.path.join(job_dir, "out", "loop")
    steps = sorted(d for d in os.listdir(loop) if re.match(r"step-\d{3}-g[\d.]+$", d))
    rows = []
    # The last nsteps steps, each differenced with the one before.
    for k in range(len(steps) - nsteps, len(steps)):
        s, s0 = steps[k], steps[k - 1]
        if int(s[5:8]) != int(s0[5:8]) + 1:
            raise SystemExit(f"non-consecutive steps {s0} -> {s}")
        paths = {
            "summary": os.path.join(loop, s, "summary.json"),
            "audit": os.path.join(loop, s, "audit.json"),
            "counters": os.path.join(loop, s, "counters.json"),
            "counters_prev": os.path.join(loop, s0, "counters.json"),
        }
        summ = json.load(open(paths["summary"]))
        audit = json.load(open(paths["audit"]))
        c = json.load(open(paths["counters"]))
        c0 = json.load(open(paths["counters_prev"]))["counters"]
        d = {key: c["counters"][key] - c0[key] for key in c0}
        for p in paths.values():
            files.append({"path": os.path.abspath(p), "bytes": os.path.getsize(p), "sha256": sha(p)})

        cyc = [round(a["events_per_particle"], 1) for a in audit]
        if len(cyc) != summ["cycles_completed"]:
            raise SystemExit(f"{s}: audit has {len(cyc)} cycles, summary {summ['cycles_completed']}")
        total = d["C_EVENTS"] / N
        row = {
            "step": s,
            "gamma": summ["gamma"],
            "outcome": summ["outcome"],
            "cycles_completed": len(cyc),
            "events_per_particle_each_cycle": cyc,
            "events_per_particle_step_total": round(total, 1),
            "completed_cycles_events_sum": round(sum(cyc), 1),
            "tiny_pair_collisions_per_particle_step": round(d["C_TINYPP"] / N, 3),
            "tiny_plate_collisions_per_particle_step": round(d["C_TINYPL"] / N, 3),
            "tiny_pair_collisions_step": d["C_TINYPP"],
            "tiny_plate_collisions_step": d["C_TINYPL"],
            "pair_collisions_per_particle_step": round(d["C_PP"] / N, 1),
            "plate_collisions_per_particle_step": round(d["C_PLATE"] / N, 1),
            "cpu_seconds": round(summ["cpu_seconds"], 1),
            "energy_gains": summ["energy_gains"],
            "audit_failures": len(summ["audit_failures"]),
        }
        covered = len(cyc)
        if summ["outcome"] != "completed":
            covered += c["event_time"] / ((summ["depth"] ** 0.5) / summ["f_star"])
        # Rates per cycle of the step's time span (completed + unfinished fraction).
        # Unlike events, these are only available per step, not per cycle.
        row.update({
            "cycles_spanned": round(covered, 3),
            "pair_collisions_per_particle_per_cycle_spanned": round(d["C_PP"] / N / covered, 1),
            "plate_collisions_per_particle_per_cycle_spanned": round(d["C_PLATE"] / N / covered, 1),
            "tiny_pair_collisions_per_cycle_spanned": round(d["C_TINYPP"] / covered),
            "tiny_plate_collisions_per_cycle_spanned": round(d["C_TINYPL"] / covered),
            "tiny_share_of_pair_collisions": d["C_TINYPP"] / d["C_PP"],
            "tiny_share_of_plate_collisions": d["C_TINYPL"] / d["C_PLATE"],
        })
        if len(cyc) >= 2:
            # Split by parity of the cycle (period doubling alternates them); the
            # parity class with the smaller mean is 'cheap'.
            odd, even = cyc[0::2], cyc[1::2]
            cheap, dear = (odd, even) if sum(odd) / len(odd) < sum(even) / len(even) else (even, odd)
            # alternation check: sign of successive differences flips every cycle
            flips = sum(1 for i in range(1, len(cyc) - 1)
                        if (cyc[i] - cyc[i - 1]) * (cyc[i + 1] - cyc[i]) < 0)
            npairs = len(cyc) // 2
            # complete pairs starting at the first cycle (each pair holds one of each half)
            pair_sums = [cyc[2 * i] + cyc[2 * i + 1] for i in range(npairs)]
            row.update({
                "alternation_flips": flips,
                "alternation_possible_flips": len(cyc) - 2,
                "cheap_cycles_events_range": [min(cheap), max(cheap)],
                "cheap_cycles_events_mean": round(sum(cheap) / len(cheap), 1),
                "expensive_cycles_events_mean": round(sum(dear) / len(dear), 1),
                "expensive_cycles_events_range": [min(dear), max(dear)],
                "costliest_cycle_events": max(cyc),
                "complete_pairs": npairs,
                "events_per_particle_per_pair_mean": round(sum(pair_sums) / npairs, 1),
                "events_per_particle_per_cycle_mean_completed": round(sum(cyc) / len(cyc), 1),
            })
        else:
            row["costliest_cycle_events"] = max(cyc) if cyc else None
        if summ["outcome"] != "completed":
            period = (summ["depth"] ** 0.5) / summ["f_star"]
            frac = c["event_time"] / period
            unf = total - sum(cyc)
            row.update({
                "unfinished_cycle_fraction": round(frac, 3),
                "unfinished_cycle_events_lower_bound": round(unf, 1),
                # the cycle before the unfinished one; under the alternation the
                # unfinished cycle is the other kind
                "last_completed_cycle_was": ("cheap" if len(cyc) >= 2 and cyc[-1] < cyc[-2] else
                                             "expensive" if len(cyc) >= 2 else "only cycle"),
            })
        rows.append(row)
    return {"f_star": f_star, "job_dir": os.path.abspath(job_dir), "rows": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("loops", nargs="+", help="f*=mirror job dir")
    ap.add_argument("--steps", type=int, default=2)
    a = ap.parse_args()
    files, loops = [], []
    for spec in a.loops:
        f, path = spec.split("=", 1)
        loops.append(loop_table(float(f), path, a.steps, files))
    json.dump({"loops": loops, "input_files": files}, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
