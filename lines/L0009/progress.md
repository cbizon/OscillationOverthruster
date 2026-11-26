# L0009 Option four — progress

## Current state (after the Nov 26 05:05Z timer run)

**Branch `method/rest`, worktree `~/Projects/experiments/sequel-data/worktrees/rest`,
tip c6dfd4d.** Numbers: `evidence/E0104-results.json` (artifact A0198). Pinned page (Chris
asked Nov 25): `lines/L0009/pinned/current-algorithm.md`. Keep it current at every change.

Stage 4 is built (D0087, D0088):
- `edmd`: MODE_STACK (2), EV_STACK (7); stack store SB (N+1,2: slot, body), SEGF (8 slots x
  2048 pieces x (2 + 15*8)), SINFO (t_end, accel bound, nseg); `rest_kernel.seg_state`
  (position plus velocity from the quartic); `body_state`, `first_contact_any`
  (conservative advancement, any pair with a stack sphere, horizon cut at span end),
  `predict_stack`, `invalidate`. run_events returns 3 (touch on a stack sphere) and 4 (span
  end). Stack spheres' S stays at span start until Python finishes the span.
- `sim`: `run_to` handles statuses 2 to 4 when `feed_stacks` (default True; tests and
  stack_event.py set False to get the old return 2). `_stack_span` integrates lazily (0.01,
  doubling) and cuts the span at a cell exit or side wall (sampled every 2e-4 of motion).
  `_stack_finish` books plate work, friction loss and plate impulse. `_on_stack_hit`: below
  v_rest join, else break plus an immediate ordinary collision (left to the queue, it looped
  at one instant). `_on_span_end`: split at an open contact, break at a wall, otherwise
  continue. Checkpoints with live stacks raise NotImplementedError; spans are paused at each
  run_to end.
- Tests: 55 method, 74 frozen pass.

E0104 (falsified): seed 1 f* 0.3 passes the old stall (5.8346) and reaches 5.88: 28 built,
7 joined, 28 broken, 661 pieces, 54 s Python. It then raises "rider and free sphere overlap"
in the step to 5.89. Seed 2 f* 0.3 and seed 1 f* 0.4 each spent about 705 s CPU inside one
0.01 step with no report, and I killed them. The CPU cap in feed_capped.py is only checked
between steps.

## What's next

1. Trace the overlap at 5.88 (seed 1, f* 0.3). Suspects: `_hand_back` of a broken stack
   sphere to rider (ride_setup from a state slightly off the plate), or a contact search
   against a stack sphere missing a touch because the span was cut or restarted. Debug
   harness pattern: wrap `s._on_stack_event/_on_stack_hit/_on_span_end` and print (see the
   session's tmp scripts; not kept). Start from `s.run_to(5.83)`, then `s.run_to(5.9)`.
2. Find where seed 2 and the f* 0.4 layer spend CPU (same harness, with faulthandler
   `dump_traceback_later`).
3. Rerun E0104 as a new experiment. Record the stack lifetime and the approach speed of
   each breaking hit, to answer the cost question and the question to Chris (immovable
   bounce between v_rest and v_wake for stack spheres?).
4. Still spheres (balance test): later.

## Jobs in flight

None (E0104 runs were killed; active.jsonl unchanged).

## Older state (after the Nov 25 10:38Z timer run)


Chris's instruction (lines/L0009/instruction.md, Nov 24): implement the resting-contact
design, no time-stepped code in disguise. Answers are D0073 to D0076 and
`lines/L0009/design.md` section 6. No new instruction entries since then.
Open question to Chris (asked three times, last Nov 25 10:38Z run): does the moving-stack integration count as
time-stepping? Default: build it (D0076) and measure the share of sphere-time in stacks.

**Branch `method/rest`, worktree `~/Projects/experiments/sequel-data/worktrees/rest`,
tip e299265.**

Nov 25 10:38Z run (evidence/L0009-build-2026-11-25-3.json):
- `granular/stack.py`: dense output (`_P`, `dense`), dip search `_sample_dip` in every
  accepted step (D0081; counters `n_dip_samples`, `n_dips`); `integrate(..., record=list)`
  appends `(t, h, position_poly)` per step, covering [t0, t_end] without gaps;
  `position_poly` = per-sphere quartic in the step fraction (D0082); sliding friction at zero
  slip uses the hint `contacts[k][3]` (`_fric_dir`, `start_sliding`, SLIP0 1e-13);
  `consistent_modes(t, y)` switches over-limit rolling contacts to sliding at a stack's start
  (D0083); `integrate` raises ValueError on a violated start condition. Contacts may now be
  4-element lists `[a, b, mode, hint]`.
- `granular/rest_kernel.py`: `seg_position(SEG_T, SEG_H, SEG_C, nseg, b, t, out)` (numba).
- `scripts/rest_plate/stack_replay.py [out.json]`: the stall pair (92 rider, 94 on it) as a
  two-sphere stack, offline: 94-on-92 needs 1.10 mu N to roll -> slides; stack lasts 0.396
  time units (66 steps, 840 force solves, 3.7 s CPU), ends with 94 leaving 92; books 2.6e-14.
- Tests: 52 method tests pass, 74 frozen pass. Use `--basetemp ~/Projects/experiments/sequel-data/tmp/<x>`
  with pytest (the checker flagged scratch in ~/.tmp twice). The plate part is now in the event loop (commit 4221e36):
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

### (older) What was next: sphere-on-sphere rest in the event loop

Done: (1) missed-dip fix (D0081); (2) decision on the compiled loop (D0082) and its segment
storage/evaluator; stack start modes (D0083); offline replay of the stall pair.

3. In `edmd.py`: MODE_STACK; arrays for stack segments (SEG_T, SEG_H, SEG_C per stack, plus
   sphere -> (stack, body) map); a new `run_events` return status at a stack event (internal
   contact change at the segment span's end, horizon end, or a free sphere / rider hitting a
   stack sphere below v_rest). In EV_PP with a rider partner below v_rest: return to Python
   instead of freeing the rider (replaces D0078). Python: build `Stack` from the rider's plate
   contact + hitter (remove residual approach, book it), `consistent_modes`, integrate with
   `record`, write segments, set modes; at the stack's end hand spheres back as free/rider.
4. Free spheres' contact searches against stack spheres via `seg_position` (conservative
   advancement needs a speed bound per segment: derive from the polynomial's derivative).
   Stack spheres' cell faces and walls likewise. Hits between v_rest and v_wake bounce off the
   stack sphere as if immovable (D0074); above v_wake the stack is broken.
5. Still spheres (balance test, no slip) as rigid plate followers: later, after a layer runs.
6. Replay the stall (stall.py), then the 2D grid (register experiments first), counting the
   share of sphere-time in stacks. The Python stack cost (about 9 ms per step) is the number
   to watch.

## Jobs in flight

None.

## Background (older results, still valid)

- Clusterlifter (`method/held-contact`, 8f8f999) is stopped as built; description in
  `lines/L0009/clusterlifter.md`.
- E0086 (clusterlifter v4, deep Gamma 5): audit failed nearly every cycle (worst 2.0e-4).
- E0087: clusterlifter with friction zero passed the bulk check at Gamma 3.5, f* 0.3, depth 10.
- The overlap tolerance in clusterlifter v4/v5 is rejected by Chris; the new design keeps
  the engine's 2e-8 check unchanged.
