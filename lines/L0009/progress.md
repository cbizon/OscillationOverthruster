# L0009 Option four — progress

## Current state (after the Nov 25 09:33Z timer run)

Chris's instruction (lines/L0009/instruction.md, Nov 24): implement the resting-contact
design, no time-stepped code in disguise. Answers are D0073 to D0076 and
`lines/L0009/design.md` section 6. No new instruction entries since then.
Open question to Chris (asked twice): does the moving-stack integration count as
time-stepping? Default: build it (D0076) and measure the share of sphere-time in stacks.

**Branch `method/rest`, worktree `~/Projects/experiments/sequel-data/worktrees/rest`,
tip bcd1d5f.** The plate part is now in the event loop (commit 4221e36):
- `granular/edmd.py`: `P_VREST`, `P_VWAKE` (NP_FLOAT 18; v_rest 0 = main's engine);
  `mode` array (MODE_FREE 0, MODE_RIDER 1) and rider rows `RP` (rest_kernel layout) passed
  to `run_events`/`schedule`/`predict`; `advance_rider` books each ride segment (vertical
  energy change -> EN_PLATE_WORK, horizontal+spin change -> EN_PLATE_DISS with gain check,
  m(dvz + g dt) -> EN_PLATE_JZ); `advance_any` dispatches; `capture_on_plate` (Walton, e = 0)
  in EV_PLATE when |vp - vz| < v_rest and G > 0 (D0077), centre snapped to the plate with
  EN_MAX_SNAP (D0080); `EV_REL` release; `predict_rider` (release, x/y/z faces and walls by
  `first_cross` monotone pieces + bisection, rider-free and rider-rider conservative
  advancement); free spheres' `predict` calls the rider-free search for rider neighbours;
  EV_PP and EV_WALL free a rider (D0078, temporary); counters C_CAPTURE, C_RELEASE,
  C_RIDERHIT, C_RIDERSEARCH, C_REPREDICT; `project_rest`, `synchronize_rest`, `rebase_rest`.
- `granular/sim.py`: `Simulation(..., v_rest=0.0, v_wake=0.0)`, `mode`/`RP` permuted at sort,
  saved in checkpoints, rebased per cycle; `snapshot` uses `project_rest`.
- `granular/rest_kernel.py`: `first_cross`, `first_contact_rider_rider`; overlap refusal at
  the engine's 2e-8 (D0079).
- Tests: 45 pass (tests/test_rest_engine.py 4 new). Frozen tests with method off: 74 pass.
  Run: `cd <worktree> && PYTHONPATH=.:tests /Users/bizon/Projects/experiments/sequel.L0009/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_rest_engine.py tests/test_rest.py tests/test_stack.py tests/test_rest_kernel.py`
  and `PYTHONPATH=. ... -m pytest -q -p no:cacheprovider <main>/referee/tests`.
- **Numba cache trap:** after editing `rest_kernel.py`, delete `granular/__pycache__/*.nbi
  *.nbc` in the worktree, or `edmd` keeps the old compiled version (cost one false failure).
- Reproducers: `scripts/rest_plate/{one.py,layer.py,stall.py}` on the branch (run with
  `PYTHONPATH=.` from the worktree). Numbers: `evidence/L0009-build-2026-11-25-2.json`.

**Result:** one sphere captured/ridden/released, books close to 1e-14. A 2D layer (N 100,
L 20, Gamma 2, f* 0.3, depth 5, seed 1) stalls in cycle 0 at t = 5.8346320: sphere 94 rests
on rider 92; the plate carries 92 into 94, the hit frees 92 (D0078), plate recaptures it at
once; 10,000 rounds in 6e-8 time units. This is the stage-3 case.

## What's next: sphere-on-sphere rest in the event loop

1. Fix the stack integrator's weakness the checker raised (review of 2026-11-24-L0009-2):
   contact changes are found only by a sign change between step ends; a push dipping below
   zero and recovering within one step is missed. Use a bound (like first_root) or check
   the dense output's extremum within each step.
2. Decide and record how stacks run with the compiled loop: `run_events` returns to Python
   at a stack event (new return code) and `stack.py` advances it, or compile stack.py.
3. A sphere hitting a rider (or a stack sphere) below v_rest joins a moving stack; still
   spheres (balance test passes, no slip) move rigidly with the plate (a rider row with zero
   horizontal motion; a sphere on still spheres is the plate plus an offset, needs a z-offset
   field separate from RP_R); hits between v_rest and v_wake bounce as off the plate (D0074);
   above v_wake the sphere is freed.
4. Stack spheres' contacts with free spheres and cell faces as events (dense output roots).
5. Replay the stall (stall.py), then the 2D grid (register experiments first), counting the
   share of sphere-time in stacks.

A timer (`program wake`) starts the next run of this line.

## Jobs in flight

None.

## Background (older results, still valid)

- Clusterlifter (`method/held-contact`, 8f8f999) is stopped as built; description in
  `lines/L0009/clusterlifter.md`.
- E0086 (clusterlifter v4, deep Gamma 5): audit failed nearly every cycle (worst 2.0e-4).
- E0087: clusterlifter with friction zero passed the bulk check at Gamma 3.5, f* 0.3, depth 10.
- The overlap tolerance in clusterlifter v4/v5 is rejected by Chris; the new design keeps
  the engine's 2e-8 check unchanged.
