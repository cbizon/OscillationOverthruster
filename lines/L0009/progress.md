# L0009 Option four — progress

## Current state (after the Nov 25 04:40Z run, instruction lines/L0009/instruction.md)

Chris answered the five design choices (Nov 24 23:13) and said "Implement
this idea ... under no circumstances should you move to a time stepped code
in sheep's clothing". The answers are decisions D0073 to D0076 and
`lines/L0009/design.md` section 6 (with a build-status table).

**Build: branch `method/rest`, worktree `~/Projects/experiments/sequel-data/worktrees/rest`,
tip e4d6637 (branched from main 9d1db8b).**
- `granular/rest.py`: `RestParams` (v_rest 0.01, v_wake 0.05, n_friction_dirs 8),
  `balance_test` (phase-one simplex, inscribed 8-edge pyramid in 3D, exact in 2D),
  `PlateRide` (closed-form slide-to-roll on the plate, release time, plate work, friction loss).
- `tests/test_rest.py`: 17 tests, all pass. Run them with the main checkout's venv:
  `cd <worktree> && PYTHONPATH=. /Users/bizon/Projects/experiments/sequel.L0009/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_rest.py`
  (`uv run` inside the worktree fails: the roborobo path source is relative).
- Nothing is wired into `edmd.run_events`; no simulation has run with the method.

## What's next (in order)

1. Per-sphere state array (free / riding / still) and capture (base collision with
   e = 0, Walton unchanged) at plate hits below v_rest; plate riders moved by
   `PlateRide` (port to numba or keep the formulas inline in the kernel); release at
   G = 0; prediction of free spheres against plate riders.
2. Still spheres: move with the plate, zero spin; prediction against free spheres
   (plate root search on a sphere); hits below v_rest capture, between v_rest and
   v_wake bounce via `collide_wall` with the sphere normal (D0074), above v_wake wake.
3. Single rider on still spheres: integrated (adaptive, round-off tolerance, dense
   output), events for push = 0 and slip changes.
4. Moving stacks (D0076): joint ODE with contact-force linear solve; counters for
   integrator steps and sphere-time share in stacks.
5. Energy books into the audit (plate work for still and riding spheres, pair
   losses for slip); collapse cascade.
6. Frozen engine tests on the branch, replayed stalls, then the 2D grid (register
   experiments before running).

## Jobs in flight

None.

## Background (older results, still valid)

- Clusterlifter (`method/held-contact`, 8f8f999) is stopped as built; description in
  `lines/L0009/clusterlifter.md`.
- E0086 (clusterlifter v4, deep Gamma 5): audit failed nearly every cycle (worst 2.0e-4).
- E0087: clusterlifter with friction zero passed the bulk check at Gamma 3.5, f* 0.3, depth 10.
- The overlap tolerance in clusterlifter v4/v5 is rejected by Chris; the new design keeps
  the engine's 2e-8 check unchanged.
