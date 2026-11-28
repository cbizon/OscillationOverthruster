# L0009 Option four — progress

## Current state (after the Nov 28 07:02Z timer run, summary sessions/2026-11-28-L0009-2.json)

**Branch `method/rest`, worktree `~/Projects/experiments/sequel-data/worktrees/rest`, tip dbc0f59.**
- dbc0f59 = D0104: `Simulation._pair_list` offsets each inner pair by -RIDER_GAP_TOL/(4 (Ra+Rb))
  (the D0102 floor in gap terms). Method tests 57 pass.
- Scripts: `trace_live.py` (per-call JSON-lines log, flushed; SIGPROF CPU cap that fires inside
  handlers; `kill -PROF <pid>` stops it cleanly with a cap line; step-end pickle, resumable);
  `live_summary.py` (steps, counters over CPU, bursts); `diag/diag5.py` (stack starts: modes,
  switches, pushes, friction ratios, with and without the joining contact).

Results this run:
- E0123 (39e28e3, supported): seed 1 5.92->5.93 crawls. Phase 1: 86 kept beside 84, rejoined
  every 4.45e-10 (inner_joined 97 by 180 s). Phase 2 from 5.920524234706: stacks [84, 93] and
  [92, 94] broken by a 93-94 stack_hit and rebuilt (wall cut on [92, 94]) every 9.8e-15; 1076
  calls; got out at ~600 s; 5.920524449586 at 801 s.
- E0124 (falsified): f* 0.4 completes 5.29 (240 s), then crawls: 5.291911 at 801 s, kept 121,
  released 0.
- E0125: inside the chatter the joining contact 84-86 itself slides (slip 0.0102) and pulls
  (-0.0786, identical each round); the inner check was cut by gap noise -> D0104.
- E0126 (D0104, falsified): chatter gone (inner_joined 3), seed 1 stays in phase 2 from
  5.920524237 for 1380 calls to the 900 s cap. f* 0.4: 5.29 at 500 s, 5.292022 at 900 s, last
  burst 216 calls of joins/builds/breaks on 58, 69, 54, 60.
- E0116 outcome corrected (new record): the inner check acted before 5.92.
- Machine was loaded: ~0.6 CPU-s per wall-s; plan caps in CPU accordingly (a 900 s cap took
  ~25 min wall).

## What's next

0. Seed 1 phase 2: trace the 93-94 stack_hit (approach speed, gap, are [84, 93] and [92, 94]
   separating?). `_on_stack_hit` breaks both stacks on a touch between stacks. If round-off:
   apply the D0092/D0102 rule to stack-stack pairs in `edmd.first_contact_any`. If real slow
   touches: join the stacks below v_rest (asked Chris; record a decision). Start from
   runs/E0125/snap.pkl (39e28e3 state inside phase 1, 5.92052378) or regenerate a state at
   5.9205242372 with snap_at.py (from runs/E0118 pickle, ~3 min CPU with D0104).
1. f* 0.4 crawl near 5.292 (E0124 keep-rejoin bursts on 54; E0126 join/build/break on 58, 69).
   The 5.29 pickle was not kept (rm at the end; disclosed): regenerate with trace_live (240 s).
2. Is D0103 still needed with D0104? Test handing detached spheres back free with the floor.
3. Singular force matrices by condition number (E0117); time the force build in a layer;
   join all touches at one instant at once; `n_indeterminate` in feed_run; seed 2 at 6.59.
4. Still open to Chris: immovable bounce between v_rest and v_wake for stack spheres; join
   stacks on a slow stack-stack touch?

## Jobs in flight

None (all local processes ended; active.jsonl has no L0009 entries). Snapshots kept:
runs/E0114 (A0217), runs/E0118 (A0221: s1_f0.3_t5.92.pkl), runs/E0119 (A0222: f04_loop.pkl),
runs/E0121 (A0224), runs/E0125 (A0228: snap.pkl inside seed 1's chatter, made at 39e28e3).

## Older state (after the Nov 28 05:03Z timer run, summary sessions/2026-11-28-L0009.json)

**Branch `method/rest`, worktree `~/Projects/experiments/sequel-data/worktrees/rest`,
tip 39e28e3 (code) + later script commits.** New this run:
- 98fe790 = D0101: contacts carried over rolling from a live stack keep rolling at a new
  stack's start (`Stack.held`, `Simulation._hold`, counter `held_kept`); `_stack_finish` at
  the span's start instant restores the first segment's modes (it left the span's END modes:
  real bug); undone joins count as `join_dropped`, not `joined`.
- fde8612 = D0102: `edmd.first_contact_any` round-off rule walks on and reports the touch
  where hv reaches -RIDER_GAP_TOL/2 (the real crossing), not at the zone's start.
- 39e28e3 = D0103: a pulling contact dropped at a stack's start that leaves one plate-held
  part and detached off-plate parts -> the stack keeps ALL spheres; detached ones are
  members with no contact (`_start_kept`), joined again by the inner-pair check (D0100)
  when their gap closes past its start value; released at the next span restart
  (`_restart_span`, counter `members_released`). Counter `kept_members`.
- Scripts: `snap_at.py` (pickle at the first handler call at/after a time: replay a loop in
  seconds), `scripts/rest_plate/diag/diag*.py` (probe copy, force matrix at a refused start,
  stack starts with pushes under alternative modes).
Method tests 57 pass; frozen 74 pass on main and against the branch engine (39e28e3).

Results this run:
- E0119 (supported): the undone join is NOT a round-off approach or a singular matrix
  (condition 30). Start modes disagree with the modes a moment later: a contact sliding
  with tiny slip at the start makes the joining contact pull; it sticks soon after, then
  the free sphere closes. Also a10d930 passes the 22e1f09 seed-1 loop instant and loops
  3.6e-11 later (same pair).
- E0120 (D0101, falsified): seed 1 loop moved to 5.920524091; f* 0.4 unchanged (hold did
  not act there).
- E0121 (D0101+D0102, falsified): loops at 5.281595188 (f* 0.4) and 5.920506155 (seed 1,
  EARLIER than D0101 alone); same mechanism (sliding contact slip 1.5e-7 / 3.4e-5; with it
  rolling the joining contact pushes +0.43 / +0.37).
- E0122 (D0103): f* 0.4 from runs/E0119/f04_loop.pkl COMPLETES 5.29 (148 calls, 240 s;
  kept_members 31, inner_joined 27, max 8 calls at one instant, touch_max_gain 1.5e-15).
  Seed 1 (5.92 -> 5.93 from runs/E0118 pickle): still running after 19.5 min with no output
  when the run ended (earlier traces of that step: 92-281 s). Unknown: crawl or slow progress.

## What's next

0. FIRST: rerun seed 1 5.92 -> 5.93 at 39e28e3 with a CPU cap and a handler log written as
   it goes (trace_step.py only writes at the end; add a per-call flush and faulthandler
   dump_traceback_later) to see whether D0103 makes it crawl (a member kept in a stack for a
   whole span? many restarts?). Then run f* 0.4 from 5.29 on; register first. Watch kept_members/members_released,
   touch_max_gain (1.5e-15 now, was 8e-17), start_refused (19 in E0122 f* 0.4).
1. Singular force matrices: count condition numbers in real stacks; lstsq or a rank check
   when singular (np.linalg.solve does not flag them, E0117).
2. Time the direct force build in a layer; locate contact changes from the dense output;
   join all touches at one instant at once.
3. Report `n_indeterminate` in feed_run; CPU cap inside a handler; seed 2 at 6.59.
4. Checker (Nov 27): a separating touch between two stacks breaks both (negative-approach
   93-94 hits in seed 1): decide whether it should.
5. Still open to Chris: immovable bounce between v_rest and v_wake for stack spheres.

## Jobs in flight

None collected. The E0122 seed 1 trace (writing runs/E0122/trace_s1.json) was still running at
the end; if that file appears, run `program record` on runs/E0122 again and read it.
Snapshots kept: runs/E0114 (A0217), runs/E0118
(A0221), runs/E0119 (A0222: f04_loop.pkl at 5.281594649757622, s1_loop.pkl), runs/E0121
(A0224: f04_loop2.pkl, s1_loop2.pkl).

## Older state (after the Nov 27 09:53Z timer run, summary sessions/2026-11-27-L0009-3.json)

**Branch `method/rest`, worktree `~/Projects/experiments/sequel-data/worktrees/rest`,
tip a10d930.** 22e1f09 = D0100: pairs of stack spheres with no contact between them are
watched like a side wall (`Simulation._pair_list`, span cut by bisection, end kind 'inner',
`_on_inner`: approach < v_rest -> rolling contact added with the join projection, else break
+ ordinary collision; counters `inner_cuts`, `inner_joined`, `inner_broken`). a10d930 =
`Stack.forces` builds the matrix directly (M = H G, `_cx` cross product); the old build is
`Stack.forces_loop` (reference). Scripts: `snap_run.py` (run to a step end, pickle the
Simulation: pickling works, ~16 MB), `trace_step.py` (one step from a pickle with handler
logging), `force_bench.py`. Method tests 57 pass at a10d930; frozen 74 pass on main.
Second checkout for tracing at a fixed commit: `~/Projects/experiments/sequel-data/worktrees/rest-trace`
(detached; left at 915363e).

Results this run:
- E0115 (supported): the "rider and free sphere overlap" (E0113) came from spheres 84 and 93
  of one 5-sphere stack with no contact between them overlapping by 4.6e-5, handed back when
  86 was hit at 5.92284 -> D0100.
- E0116 (D0100 at 22e1f09, falsified): seed 1 path acted (inner_cuts 1, joined 1), overlap
  gone, but a same-instant loop at 5.920523784634156 (84-86, approach 1e-18). Seed 2 identical
  to E0111 (CPU cap at 6.59, no inner cut).
- E0118 (supported): that loop = free 86 joins [84, 93], the new contact pulls, dropped
  (D0091), 86 back free at gap 4.3e-14 still closing at 7.8e-19, touch reported again.
  36 of 41 calls move pull_dropped AND joined (both counters count repeats).
- E0117 (supported): direct force build = same system to 2.1e-15 where well conditioned;
  6.3-10.5x cheaper per solve; replay 2.21 vs 6.70 s. 38 of 300 random rolling stacks have
  singular force matrices (condition > 1e12) that `np.linalg.solve` does NOT flag, so the
  D0098 lstsq fallback never runs for them. Check how often real stacks hit this.
- E0114 (supported): f* 0.4 loop at 5.2816 is the same: 54-59 opens (split), 59 rejoins at 1.5e-16,
  pulls, dropped, back free still closing; 40 of 41 calls move pull_dropped and joined.

## What's next

0. Fix the dropped-join loop (E0118, and very likely E0110's 5.2816): when a join's new
   contact is dropped as pulling, the pair separates by its accelerations; the round-off
   approach left must not count as a touch. Look first at why D0092's probe in
   `edmd.first_contact_any` does not reject it (gap 4.3e-14 > 0 so maybe not "at contact";
   or the joiner is free and the probe uses the wrong acceleration bound). Also stop
   counting undone joins in `joined`. Test from runs/E0118/s1_f0.3_t5.92.pkl (made at
   22e1f09; trace_step.py, 320 s) and from runs/E0114/s1_f0.4_t5.28.pkl (made at b1702ad).
1. Singular force matrices: count condition numbers in real stacks; use lstsq (or a rank
   check) when the matrix is singular, not only when solve raises.
2. Time the direct force build in a layer (seed 1 f* 0.4 to 5.28 took 1350 s with the old
   build); then locate contact changes from the dense output; join all touches at one
   instant at once (checker: ~300 of 494 s in E0112 were sequential joins at 5.251078).
3. Report `n_indeterminate` in feed_run; CPU cap inside a handler; seed 2 at 6.59.
4. Still open to Chris: immovable bounce between v_rest and v_wake for stack spheres.

## Jobs in flight

None kept (local jobs do not survive the run). Snapshots kept: runs/E0114 (A0217),
runs/E0118 (A0221).

## Older state (after the Nov 27 08:01Z timer run, summary sessions/2026-11-27-L0009-2.json)

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
- E0110 (975a4d7, f* 0.4, cap 2100 s, supported): D0095 acted (35 dropped, 8 opened, 0 refused);
  completes 5.28 (1360 s), then a same-instant loop at 5.281594649757622: sphere 54 touches
  stack sphere 59 again and again at approach 1.5e-16 .. 1.5e-17, each a join (joined 79).
- Rider snaps up to 3.3e-10 now (max_snap; was 3e-14 before the plate landing D0096):
  check where (hand_back of a sphere slightly off the plate?).
- Local jobs: finished processes stay as zombies (/proc/<pid> exists, state Z); wait on the
  result json, not on the pid.

## What's next

0. f* 0.4 loop at 5.2816 (E0110): a touch on a stack sphere at round-off approach rejoins at
   the same instant; find what undoes the join (split/pull right after?) and apply the D0092
   round-off rule to free-to-stack touches.
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
