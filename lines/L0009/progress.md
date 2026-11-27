# L0009 Option four — progress

## Current state (after the Nov 27 08:01Z timer run, summary sessions/2026-11-27-L0009-2.json)

**Branch `method/rest`, worktree `~/Projects/experiments/sequel-data/worktrees/rest`,
tip 0cd6a2b.** f397ada = D0098: side walls as stack contacts. `stack.Wall(axis, sign, pos)`
partner (still plane, normal push, roll/slide with mu; no plate power); `_stack_span` finds
a side-wall crossing by bisection (`_wall_list`: walls a sphere has no contact with, gap
offset by a negative start gap), cut kind 'wall'; `_on_span_end` -> `_on_wall`: approach
below v_rest -> wall contact added, approach removed by `_touch_projection` (now has wall
rows), `_stack_new`; else break (ordinary wall bounce). Side walls are no longer cell exits.
Singular force matrix -> lstsq (counter `Stack.n_indeterminate`, not yet reported by
feed_run). Counters `wall_cuts`, `wall_joined`, `wall_broken`. 1c2b35b adds
`scripts/rest_plate/cost_trace.py`. 0cd6a2b = D0099: `_restart_span` used for both span-end
restarts and pause restarts at the start of `run_to` (pause restarts had no handling);
`_pull_index` also reads integrate's "conditions violated [2k, ...]" as contact k pulling.
Method tests 57 pass; frozen 74 pass on main.

Results this run:
- E0111 (f397ada, supported): seed 1 f* 0.3 passes the wall loop at 5.918, completes 5.92
  (5 wall cuts, 2 joins), then stopped on the pause-restart error (-> D0099). Seed 2
  unchanged from E0109 (6.59 at 900 s cap; no wall cuts).
- E0112 (supported): f* 0.4 stack cost = force solves (99.1% of handler CPU; 9.1 solves per
  Dormand-Prince step; ~14 steps per stored piece; ~18 ms/solve under cProfile; numpy
  `cross` on 3-vectors and axis handling top the profile).
- E0113 (0cd6a2b, falsified): D0099 acted (2 splits); seed 1 stops in the step to 5.93 with
  "rider and free sphere overlap" (not traced).
- E0110 (975a4d7, f* 0.4, cap 2100 s): see the summary for its end; it tests D0095 past 5.276.
- Rider snaps up to 3.3e-10 now (max_snap; was 3e-14 before the plate landing D0096):
  check where (hand_back of a sphere slightly off the plate?).
- Local jobs: finished processes stay as zombies (/proc/<pid> exists, state Z); wait on the
  result json, not on the pid.

## What's next

1. Trace the "rider and free sphere overlap" in seed 1 f* 0.3, step 5.92 -> 5.93 (E0113).
   Suspects: a wall join or pull split handing a sphere back as a rider next to a free
   sphere; the 3.3e-10 snaps.
2. Make force solves cheap (E0112): write the 3-vector cross products and the matrix build
   without numpy small-array calls (or in numba), and locate contact changes with fewer
   full steps (the bisection takes up to 200 full Dormand-Prince steps per event; use the
   dense output instead). Same results to round-off; a performance change: time both on
   the same inputs.
3. Report `n_indeterminate` in feed_run; check seed 2 at 6.59 (where its time goes).
4. CPU cap inside a handler (cost_trace's SIGPROF timer works; use it in feed_run).
5. Still open to Chris: immovable bounce between v_rest and v_wake for stack spheres.

## Jobs in flight

None at the end of this run (see the summary for E0110).

## Older state (after the Nov 27 05:05Z timer run, summary sessions/2026-11-27-L0009.json)

**Branch `method/rest`, worktree `~/Projects/experiments/sequel-data/worktrees/rest`,
tip 975a4d7** = D0095 (pull found at a span restart or after an in-span mode change:
span ends as 'open' at that contact, or `_Pull` before the first piece -> `_start_parts`
without it; counters `pull_opened`, `pull_dropped`) + D0096 (plate cut records
`rec['plate_body']`; `_on_span_end` kind 'plate' breaks, then hands that sphere back as a
rider if |vz - vp| < v_rest and plate accel > -g; counter `plate_landed`). Method tests 55
pass; frozen 74 pass on main (start of this run).

Results (evidence/E0108-results.json A0211, E0109-results.json A0212):
- E0108 (f6d148d, D0093 alone, falsified): plate cut acted (2 cuts, first 5.88242 sphere
  92); seed 1 looped at 5.886136 (92 left free at plate, rejoined rebuilt [93, 94]).
  Seed 2 stuck in one handler call in step 6.23, killed at 1307 s CPU (no json).
- E0109 (975a4d7, falsified on f* 0.4 clause): seed 2 f* 0.3 reaches 6.59 (cap 900 s;
  pull_opened 7, pull_dropped 8, plate_landed 1, fallback collisions 4); seed 1 f* 0.3
  reaches 5.91 then loops at 5.918301642464967: sphere 92 rests against the right side
  wall (x + r = 20.0000) in stacks [93, 94, 92]/[92, 94]; every span is cut at start as
  'cell' at a wall -> break -> rebuild. f* 0.4 stops at 5.27 (cap): handler calls of 112 s
  (69 joins 4-stack at 5.2508) and 18 s; integration cost, not a loop.
- The 579 s of the Nov 26 D0093 trace was not reproduced (steps to 5.88 as in E0107).
- Local jobs: run them inside the run (they do not survive it). The CPU cap in
  feed_run.py is checked only between handler calls; a single long call overruns it.

## What's next

1. Side walls as stack contacts (like the plate contact): a stack sphere at a wall gets a
   wall contact (normal push, friction), so spans are not cut at once. Design note first
   (decision), then build and rerun seed 1 f* 0.3.
2. f* 0.4 cost: instrument `stack.integrate` (steps, rejected steps, mode switches, force
   solves per call) on the 5.2508 join; find what makes 3-5 sphere stacks cost 18-112 s.
3. Seed 2: check the near-same-instant loop on 54/60 (checker Nov 26) is gone (E0109 had
   4 fallback collisions, E0107 19,779) and where it is spending time at 6.59.
4. Make the CPU cap interrupt inside a handler (check in the integrator loop) so runs stop
   on time.
5. Counter for the D0092 probe; seed 2 side-by-side rider collisions (D0078).
6. Still open to Chris: immovable bounce between v_rest and v_wake for stack spheres.

## Jobs in flight

None (all E0108/E0109 processes ended or were stopped; active.jsonl unchanged).

## Older state (after the Nov 26 08:04Z timer run, summary sessions/2026-11-26-L0009-3.json)

**Branch `method/rest`, worktree `~/Projects/experiments/sequel-data/worktrees/rest`,
tip f6d148d.** 3895370 = D0091 (drop a pulling contact at a stack start, helper
`_start_parts` shared with `_on_span_end`; feed_run.py CPU cap also checked at every stack
handler call); 607b687 = D0092 (in `edmd.first_contact_any`, a closing pair at contact is a
touch only if the gap could go below -RIDER_GAP_TOL before it opens; probe step from M).
Method tests 55 pass on 607b687; frozen 74 pass on main. **f6d148d = D0093, UNTESTED**:
`_stack_span` samples the plate gap of stack spheres with no plate contact, cuts the span at
the crossing (bisection), end_kind 'plate' -> `_on_span_end` breaks the stack. Counter
`stack_stats['plate_cuts']`.

Found this run (evidence/E0105-collection.json, E0106-results.json, E0107-results.json):
- **E0105 s1_f0.4 has no result**: pid 1080 gone, log stopped at 5.25 (07:03). Local
  background jobs do NOT outlive the run here (each run gets a fresh process-id space, its
  own pids start near 80; no `ps`, `uptime`, `caffeinate`). Run local jobs only within the
  run, or on Hatteras.
- **E0106 (D0091, falsified)**: path ran 30 times, but pair 93-94 re-touched at an approach
  of 7e-18 at the same instant -> loop at 5.870650988602072. In-step CPU cap works (f* 0.4
  stopped at 5.276 after 1205 s).
- **E0107 (D0091+D0092, supported)**: seed 1 f* 0.3 passes 5.8707, completes step 5.88,
  stops in step to 5.89: "sphere penetrates the bottom plate". Traced: free sphere 92 joined
  stack [93, 94] at 5.8821867 with plate gap 4.16e-6 and no plate contact; the stack
  integration has no plate check for it; at the break (86 hits 94, 5.8845922) 92 is handed
  back with gap -4.65e-5. Seed 2 identical in all three experiments (penetration after
  6.22; its two pulling contacts come at span restarts in `_stack_span`, which still
  refuse; probably the same sinking cause, not traced). Seed 1 f* 0.4 crawls from 5.25.
- With D0093 the trace (`run to 5.88 in 0.01 steps, then run_to(5.89)`) used 579 s CPU
  without finishing (about 110 s before). Unknown why: a crawl, or many plate cuts.

## What's next

1. Test D0093: rerun the trace with per-handler logging (pattern: wrap `s._on_stack_event`,
   `_on_stack_hit`, `_on_span_end`, log t, i, j, stacks before/after and plate gaps; plus
   `plate_cuts`) and faulthandler; find where the 579 s goes. Register an experiment first,
   with `at` taken from `date -u` (this run's E0106/E0107 `at` were estimates 20-30 s after
   the commits; disclosed in the summary).
2. Span restarts (`_stack_span` -> `consistent_modes` raising "pulls") still refuse and
   break the whole stack: apply D0091 there too.
3. Add a counter for the D0092 probe (how often a contact touch was skipped as round-off).
4. f* 0.4 crawl from 5.25: where the stack integration spends its time (largest stack,
   steps per span).
5. Seed 2's 19,779 side-by-side rider collisions (D0078 rule).
6. Still open to Chris: immovable bounce between v_rest and v_wake for stack spheres. E0105
   numbers without the loop repeats: seed 1, 23 real touches, 18 at or above v_rest, 1 at or
   above v_wake, median approach 0.017; seed 2, 13 touches, 9 at or above v_rest, 5 at or
   above v_wake.

## Jobs in flight

None (E0107 s1_f0.4 collected or stopped at the end of this run; see the summary).

## Older state (after the Nov 26 05:05Z timer run)

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
