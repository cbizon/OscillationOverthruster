"""Settle-then-step ramp: each step runs until the layer settles, then Gamma
advances.  Uses the same step-directory layout as ramp.py so the same
analysis tools (loop_analysis.py, rates_table.py) work on the output.

Stopping rule (agreed with Chris, Nov 21):
  - Run in chunks of BLOCK_CYCLES (default 50).
  - After at least MIN_CYCLES (default 200), compare two 100-cycle windows:
    the last 100 cycles (window B) and the 100 before it (window A).
  - For each monitored quantity (pattern amplitude A and layer height), compute
    the mean of the two 50-cycle block values in each window.  The standard
    error of window A's mean is |block1 - block2| / 2 (block SE with 1 df).
  - Settled when |mean_B - mean_A| < 2 * SE_A for both quantities.
  - A step that reaches MAX_CYCLES (default 3000) is recorded as unsettled.

usage: settle_ramp.py ENGINE OUTDIR --dim D --fstar F --N N --L L --seed S
                      --gammas G0,G1,...
                      [--block-cycles 50] [--min-cycles 200] [--max-cycles 3000]
                      [--max-cpu-hours-per-step X] [--max-cpu-hours-total X]
                      [--keep-checkpoints-every X] [--keep-checkpoints-range LO:HI]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

SEQ = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent
BAND_LO = 3           # same as loop_analysis.py

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
ap.add_argument("--block-cycles", type=int, default=50)
ap.add_argument("--min-cycles", type=int, default=200)
ap.add_argument("--max-cycles", type=int, default=3000)
ap.add_argument("--max-cpu-hours-per-step", type=float, default=20.0)
ap.add_argument("--max-cpu-hours-total", type=float, default=None)
ap.add_argument("--keep-checkpoints-every", type=float, default=None,
                help="keep a completed step's checkpoint if its Gamma is a multiple of this")
ap.add_argument("--keep-checkpoints-range", default=None,
                help="LO:HI — keep every checkpoint in this Gamma range")
a = ap.parse_args()
engine = a.engine.expanduser().resolve()
out = a.outdir.expanduser().resolve()
out.mkdir(parents=True, exist_ok=True)
gammas = [float(g) for g in a.gammas.split(",")]
sys.path.insert(0, str(SEQ / "referee"))
import bulk  # noqa: E402

keep_lo, keep_hi = None, None
if a.keep_checkpoints_range:
    keep_lo, keep_hi = (float(x) for x in a.keep_checkpoints_range.split(":"))


def step_dir(k):
    return out / ("step-%03d-g%s" % (k, gammas[k]))


def summary(k):
    p = step_dir(k) / "summary.json"
    return json.loads(p.read_text()) if p.exists() else None


def referee(k, total_cycles):
    """Run the referee up to total_cycles for step k (--resume)."""
    cmd = [sys.executable, str(TOOLS / "field_recorder.py"),
           "--engine", str(engine),
           "--outdir", str(step_dir(k)), "--dim", str(a.dim),
           "--gamma", str(gammas[k]), "--fstar", str(a.fstar),
           "--N", str(a.N), "--L", str(a.L), "--seed", str(a.seed),
           "--cycles", str(total_cycles),
           "--checkpoint-every", str(a.block_cycles),
           "--max-cpu-hours", str(a.max_cpu_hours_per_step),
           "--resume"]
    if a.depth is not None:
        cmd += ["--depth", str(a.depth)]
    with open(str(step_dir(k)) + ".log", "a") as log:
        subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=False)


def corrected_amplitude(spec_frames):
    """Noise-corrected band amplitude from an array of spectra (frames x modes)."""
    band = spec_frames[:, BAND_LO - 1:]
    P = band.mean(axis=0)
    return float(np.sqrt(max(P.sum() - len(P) * np.median(P), 0.0)))


def block_values(step_k, total_cycles):
    """Compute per-block amplitude and thickness for all complete blocks."""
    d = step_dir(step_k)
    fields = np.load(d / "fields.npz")
    quant = np.load(d / "quantities.npz")

    spec = fields["spec"].astype(float)
    thickness = quant["thickness"].astype(float)

    frames_per_cycle = 32
    # Drop the initial frame (phase 0 before any cycles); each cycle then
    # has exactly 32 frames (phases 1/32..31/32 within plus phase 0 after).
    # With --resume the recorder drops frames past the checkpoint on reload,
    # so the total here reflects the cycles actually run.
    n_frames_expected = 1 + total_cycles * frames_per_cycle
    # Use however many frames are present (may be fewer if the run stopped)
    n_spec = min(len(spec), n_frames_expected)
    n_thick = min(len(thickness), n_frames_expected)
    # Number of complete cycles from the frame count (drop the first frame)
    cycles_from_spec = (n_spec - 1) // frames_per_cycle
    cycles_from_thick = (n_thick - 1) // frames_per_cycle
    n_complete = min(cycles_from_spec, cycles_from_thick)

    block = a.block_cycles
    n_blocks = n_complete // block
    amp_blocks = []
    thick_blocks = []
    for b in range(n_blocks):
        c0 = b * block
        # Frames for this block: skip frame 0, then 32 frames per cycle
        f0 = 1 + c0 * frames_per_cycle
        f1 = 1 + (c0 + block) * frames_per_cycle
        amp_blocks.append(corrected_amplitude(spec[f0:f1]))
        thick_blocks.append(float(thickness[f0:f1].mean()))

    return np.array(amp_blocks), np.array(thick_blocks), n_complete


def check_settled(amp_blocks, thick_blocks):
    """Check the stopping rule.  Returns (settled, details_dict).
    Requires at least 4 blocks (200 cycles with the default 50-cycle blocks)."""
    if len(amp_blocks) < 4:
        return False, {"reason": "not enough blocks"}

    def test_quantity(blocks, name):
        # Window A: the two blocks before the last two
        # Window B: the last two blocks
        a1, a2 = blocks[-4], blocks[-3]
        b1, b2 = blocks[-2], blocks[-1]
        mean_a = (a1 + a2) / 2
        mean_b = (b1 + b2) / 2
        se_a = abs(a1 - a2) / 2     # block SE with 1 df
        diff = abs(mean_b - mean_a)
        threshold = 2 * se_a
        passed = bool(diff < threshold) if se_a > 0 else bool(diff == 0)
        return passed, {f"{name}_mean_prev100": round(mean_a, 6),
                        f"{name}_mean_last100": round(mean_b, 6),
                        f"{name}_se_prev100": round(se_a, 6),
                        f"{name}_diff": round(diff, 6),
                        f"{name}_threshold": round(threshold, 6),
                        f"{name}_settled": passed}

    amp_ok, amp_detail = test_quantity(amp_blocks, "amplitude")
    thick_ok, thick_detail = test_quantity(thick_blocks, "thickness")
    detail = {**amp_detail, **thick_detail}
    settled = amp_ok and thick_ok
    detail["settled"] = settled
    return settled, detail


last = None      # index of the last completed step
spent = 0.0      # total CPU seconds


def prune(j):
    """Drop step j's checkpoint unless it's one to keep."""
    if j is None or j == 0:
        return
    g = gammas[j]
    # Keep in the special range
    if keep_lo is not None and keep_lo - 1e-6 <= g <= keep_hi + 1e-6:
        return
    # Keep at Gamma multiples
    if a.keep_checkpoints_every is not None:
        q = g / a.keep_checkpoints_every
        if abs(q - round(q)) < 1e-6:
            return
    (step_dir(j) / "checkpoint.npz").unlink(missing_ok=True)


for k, g in enumerate(gammas):
    s = summary(k)
    if s is not None and s.get("outcome") == "completed":
        spent += s.get("cpu_seconds", 0.0)
        last = k
        continue
    if a.max_cpu_hours_total is not None and spent > a.max_cpu_hours_total * 3600:
        raise SystemExit("total CPU cap reached before step %d (Gamma %s): %.2f h"
                         % (k, g, spent / 3600))
    if s is not None and "outcome" in s and s["outcome"] != "running":
        raise SystemExit("step %d ended as %s; not continuing" % (k, s["outcome"]))

    # Set up the step directory (from previous step's checkpoint, as ramp.py does)
    d = step_dir(k)
    if k == 0 and not d.exists():
        pass  # Fresh start: referee creates the directory and initial state
    elif k > 0 and not d.exists():
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
                 particle_count=int(prm[0]),
                 **{q: np.zeros(0) for q in bulk.QUANTITIES})
        (d / "audit.json").write_text("[]\n")
        (d / "summary.json").write_text(json.dumps(dict(
            wall_seconds=0.0, cpu_seconds=0.0, slow_episodes=[],
            ramp=dict(step=k, gamma=g, previous_gamma=gammas[last],
                      from_checkpoint=str(step_dir(last) / "checkpoint.npz")))) + "\n")

    # Run in chunks until settled or at max_cycles
    settled = False
    cycles_run = 0
    settle_detail = {}
    if s is not None and s.get("cycles_completed"):
        cycles_run = s["cycles_completed"]

    while cycles_run < a.max_cycles:
        target = min(cycles_run + a.block_cycles, a.max_cycles)
        if k == 0 and cycles_run == 0:
            # First step, first chunk: not a resume (no checkpoint yet)
            cmd = [sys.executable, str(TOOLS / "field_recorder.py"),
                   "--engine", str(engine),
                   "--outdir", str(d), "--dim", str(a.dim),
                   "--gamma", str(gammas[k]), "--fstar", str(a.fstar),
                   "--N", str(a.N), "--L", str(a.L), "--seed", str(a.seed),
                   "--cycles", str(target),
                   "--checkpoint-every", str(a.block_cycles),
                   "--max-cpu-hours", str(a.max_cpu_hours_per_step)]
            if a.depth is not None:
                cmd += ["--depth", str(a.depth)]
            with open(str(d) + ".log", "a") as log:
                subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=False)
        else:
            referee(k, target)

        s = summary(k)
        if s is None:
            raise SystemExit("step %d has no summary after running" % k)
        cycles_run = s.get("cycles_completed", 0)

        if s.get("outcome") not in ("completed", "running"):
            # Physical failure, frozen time, or CPU budget
            break

        if cycles_run >= a.min_cycles:
            amp_blocks, thick_blocks, n_complete = block_values(k, cycles_run)
            settled, settle_detail = check_settled(amp_blocks, thick_blocks)
            if settled:
                break

        if s.get("outcome") == "completed" and cycles_run >= target:
            # The referee completed all requested cycles but we want more
            pass
        elif s.get("outcome") != "completed":
            # The step didn't complete the requested cycles (CPU budget, etc.)
            break

    # Record the step outcome
    s = summary(k)
    step_cpu = s.get("cpu_seconds", 0.0) if s else 0.0
    spent += step_cpu
    # Remove 'settled' from settle_detail to avoid conflict with the explicit key
    settle_detail.pop("settled", None)
    row = dict(step=k, gamma=g, outcome=s.get("outcome") if s else "unknown",
               cycles=cycles_run, settled=settled,
               cycles_to_settle=cycles_run if settled else None,
               cpu_seconds=step_cpu,
               slow_episodes=len(s.get("slow_episodes", [])) if s else 0,
               audit_failures=len(s.get("audit_failures", [])) if s else 0,
               worst_energy_residual=s.get("worst_energy_residual") if s else None,
               **settle_detail)
    with open(out / "ramp.jsonl", "a") as f:
        f.write(json.dumps(row) + "\n")

    if s is None or s.get("outcome") not in ("completed", "running"):
        raise SystemExit("step %d (Gamma %s) ended as %s"
                         % (k, g, s.get("outcome") if s else "unknown"))

    if not settled and cycles_run >= a.max_cycles:
        print("step %d (Gamma %s): unsettled after %d cycles" % (k, g, cycles_run))

    prune(last)
    last = k

print("ramp complete:", out)
