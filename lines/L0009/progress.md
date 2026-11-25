# L0009 Option four — progress

## Current state (after the Nov 25 04:40Z run, instruction lines/L0009/instruction.md)

Chris answered the five design choices (Nov 24 23:13) and said "Implement
this idea ... under no circumstances should you move to a time stepped code
in sheep's clothing". The answers are decisions D0073 to D0076 and
`lines/L0009/design.md` section 6 (with a build-status table).

**Build: branch `method/rest`, worktree `~/Projects/experiments/sequel-data/worktrees/rest`,
tip 89b7bfe (branched from main 9d1db8b). The engine (`granular/edmd.py`) is still main's.**
- `granular/rest.py`: `RestParams` (v_rest 0.01, v_wake 0.05, n_friction_dirs 8);
  `balance_test` (phase-one simplex, inscribed 8-edge pyramid in 3D, exact in 2D);
  `PlateRide` (closed-form slide-to-roll on the plate, release time, plate work,
  friction loss); `first_root` (conservative-advancement first-contact search, status
  0 contact / 1 none / 2 re-predict here; refuses overlaps); `rider_free_gap`.
- `granular/stack.py`: moving stacks. `Stack` (contacts to PLATE, a `Fixed` still
  sphere, or another body; mode 'roll' or 'slide'), contact forces from a linear solve,
  `integrate` (Dormand-Prince 5(4), rtol 1e-12) returning at the first contact event
  ('open', 'slide', 'roll'). The caller switches the contact's mode or removes it;
  nothing is changed at ordinary steps. Last two state entries: plate work, friction loss.
- `granular/rest_kernel.py`: numba `ride_setup`, `ride_state`, `first_contact_rider_free`
  with rider rows (`RP_*`, 13 floats per sphere).
- Tests: `tests/test_rest.py` (29), `tests/test_stack.py` (3), `tests/test_rest_kernel.py` (9);
  41 pass. Run with the main checkout's venv:
  `cd <worktree> && PYTHONPATH=.:tests /Users/bizon/Projects/experiments/sequel.L0009/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_rest.py tests/test_stack.py tests/test_rest_kernel.py`
  (`uv run` inside the worktree fails: the roborobo path source is relative).
- Numbers: `evidence/L0009-build-2026-11-25.json`.

## What's next: wiring into the event loop (stage "plate" first)

Touch points in `granular/edmd.py` (all assume ballistic motion today):
1. a per-sphere mode array (0 free, 1 plate rider, 2 still, 3 stack member) and the
   rider rows; `advance` dispatches on mode (rider: `ride_state`);
2. `EV_PLATE`: capture when approach speed < v_rest and effective gravity > 0
   (Walton collision with e = 0, booked as plate collision), then `ride_setup`;
3. rider events: release time (→ free, ballistic from the ride state), horizontal cell
   faces and side walls (nonlinear while sliding: use the conservative search),
   pair contacts with free spheres (`first_contact_rider_free`, from both sides of the
   pair: the inline pair formula in `predict` must skip riders), rider–rider on the plate;
4. a rider hit: below v_rest capture into a stack (stage 3), above it the rider becomes
   free and the ordinary collision happens;
5. energy books: plate work and friction loss of rides into EN_PLATE_WORK / EN_PLATE_DISS
   at each ride's end or at each sync; `project`, `synchronize`, `rebase`, `min_gap`,
   `check_cells`, checkpoints and `sim.py` must know about riders;
6. then still spheres (moving with the plate, wake/bounce/capture by D0074), riders on
   still spheres and moving stacks (compile `stack.py` or call it from Python between
   kernel calls; decide and record);
7. frozen engine tests on the branch, replayed stalls, then the 2D grid (register first).

A timer (`program wake`) starts the next run of this line to continue.

## Jobs in flight

None.

## Background (older results, still valid)

- Clusterlifter (`method/held-contact`, 8f8f999) is stopped as built; description in
  `lines/L0009/clusterlifter.md`.
- E0086 (clusterlifter v4, deep Gamma 5): audit failed nearly every cycle (worst 2.0e-4).
- E0087: clusterlifter with friction zero passed the bulk check at Gamma 3.5, f* 0.3, depth 10.
- The overlap tolerance in clusterlifter v4/v5 is rejected by Chris; the new design keeps
  the engine's 2e-8 check unchanged.
