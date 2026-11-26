"""Per-pair-of-cycles collision ratios for E0089's stopping steps (checker Nov 26, point 1).

The cycle table (evidence/E0089-cycle-table.json) gives collisions of a stopped step per
cycle spanned. Near the wall a step alternates cheap and expensive cycles, so dividing a
stopped step that spans about 1.8 cycles (one cheap + most of an expensive one) by its
span, and comparing with a completed step's average over 25 alternating cycles, mixes
the two kinds. This compares like with like: the stopped step's whole count (at most one
pair of cycles: one cheap + part of an expensive one) against one pair of cycles of the
step before (twice its per-cycle mean, i.e. one cheap + one expensive). Applied only to
stopped steps spanning at most two cycles (f* 0.44 and 0.50); because the expensive cycle
was unfinished, the ratios are lower bounds.

Usage: python3 tools/e0089_pair_ratios.py evidence/E0089-cycle-table.json <out.json>
"""
import hashlib
import json
import sys

KEYS = {
    "pair_collisions_per_particle": ("pair_collisions_per_particle_step", "pair_collisions_per_particle_per_cycle_spanned"),
    "plate_collisions_per_particle": ("plate_collisions_per_particle_step", "plate_collisions_per_particle_per_cycle_spanned"),
    "tiny_pair_collisions": ("tiny_pair_collisions_step", "tiny_pair_collisions_per_cycle_spanned"),
    "tiny_plate_collisions": ("tiny_plate_collisions_step", "tiny_plate_collisions_per_cycle_spanned"),
}


def main():
    src, out = sys.argv[1], sys.argv[2]
    d = json.load(open(src))
    res = {}
    for loop in d["loops"]:
        rows = loop["rows"]
        stop, before = rows[-1], rows[-2]
        if stop["outcome"] == "completed" or stop["cycles_spanned"] > 2:
            continue
        r = {"gamma": stop["gamma"], "gamma_before": before["gamma"],
             "cycles_spanned": stop["cycles_spanned"]}
        for name, (step_key, per_cycle_key) in KEYS.items():
            stop_total = stop[step_key]
            before_pair = 2 * before[per_cycle_key]
            r[name] = {
                "stopped_step_total": stop_total,
                "step_before_per_pair": round(before_pair, 1),
                "ratio_per_pair_lower_bound": round(stop_total / before_pair, 1),
                "ratio_per_cycle_spanned_old": round(stop[per_cycle_key] / before[per_cycle_key], 1),
            }
        res[str(loop["f_star"])] = r
    h = hashlib.sha256(open(src, "rb").read()).hexdigest()
    json.dump({
        "experiment_id": "E0089", "line_id": "L0015",
        "what": __doc__.strip().split("\n\n")[0] + " Answers the checker review of Nov 26 (point 1).",
        "method": "ratio_per_pair_lower_bound = stopped step's whole count / (2 x step-before count per cycle). "
                  "ratio_per_cycle_spanned_old = the earlier figure (per cycle spanned, both steps).",
        "source": {"path": src, "sha256": h},
        "stopping_steps": res,
    }, open(out, "w"), indent=1)


if __name__ == "__main__":
    main()
