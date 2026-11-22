"""Stepwise ramp of Gamma at fixed f*, through the referee's long_contact.py.

usage: ramp.py ENGINE OUTDIR --dim D --fstar F --N N --L L [--depth H] --seed S
               --gammas G0,G1,...  --hold CYCLES  [--first-hold CYCLES]
               [--max-cpu-hours-per-step X] [--wrapper field_recorder.py]

Step 0 is an ordinary referee run at G0 from the engine's default start
(--first-hold cycles, default --hold), or, if OUTDIR/step-000-gG0/checkpoint.npz
was written beforehand (caseb_start.py), from that cycle-0 state.  Every later step k starts from the
final checkpoint of step k-1 (a whole-cycle boundary, plate at its mean
position, so the plate's height is the same for both amplitudes; only its
velocity changes, by (G_k - G_{k-1}) g / omega) with Gamma set to G_k and
the cycle counter set to zero, and runs --hold cycles with
long_contact.py --resume.  Each step is a complete referee run in
OUTDIR/step-KKK-gG (survival, audit, bulk quantities, final checkpoint).
Nothing in the engine or the referee is changed: only the checkpoint's
recorded Gamma and cycle number are rewritten.

Resumable: steps whose summary says 'completed' are skipped.  Stops at the
first step that does not complete; with --turn-on-stop a step of the down
branch that does not complete is the engine's floor: the remaining steps at
or below the last completed Gamma are skipped and the ramp goes on upward
from the last completed step (a second stop ends the ramp).  One line per finished step is appended
to OUTDIR/ramp.jsonl (step, Gamma, outcome, cycles, CPU seconds, slow
episodes, audit failures).
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

SEQ = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent

ap = argparse.ArgumentParser()
ap.add_argument("engine", type=Path)
ap.add_argument("outdir", type=Path)
ap.add_argument("--dim", type=int, required=True)
ap.add_argument("--fstar", type=float, required=True)
ap.add_argument("--N", type=int, required=True)
ap.add_argument("--L", type=float, required=True)
ap.add_argument("--depth", type=float, default=None)
ap.add_argument("--seed", type=int, required=True)
ap.add_argument("--gammas", required=True)
ap.add_argument("--hold", type=int, required=True)
ap.add_argument("--first-hold", type=int, default=None)
ap.add_argument("--max-cpu-hours-per-step", type=float, default=1.0)
ap.add_argument("--max-cpu-hours-per-step-up", type=float, default=None,
                help="cap for a step whose Gamma is above the previous step's (default: the same cap); "
                     "Nov 18: the half-hour floor rule is for the way down only")
ap.add_argument("--scale-first-cap", action="store_true",
                help="step 0's cap is the per-step cap times first-hold/hold (the same cost per cycle)")
ap.add_argument("--turn-on-stop", action="store_true",
                help="when a step of the down branch does not complete, skip the remaining steps at or "
                     "below the last completed Gamma and go on (upward) from the last completed step")
ap.add_argument("--turn-above-fraction", type=float, default=None,
                help="with --turn-on-stop: also turn at the first down-branch step that completes but "
                     "uses more than this fraction of the per-step CPU cap (the engine is slowing; a "
                     "step that barely completes going down may not complete going up, E0055)")
ap.add_argument("--max-cpu-hours-total", type=float, default=None,
                help="do not start a step once the completed steps' CPU exceeds this (the ramp ends there, "
                     "resumable with a larger value)")
ap.add_argument("--keep-checkpoints-every", type=float, default=None,
                help="delete a completed step's checkpoint once the next step has completed, unless its "
                     "Gamma is a multiple of this or it is step 0 (a 3D checkpoint is 7 MB)")
ap.add_argument("--wrapper", default="lc_counters.py",
                help="lc_counters.py, or field_recorder.py to also record the height field")
a = ap.parse_args()
engine = a.engine.expanduser().resolve()
out = a.outdir.expanduser().resolve()
out.mkdir(parents=True, exist_ok=True)
gammas = [float(g) for g in a.gammas.split(",")]
sys.path.insert(0, str(SEQ / "referee"))
import bulk  # noqa: E402


def step_dir(k):
    return out / ("step-%03d-g%s" % (k, gammas[k]))


def summary(k):
    p = step_dir(k) / "summary.json"
    return json.loads(p.read_text()) if p.exists() else None


def step_cap(k):
    """CPU cap for step k (hours)."""
    if k == 0:
        if a.scale_first_cap and a.first_hold is not None:
            return a.max_cpu_hours_per_step * a.first_hold / a.hold
        return a.max_cpu_hours_per_step
    if a.max_cpu_hours_per_step_up is not None and last is not None and gammas[k] > gammas[last]:
        return a.max_cpu_hours_per_step_up
    return a.max_cpu_hours_per_step


def referee(k, cycles, resume):
    cmd = [sys.executable, str(TOOLS / a.wrapper), "--engine", str(engine),
           "--outdir", str(step_dir(k)), "--dim", str(a.dim), "--gamma", str(gammas[k]),
           "--fstar", str(a.fstar), "--N", str(a.N), "--L", str(a.L), "--seed", str(a.seed),
           "--cycles", str(cycles), "--checkpoint-every", str(cycles),
           "--max-cpu-hours", str(step_cap(k))]
    if a.depth is not None:
        cmd += ["--depth", str(a.depth)]
    if resume:
        cmd.append("--resume")
    with open(str(step_dir(k)) + ".log", "a") as log:
        subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=False)


last = None                     # index of the last completed step
spent = 0.0                     # CPU seconds of the steps done so far


def prune(j):
    """Step j's checkpoint is no longer needed to continue: drop it unless it is one to keep."""
    if a.keep_checkpoints_every is None or j is None or j == 0:
        return
    q = gammas[j] / a.keep_checkpoints_every
    if abs(q - round(q)) < 1e-6:
        return
    (step_dir(j) / "checkpoint.npz").unlink(missing_ok=True)

floor = None                    # with --turn-on-stop: Gamma of the last completed step when one stopped


def costly(k, s):
    """A completed down-branch step that used more than the turn fraction of its cap."""
    return (a.turn_on_stop and a.turn_above_fraction is not None and floor is None
            and last is not None and gammas[k] < gammas[last]
            and s.get("cpu_seconds", 0.0) > a.turn_above_fraction * a.max_cpu_hours_per_step * 3600)


for k, g in enumerate(gammas):
    s = summary(k)
    if s is not None and s.get("outcome") == "completed":
        if costly(k, s):
            floor = g
        spent += s.get("cpu_seconds", 0.0)
        last = k
        continue
    if a.max_cpu_hours_total is not None and spent > a.max_cpu_hours_total * 3600:
        raise SystemExit("total CPU cap reached before step %d (Gamma %s): %.2f h" % (k, g, spent / 3600))
    if floor is not None and g <= floor + 1e-9:
        continue                # below or at the floor: skipped after a stop
    if s is not None and "outcome" in s:
        if a.turn_on_stop and last is not None and floor is None and g < gammas[last]:
            floor = gammas[last]
            continue
        raise SystemExit("step %d ended as %s; not continuing" % (k, s["outcome"]))
    hold = a.hold if (k > 0 or a.first_hold is None) else a.first_hold
    if k == 0:
        # a step 0 written beforehand (e.g. caseb_start.py's pushed start, Nov 17) is run from its checkpoint
        referee(0, hold, resume=(step_dir(0) / "checkpoint.npz").exists())
    else:
        d = step_dir(k)
        if not d.exists():
            prev = np.load(step_dir(last) / "checkpoint.npz")
            data = {name: prev[name] for name in prev.files}
            assert float(data["t_local"]) == 0.0
            prm = data["params"].copy()
            prm[2] = g
            data["params"] = prm
            data["cycle"] = np.array(0)
            d.mkdir(parents=True)
            np.savez(d / "checkpoint.npz", **data)
            np.savez(d / "quantities.npz", time=np.zeros(0), drive_phase=np.zeros(0),
                     particle_count=int(prm[0]), **{q: np.zeros(0) for q in bulk.QUANTITIES})
            (d / "audit.json").write_text("[]\n")
            (d / "summary.json").write_text(json.dumps(dict(
                wall_seconds=0.0, cpu_seconds=0.0, slow_episodes=[],
                ramp=dict(step=k, gamma=g, previous_gamma=gammas[last],
                          from_checkpoint=str(step_dir(last) / "checkpoint.npz")))) + "\n")
        referee(k, hold, resume=True)
    s = summary(k)
    spent += s.get("cpu_seconds", 0.0)
    row = dict(step=k, gamma=g, outcome=s.get("outcome"), cycles=s.get("cycles_completed"),
               cpu_seconds=s.get("cpu_seconds"), slow_episodes=len(s.get("slow_episodes", [])),
               audit_failures=len(s.get("audit_failures", [])),
               worst_energy_residual=s.get("worst_energy_residual"))
    with open(out / "ramp.jsonl", "a") as f:
        f.write(json.dumps(row) + "\n")
    if s.get("outcome") == "completed":
        if costly(k, s):
            floor = g
        prune(last)
        last = k
    elif a.turn_on_stop and last is not None and floor is None and g < gammas[last]:
        floor = gammas[last]
    else:
        raise SystemExit("step %d (Gamma %s) ended as %s" % (k, g, s.get("outcome")))
print("ramp complete:", out)
