# Program: sequel

Shared. The agent keeps this current; Chris can edit it any time. Read it
after `DIRECTION.md` at the start of every session.

## Research questions

### RQ1: How should long-lasting contacts be handled?

- Hypothesis: at least one method lets the Gamma = 5, f* = 0.44 case run
  indefinitely without injecting energy and without changing agreement with
  the 1998 reference on the other Figure 1 conditions.
- Falsified if: every method tried either stalls, injects energy, or changes
  Figure 1 agreement beyond the referee's tolerance.
- Options are in `notes/contact-options.md` (Chris, Nov 3), which is the
  reference for them:
  1. position nudge onto the plate (astra): a baseline only; it injects
     m g δ per plate hit and will eventually overlap spheres, so it can at
     best postpone a failure;
  2. stuck state on the plate, captured by e = 0, released when the plate's
     acceleration falls to -g: the plate-frame core of option 4;
  3. elastic window near zero speed (e = 1 below v_el): the cheapest test;
  4. persistent contact after González, Risso & Soto (2009), extended to a
     moving plate, friction and spin: the target;
  5. cutoffs: a trigger, not a method; kept as instrumentation.
- Order: 3 and 1 first as cheap baselines that show whether the stalled
  conditions get further, then 2, then 4.
- Status: open.
  - Nov 6: option 3 (elastic window) tried and does not help.
  - Option 1 (nudge) completes 120 cycles at every stalled condition and
    seed, but fails the survival test at 2D Gamma 5, f* 0.3, depth 10
    (overlap at cycle 163, seed 1), and slows there at the other seeds.
  - Nov 7: option 2 (plate-stick) tried; it gets no further than the
    unmodified engine.
  - Nov 8: instrumented replays (E0026) show plate-stick stalls at a free
    sphere pressed on a stuck one: they collide every 2.5e-12 time units
    without separating. The stall ends in an overlap built from rounding.
  - An option-4 design is proposed for review (D0015).
  - Nov 9: redesigned per instruction (D0016, supersedes D0015): one
    resting state, plate as supporter, modelled on González's drum.
  - Nov 11: D0016 approved. v1 to v3 built and tested on
    `method/persistent-contact`. v3 gets no further than v2 on the
    stalled 2D conditions (E0039, E0040). Every stall examined is a
    sphere rolling on the plate with a sphere pressed on it, which the
    approved rest rule never rests (D0020).
  - Nov 12: the stall needs friction to form. With mu = 0 the unmodified
    engine runs every stalled 2D condition without a slow stretch (E0041).
    With friction, the stalling sphere's collision speeds fall
    geometrically, about a thousand collisions from 1e-2 to 1e-10, where
    the paper's normal restitution alone would need about 1.4e8 (E0043):
    an inelastic collapse through the tangential part of the collision
    law. Once collapsed, the contact stays stalled with friction switched
    off, so the resting state itself is a normal-direction problem.
  - Nov 12: normal rest rule built and piloted without friction (E0042,
    E0045). Any step that removes a fixed fraction of a pressed pair's
    energy makes it collapse; waking and recapturing a resting sphere on
    every hit is such a step.
  - Nov 13: the Nov 12 reading is narrowed (D0030). With friction off the
    engine stalled in 1 of 43 runs on the 2D grid (E0046), so friction
    makes the stall far more likely but is not required. "Collapse through
    the tangential law" is a hypothesis; the run that would test it was
    dropped.
  - Nov 13: option 4 is paused by instruction: no builds, no pilots, and
    nothing built on the plate-only rest rule.
  - Nov 16: two side checks by instruction, with option 4 still paused.
    The region-freezing build with friction off freezes almost nothing
    (E0062). At the seven examined stalls, the sphere on the plate always
    has two touching contacts that do not balance the push on it; the
    balancing side neighbour is close but not touching (E0063). Chris's
    view (Nov 16): freeze only when several contacts balance the force.
  - Nov 17: settled-layer stalls are the same pressed pairs (E0066); one
    stall recorded and pictured (E0067): not a long contact but an
    enormous collision rate.
  - See Current state.

### RQ2: Do the pattern transitions show hysteresis, and where?

- Hypothesis: ramping Gamma up and then down at fixed frequency crosses some
  pattern transitions (e.g. flat to stripes or squares, or hexagons) at
  different Gamma, as seen in experiments.
- Falsified if: with ramps slow enough that the result doesn't depend on ramp
  rate, up and down transitions coincide within run-to-run spread.
- Depends on RQ1 for any condition with long contacts.
- Status: open.
  - Nov 13: plan written, `evidence/phase-diagram-plan.md`, with costs in
    `evidence/phase-diagram-plan-costs.json`. The sweep is not started;
    it waits for Chris.
  - Three engines: nudge (friction), frictionless (unmodified engine,
    mu = 0; a comparison model approved Nov 13 for the phase diagram
    only), and baseline (unmodified engine with friction) where it runs.
  - Pilots (E0050 to E0052): see Current state.
  - Nov 14 (no instruction; fallback): plan revised for the checker's four
    points; recorder, amplitude, transition rule and period rule built and
    tested (E0053 to E0056). The sweep is still not started.

  - Nov 15 (no instruction; fallback): the checker's points on the amplitude
    answered (E0057); two 3D pilots launched (E0058, E0059) and left
    running after the lid was closed at 23:26 (B0005).

  - Nov 16: the staged plan is replaced by a fast pass (instruction of
    Nov 16; plan section 0b): 3D only, ten f\*, Gamma 1.7 to 7.0 and back,
    no transition point, slow loops placed by Chris from the figures. The
    no-friction pass is running (E0060). Both pilots collected (E0058,
    E0059, supported).
  - Nov 17: nudge pass running (E0065), baseline queued (E0068), slow loop
    at f\* 0.44 running (E0064); wider-versus-deeper written.

### RQ3: Does the model produce oscillons?

- Hypothesis: localized, period-two excitations exist in a range of driving
  and layer depth comparable to the experiments.
- Falsified if: a pre-registered search over that range, with an agreed
  definition of an oscillon, finds none.
- Status: open.

### RQ4: Are the results robust to the contact method?

- Any phenomenon from RQ2 or RQ3 is checked with more than one contact method
  from RQ1. Sensitivity is reported as evidence about the method, not hidden.
- Status: open; becomes active once RQ1 has two working candidates.

### RQ0: Is running locally adequate?

- Each session records its run conditions (scheduled versus actual start,
  duration, interruptions such as sleep, CPU-hours used, simulations left
  unfinished or waiting on compute). The checker reviews them.
- Decision point: after two weeks of sessions, Chris decides whether to stay
  local or move to Sterling or Hatteras, from this record.
- Status: open.
  - Nov 17 session: awake on AC, lid open, no sleep events. Ten cores
    full all night; wall clock, not CPU-hours, limits the passes.
  - Nov 16 session: awake on AC, lid open, no sleep events (B0005
    resolved). Nothing else running at the start. Ten cores were not
    enough to finish the night's main job: the ten loops need about two
    days.
  - Nov 15 session: lid closed at 23:26, 19 minutes in (clamshell sleep on
    AC, B0005). Only maintenance wakes after that; two jobs left running.
    Third such night (Nov 8, 9, 15).
  - Nov 14 session: awake on AC, no sleep events; free disk 46 GB at the
    start. Another program (grapenuts) ran 3 to about 10 jobs; load
    average reached 52 around 23:50 with our seven. Timings are upper
    estimates again.
  - Nov 13 session: awake on AC, no sleep events; free disk 47 GB, above
    the floor all session. Six jobs of another program (grapenuts) ran
    throughout, so the session used at most seven cores and its timings
    are upper estimates.
  - Nov 12 session: awake on AC, no sleep events. Free disk was under the
    40 GB floor all session and under the 25 GB hard floor from 23:38
    (swap from other jobs on the Mac, B0004), so most of the night's
    queued runs could not launch.
  - Nov 11 session: awake on AC throughout, no sleep events; the queues
    lost to the Nov 11 00:05 kernel panic were restarted at 23:16.
  - Nov 8: the Mac rebooted at 23:23, after the scheduled 23:00 start. The
    session started at 23:26. No jobs were lost: both were already done.
  - Nov 8: clamshell sleep (lid closed) at 23:57 paused the session and its
    jobs. Blocker B0002.
  - Nov 9: clamshell sleep again at 23:23, fifteen minutes in; jobs got
    about 25 CPU-minutes each by 02:25. B0002 still open.
  - Nov 10: awake on AC all session. Another job on the Mac drove swap up
    and free disk under the floor from 23:11; launches held (B0003).

## Approaches under consideration

The five options in `notes/contact-options.md`.

### Option 3, elastic window

- Branches: `method/elastic-window` (v_el = 0.01) and `-v003` (v_el = 0.03).
- Not a candidate (Nov 6): no better survival than the unmodified engine.

### Option 1, position nudge

- Branch: `method/nudge` (b608fef).
- The only method that gets through the stalled conditions:
  - 120 cycles at all 8 stalled 2D conditions, and at 3D Gamma 5 at seeds
    1 to 3;
  - 1000 cycles at 7 of 8 (seed 1).
- Where it fails or slows:
  - Overlap at 2D Gamma 5, f* 0.3, depth 10 (cycle 163, seed 1). Seeds 2
    and 3 there completed 1000 cycles but spent 47% and 13% of their CPU in
    slow stretches (E0025).
  - At f* 0.3, depth 15: seed 1 spent 71% of its CPU in slow stretches;
    seeds 2 and 3 none. The f* 0.5, depth 15, seed 2 run had none either.
- Audit failures are almost all energy losses, with two gains (+9.2e-8 and
  +1.4e-8 of throughput; E0023, E0025).
- Bulk physics passes wherever a baseline exists:
  - 2D shallow and deep layers, against the unmodified engine and the C
    code;
  - 2D L = 400 at three conditions, 3 seeds each (Nov 7);
  - 3D case g, provisionally.
- Running (E0028): the referee's 3D Gamma 5 case to 1000 cycles at seeds 2
  to 5.

### Option 2, plate-stick

- Branches: `method/plate-stick` (3900896, v_stick 1e-4) and
  `method/plate-stick-v1e-3` for the pilot.
- Built and tested Nov 7: frozen tests pass, capture, ride and release
  match the closed form, and the energy books balance to round-off.
- Fails survival: 23 of 24 runs overlap where the unmodified engine slows
  (and sometimes clears).
- Every failure is a free sphere pressed at an angle on a stuck one. E0026
  replayed five failures:
  - the pair collides 2.6 to 17 million times without separating;
  - each collision is followed by recapture of the lower sphere, so the
    next collision comes two pressed-contact steps later (2.5e-12 time
    units);
  - rounding of about 1e-15 D per step builds 99.89% to 100% of the 2e-8
    overlap.
- The pressed-contact rule is recorded as D0014.
- Captured spheres are almost always freed by collisions before their
  release phase. One release was seen, in the v_stick 1e-3 3D run.
- Where baselines exist it barely captures, so its bulk passes are
  uninformative.
- Not a candidate as it stands. The pair needs a resting state of its own:
  transitive sticking (a model change Chris ruled out by default) or
  option 4.

### Option 4, persistent contact

- Design: `evidence/D0016-option4-redesign.md` (D0016), approved Nov 11
  with all five choices. A slow hit on a resting sphere is a plate-law
  collision with the impulse along the line of centres.
- Branch `method/persistent-contact` (worktree
  `sequel-data/worktrees/persistent-contact`):
  - v1 094056e: settings and bookkeeping. With the method off it is
    bit-identical to main.
  - v2 c52079f: resting on the plate.
  - v3 e0f8a5f: resting on resting spheres, one supporter, cascade wake.
  - 158add1: explicit slow-hit test.
  - Tests: 74 frozen, 133 branch, plus 1 strict xfail for the rolling
    limitation (`evidence/D0016-build-v1-v3.json`). Details: D0019.
- Pilots, 7 stalled 2D conditions at seed 1 (E0038, E0039, E0040):
  - v2 stalls like plate-stick.
  - v3 completes the same cycles as v2 at 6 of 7 conditions with twice
    the CPU, and overlaps once.
  - Of the five E0026 starts, v3 gets past plate-stick's failure cycle
    in 1.
- Diagnosis (4 stalls examined event by event): a free sphere rolls on
  the plate without slip (speed 0.04 to 1.06), with one sphere pressed
  on it. No sphere is resting at the time. Under the approved rule a
  sphere rests only when its full speed is below v_sleep, which a
  rolling sphere never is.
- Exploratory `method/persistent-contact-roll` (c3dd7b2, `plate_rest =
  roll`): resting on the plate keeps horizontal velocity and spin. The
  lone rolling sphere is fixed, but a layer stalls at a sphere pressed
  on a rolling resting one. Question for Chris (D0020).
- Pinned worktrees for the pilots: `persistent-contact-v2`, `-v3`.
- Nov 12, normal rest rule, `method/persistent-contact-normal` (setting
  `rest_rule = normal`; the default stays D0016's `full`; D0022):
  - 9923d8a: rest on the plate when the vertical speed relative to the
    plate is below v_sleep; horizontal velocity and spin are kept, so the
    sphere slides. Nothing rests on a sphere. Every hit on a resting
    sphere wakes it (`normal_hit = wake`).
  - 8b78fec: `normal_hit = held`: a slow hit from above is one collision
    in which the plate holds the resting sphere vertically and it recoils
    horizontally. Frictionless only.
  - Tests: 74 frozen, 148 branch, 1 skipped, 1 strict xfail.
  - Pinned pilot branches (defaults mu = 0 and the rule on; not for
    merging): `method/persistent-contact-normal-mu0` (b40bfd4),
    `method/persistent-contact-normal-held-mu0` (cba8c0c), and
    `method/mu0-unmodified` (765c1f0) for the frictionless baseline.
  - Proposal for rest on a sphere (D0024, for Chris):
    `evidence/D0024-rest-on-sphere-proposal.md`.
- **Paused (Nov 13 instruction).** No builds, no pilots; do not build on
  the plate-only rest rule. The step that was next, normal-only rest with
  friction, was not started. E0045 (held-hit pilot and sweep) and the
  rest of E0042's sweep were dropped with the friction diagnostics
  (D0031).

## Current state

### Nov 17 findings

Instruction of Nov 17 (six items). One seed everywhere; nothing below is a
physical result. Session summary: `sessions/2026-11-17.json`.

- **CPU-hours are no longer a reason to trim** (Chris, Nov 17: 2000 a week,
  100 per run). Limits that hold: ten cores, disk, memory.
- **No-friction fast pass (E0060):** 8 of 10 loops complete; f\* 0.30 and
  0.27 on the way down. No slow stretch or audit failure in 1980 steps. At
  the first onset the way down stays above the way up over a range that
  widens as f\* falls (none from 0.50 up; 2.15 to 2.3 at 0.44; 1.9 to 2.1
  at 0.38). Every figure redrawn with the half-box and whole-box rings
  (D0043); structure the size of the box dominates at many Gamma above 4.
  At f\* 0.84, Gamma 4.5 (way up only) and f\* 0.50, Gamma 4.0 it is part of
  the layer bouncing on alternate cycles, with a front.
- **Slow loop (E0064, running):** f\* 0.44, 1.9 to 2.6 and back, 100 cycles
  a step. 10 of 29 steps at the summary; way up above the fast one from
  2.15. Rebuild with `tools/e0064_evidence.py`.
- **Nudge pass (E0065, running):** Chris's friction loop (3.0 down to the
  half-hour floor, up to 7.0, back). Queue `runs/q-1117.spec` via
  `tools/qx6.sh`, 95 CPU-hours per loop. Six running at the summary.
- **Baseline pass (E0068, queued):** behind the nudge loops
  (`runs/q-1117b.spec`, started by a waiter on `q-1117.log`), half-push
  start (`tools/baseline_loop.sh`). Priced at most 301 CPU-hours.
- **Wider versus deeper:** `evidence/wider-vs-deeper.md`. Wider is the
  cheaper step and opens low f\*; deeper in the same box closes them.
- **Settled-layer stalls (E0066):** same picture as first-landing stalls;
  balancing neighbour within 0.01 D at 2 of 7.
- **One stall pictured (E0067):** `evidence/E0067-figures/`. 7.8 million
  collisions in 7.5e-5 of a period; the contact lasts 0.016 of a period,
  shorter than some ordinary contacts; the extreme is the collision rate.
- **Tools:** branch `tools/phase-diagram` (bf6176d and after).

### Nov 16 findings

Instruction of Nov 16 (seven items). One seed everywhere; nothing below is
a physical result.

- **Fast pass, no friction (E0060, running).** Ten loops in the paper's 3D
  layer (N 60000, L 100), f\* 0.27 to 0.84 (D0039), Gamma 1.7 to 7.0 and
  back, steps of 0.05, 25 cycles per step.
  - Eight run at a time; f\* 0.30 and 0.27 are queued
    (`runs/fastpass-1116b.spec`, `tools/qx5.sh`). Each loop stops itself at
    38 CPU-hours and keeps checkpoints at Gamma multiples of 0.5.
  - Progress, figures and per-step amplitudes: rebuild with
    `tools/fastpass_evidence.py` (writes `evidence/E0060-results.json` and
    `evidence/fastpass-figures/`). The session summary has the count at
    the time it was written.
  - No slow stretch, audit failure or incomplete step so far.
  - Cost: about 154 CPU-hours for the ten, not the 80 registered
    (`evidence/phase-diagram-plan-costs-v3.json`; the first hour suggested
    190).
  - On the way up (680 of 2130 steps): f\* 0.33 to 0.44 have a strong
    pattern from the first onset (A 0.6 to 1.4 D). f\* 0.50 to 0.84 have a
    weak first pattern (A at most 0.09 to 0.15 D) that fades by Gamma 3.0
    to 4.0, then a sharp second rise to 0.65 to 1.1 D starting at Gamma
    4.1 (f\* 0.50) to 5.3 (f\* 0.84). Two loops have turned at 7.0. The
    fields have not been looked at; the patterns are not named.
- **No transition point** is computed. Deliverable: amplitude against
  Gamma, both branches, per frequency and model (`tools/loop_figure.py`,
  SVG).
- **Pilots collected.**
  - E0058 (no friction, f\* 0.44, Gamma 1.7 to 2.7 and back): supported.
    Flat level 0.025 D; branches apart between Gamma 2.05 and 2.4 at the
    fast rate (0.10 D up against 0.34 D down at 2.2). 3.1 CPU-hours.
  - E0059 (nudge descent from 3.0 at f\* 0.44): supported. Floor 2.25 at
    half a CPU-hour per step; cost 15 s per cycle at 3.0, 55 at 2.25;
    pattern gone from 2.4 down.
- **Nudge and baseline loops: none run.** Nudge loops priced at 16 to 49
  CPU-hours each, about 300 for ten; f\* 0.33, 0.30, 0.27 are at or over
  the per-run limit. Two were queued and withdrawn before starting
  (E0061 abandoned, D0041) when the no-friction pass looked like taking
  the week to 89% of the CPU budget; on the later price it is about 80%.
- **Freezing with friction off (E0062, falsified on one prediction).**
  Region-freezing build pinned as `method/persistent-contact-mu0`
  (8372586), 2D grid, seed 1, 120 cycles, four thresholds.
  - v_sleep 1e-4: one rest in 12 runs; 11 runs identical to the baseline.
  - 1e-3: 134 rests. 1e-2: 124,741. 3e-2 (v_wakeup also 3e-2): 180,250.
  - At most 5 (1e-2) and 17 (3e-2) of 1500 spheres resting at a recorded
    frame; largest region 3 and 6; only while the plate pushes up. 97%
    and 94% of rests end at the next hit.
  - No audit failure. Bulk passes except one run at 3e-2.
  - Runs fail as the threshold rises: 1 of 12 at 1e-2, 5 of 12 at 3e-2.
- **Stalls against the multi-contact criterion (E0063, falsified on one
  prediction).** Seven E0043 stalls replayed and read
  (`tools/stall_neighbours.py`).
  - Six are a sphere on the plate with one pressed on it. The lower one
    touches the plate and the presser only; those never balance the push.
  - A balancing neighbour is within 1e-3 D at 1 of 6, 1e-2 D at 4, 1e-1 D
    at 6; due in 0.003 to 0.18 time units at 4, not approaching at 2.
  - The spheres are not slow (0.03 to 1.3); only the contact closing
    speeds are (1e-11 to 1e-10). A contact that has just bounced has no
    scheduled collision.
  - The seventh is one slow sphere held by two above it: three touching,
    balanced contacts.
- **Plan** revised (section 0b): fast pass, prices, deeper layers next
  with their cost.
- **Budget:** see the session summary. Past 50% once the loops' CPU is
  counted; about 80% when they finish.
- **Tools:** `ramp.py` (total CPU cap, checkpoint pruning), `qx5.sh`,
  `loop_figure.py`, `fastpass_evidence.py`, `freeze_recorder.py`,
  `e0062_evidence.py`, `stall_neighbours.py`, `e0063_evidence.py`,
  `plan_costs_v3.py`, `session_1116.py`. Branch `tools/phase-diagram`
  (c738269 and after).

### Nov 15 findings

No instruction; fallback, default applied (D0037). The sweep is not started.

- **Lid closed at 23:26 (B0005).** The session and both pilots ran only in
  maintenance wakes after that. Records were written at the first wake.
- **Checker's points on the amplitude (E0057, falsified narrowly;
  `evidence/E0057-results.json`; plan section 0a):**
  - The noise-corrected amplitude A is no steadier than a snapshot: up and
    down branches differ by 7.2% of its range on the 100-cycle loop
    (snapshots 7.0%, the dropped plain amplitude 3.6%).
  - With a wider band, a narrower band, and the floor at 0.05 D or 0.2 D,
    45 of 48 frictionless f* 0.3 transition points move by one step or
    less, 3 by two steps (one loop). None appears or disappears.
  - A single loop at 25 cycles per step cannot show a width under about
    0.15 in Gamma. At 100 cycles per step this is not measured.
  - A baseline started from the nudge's state is not used for engine
    comparisons (plan, section 0a).
- **3D pilots, running** (`runs/active.jsonl`; evidence files are interim):
  - E0058: frictionless loop, N 60000, f* 0.44, Gamma 1.7 to 2.7 and back.
    2 of 41 steps. Flat-layer A is 0.025 D at Gamma 1.7 and 1.75 (the
    floor is 0.1 D). Cost there 18 to 21 CPU-seconds per cycle.
  - E0059: nudge down-ramp from its 1000-cycle Gamma 3.0 state, cap 0.5
    CPU-hours per step, ends at the first step that fails. 3 steps done
    (3.0, 2.95), 14.6 and 15.0 CPU-seconds per cycle.
  - Rebuild the evidence with `tools/e0058_59_evidence.py` when they end,
    then record the outcomes.
- **Tools:** `loop_analysis.py` takes the band's upper edge as a parameter;
  `e0057_variants.py`, `e0058_59_evidence.py`, `e0059_run.sh`. Branch
  `tools/phase-diagram` (36be34e and after). Queue spec `all-1115.spec`.

### Nov 14 findings

No instruction for the night; the fallback applies. The sweep was not
started (D0033). Everything below is from one seed per condition unless
said, and none of it is a physical result.

- **Plan revised** (`evidence/phase-diagram-plan.md`, section 0; D0034) for
  the checker's four points:
  - the nudge's 3D diagram is spelled out and a nudge scan above onset is
    added (stage I, 74 CPU-hours, upper estimate);
  - stage A (2D, depths 5 and 10) is repriced from measured ramps with the
    baseline included: 64 CPU-hours, not 22; the whole plan about 525;
  - the budget is 400 CPU-hours per seven days (`budgets.yaml`);
  - the transition point is redefined so it applies to an engine that
    turns with few flat holds.
- **Field recorder built** (`tools/field_recorder.py`, E0053). It saves the
  height field's spectrum at every referee frame. All 147 steps of the
  three Nov 13 frictionless ramps, rerun with it, end bit-identical.
- **Order parameter** (D0035): the band amplitude A with the white part of
  the spectrum removed.
  - The plain band amplitude I registered separates flat from patterned by
    a factor of 7.9, but is only about twice as smooth as a snapshot (0.509
    against the 0.5 I required: E0053 recorded falsified).
  - It also rises with Gamma from shot noise where there is no pattern, so
    it was replaced (E0055).
- **Transition rule as code** (`tools/loop_analysis.py`): flat level from
  the lowest five holds (median, robust scatter); patterned if above it by
  max(5 scatter, 0.1 D), three steps running.
- **Rule tested on a seed it was not set on** (E0056, seed 11): 4 of 5
  predictions held; recorded falsified.
  - Frictionless: transitions within 0.05 of seed 1 at depth 5 and depth
    10, f* 0.3; none at depth 5, f* 0.5.
  - Nudge, depth 10, f* 0.3: 2.43 on the way down at both seeds.
  - Missed: nudge, depth 5, f* 0.3. Predicted 2.15 to 2.40 from the Nov 13
    snapshot amplitude; the rule gives 2.53. The snapshot amplitude tracks
    the layer thinning between 2.5 and 2.3, with no spectral peak.
- **Temporal-period rule** (E0054): 16 of 16 on our own case-b and case-g
  runs, which it was not chosen on. Two conditions, both patterned.
- **Engines with friction on a down ramp** (E0055, E0056; 2D, 25 cycles
  per step):
  - Nudge floors: 2.05 to 2.30. Its pattern ends 0.13 to 0.43 above the
    floor (least at depth 10, f* 0.3), so its loops have 6 to 17 flat
    holds. Cost per cycle rises 8 to 110 times toward the floor.
  - Baseline floors: 2.2 to 2.35, and 2.85 at depth 10, f* 0.3, where it
    cannot start from rest at Gamma 3 and stops while still patterned.
  - A step that just completes going down may not complete going up;
    `ramp.py` now turns at the first step above half its CPU cap.
- **2D at f* 0.5**: no pattern between Gamma 1.8 and 3.0 at depth 5 with
  any engine; a weak, gradual one at depth 10.
- **Tools on a branch**: `tools/phase-diagram` (worktree
  `sequel-data/worktrees/tools-phase-diagram`), with tests.
- **Budget:** 5.1 CPU-hours tonight (E0053 0.11, E0054 0.52, E0055 2.78,
  E0056 1.71). See the session summary for the weekly count.
- **Disk:** 46 GB free at the start, program data 3.5 of 15 GB.

### Nov 13 findings

- **Phase-diagram plan written** (`evidence/phase-diagram-plan.md`). Its
  main points:
  - 3D at L 100, N 60000, six f* values, Gamma covered by ramps and by
    holds at the seven Figure 1 conditions; 2D on the referee's grid in
    wider boxes.
  - Hysteresis by stepwise ramps (`tools/ramp.py`), at the experimental
    rate (0.002 in Gamma per cycle) and slower, with four checks against
    a ramp that is too fast; the decisive one is two long holds at one
    Gamma from the two branches.
  - Cost about 410 CPU-hours for everything; 22 for the first stage (2D,
    depths 5 and 10).
- **No-friction baseline runs (E0046, E0049).**
  - 38 of 39 runs completed with no slow stretch: every 1020-cycle run
    (12 grid points, seed 1), the 3D Gamma 5 case at three seeds (300
    cycles, 90 CPU-seconds each), and the five grid points not run
    before.
  - One stalled: 2D Gamma 5, f* 0.3, depth 15, seed 3, in cycle 10 at
    phase 0.902, with 8.5e8 collisions slower than 1e-10 before its CPU
    cap. Not yet examined event by event.
  - The frictionless engine now has three seeds and a ten-block
    1020-cycle baseline at all 12 points of the 2D grid
    (`evidence/E0046-E0049-grid.json`).
- **Cost and feasibility pilot (E0050), Gamma 2 to 7, one seed, 30 to 60
  cycles.**
  - Frictionless: 29 of 29 runs complete, no slow stretch.
  - Nudge: 25 of 28. It stops at its CPU cap at 2D Gamma 2.0 and 2.5
    (f* 0.3, depth 10) and at 3D Gamma 2.2 (45 s per cycle at N 15000,
    against 7 at Gamma 3).
  - Baseline: 15 of 28. Nothing at Gamma 2.0 to 2.2.
  - 3D cost per particle per cycle at Gamma 3, f* 0.44: frictionless
    0.11 ms, nudge and baseline 0.32 ms. The same at L 50 and L 100.
- **Ramp pilot (E0052), 2D, f* 0.3, depth 5, L 200, one seed.**
  - `tools/ramp.py` drives the referee step by step; an unchanged-Gamma
    step is bit-identical to a continuous run; no audit failure.
  - Frictionless: three complete loops over Gamma 1.8 to 3.0. Amplitude
    rises from about Gamma 2.0. No loop at 25 or 100 cycles per step.
  - With friction, down from 3.0: the nudge reaches 2.15 and stops at
    2.1 (CPU cap); the baseline reaches 2.25 and overlaps at 2.2. The
    pattern has died away by about 2.25 to 2.3, so both stop in the flat
    state just below it. Their layer thickness agrees within 0.075 at all
    16 common steps.
  - Not a result: one seed, snapshot amplitudes.
- **Pattern identifier (E0051), `tools/pattern_id.py`.**
  - On the seven labelled Figure 1 reference runs: planform right 7 of 7,
    temporal period 6 of 7 (thresholds set beforehand).
  - On our own 1000-cycle case-b runs: 4 of 8 called stripes. Contrast
    and wavelength are the same in all eight; the stripes still have
    defects. Registered rule failed; planform needs Chris's eye or
    longer runs.
- **Budget:** 242 of 400 CPU-hours by the runs' own records
  (`evidence/budget-2026-11-13.json`), 61%. Past 50%, below 80%.
- **Disk:** 47 GB free at the start, 46 at the end; B0004 resolved.

### Nov 12 findings

Narrowed on Nov 13 (D0030): read the first item below with the RQ1 status
note. Friction is not required for the stall; the tangential-law mechanism
is a hypothesis.

- **The stall needs friction to form (E0041, E0043).**
  - With mu = 0 the unmodified engine completed 120 cycles at all seven
    stalled 2D conditions (seed 1) with no slow stretch and not one
    collision slower than 1e-10 (`evidence/E0041-results.json`).
  - With friction, at the first stall of each condition the picture is the
    same: a sphere on the plate, normal speed relative to the plate about
    1e-11, rolling without slip, with a second sphere pressed on it 22 to
    61 degrees from vertical. The Nov 11 "speed relative to plate" was
    wrong, as Chris suspected: the tool took velocities at the last frame
    time, not the event time. `tools/mu_switch.py` replaces it.
  - On the way in, the stalling sphere's collision speed falls from 1e-2
    to 1e-10 in 306 to 2097 collisions (four conditions traced), a factor
    of 0.95 to 0.995 per collision. The paper's normal restitution alone
    would take about 1.4e8.
  - Friction switched off five chunks (500 N events) before the stall: no
    stall in that cycle, 4 of 4. Friction switched off after the stall has
    formed: still stalled at 5 of 7 (one clears, one partly).
  - Reading: the paper's e(v) goes to 1 at low speed, which protects the
    normal direction from inelastic collapse; the tangential law has no
    such limit, so a pressed, oblique pair collapses through it. The
    collapsed contact then needs no friction to stay stalled.
  - Not yet done because free disk was under the floor (B0004): the last
    three traces, seeds 2 and 3, 1020 cycles, the 3D case (E0046), the
    friction scan (E0047), and which part of the tangential law does it
    (E0048). All queued in `runs/all-1112c.spec`.
- **Normal rest rule, frictionless pilots (E0042, E0045).** Built as the
  Nov 12 instruction asked (see Option 4).
  - Because the frictionless engine does not stall, these pilots cannot
    test survival. They test whether the rule acts and what it changes.
  - `normal_hit = wake`, v_sleep 1e-4: completes all seven conditions;
    0 to 686 sleeps per run, every one ended by a hit, none by release.
    No slow hits by construction.
  - Same rule at v_sleep 1e-3 and above: collapses. Six sweep runs done:
    one completed, one overlapped in cycle 6 after 1.04e8 sleep/wake
    pairs, four stopped at their CPU cap in cycle 0 to 2 with 3e8 to 5e8
    (`evidence/E0042-results.json`). The rule creates a stall where the
    unmodified engine has none: each wake-and-recapture is a collision
    with zero restitution.
  - `normal_hit = held` ran the failing condition for 12 cycles at v_sleep
    1e-3, 1e-2 and 3e-2 with ordinary event counts (trial, in the branch
    tests). Its pilot (E0045) is queued.
- **Accumulator fix merged and checked (D0021, D0025, E0044).** Reruns of
  three runs with the fix are bit-identical to the originals in every
  recorded sample, and every audit-failing cycle goes away: nudge 46 of
  46 (Gamma 5, f* 0.5, depth 15, seed 2), unmodified 2 of 2 (Gamma 3.5,
  f* 0.3, depth 10, seed 1; both were +1e-6 in cycles with about a
  million events per particle), and nudge 130 of 130 (Gamma 5, f* 0.3, depth 10, seed 3). Worst
  residual after the fix: 1.7e-11. So the audit failures of both engines were bookkeeping
  round-off, of either sign. This also bears on the note of Nov 6 in
  `notes/contact-options.md` that resting contact simulated as many
  collisions drifts energy: that drift has the same source.
- **Numba cache hazard.** A test that loads `main`'s engine under a
  second module name (`granular_main`) writes cache entries that break
  the next plain import of `granular` if it is the first to compile
  after a source change. It made a frozen test fail after the merge;
  clearing `granular/__pycache__/*.nb*` fixes it. The branch tests on
  `method/persistent-contact*` still load `main` that way.
- **Engine comparison, final (E0031, E0034).** 2D, L 100, Gamma 5, seeds 1
  to 3: unmodified 0 of 18 runs completed 1000 cycles, nudge 17 of 18.
  E0031 is recorded falsified on its second clause (positive residuals
  per 1000 cycles, at conditions where the unmodified engine ran almost
  no cycles); E0044 shows those residuals were round-off.
- **Nudge at case b (E0037, E0036).** Passes the bulk rule at all four
  seeds from the half-push start (largest deviation 2.69 block SDs,
  threshold 4.24 for 7 blocks) and from the C state (1.06, threshold
  3.62). Both engines ran 1000 cycles with no slow stretch.
- **Budget:** 238 CPU-hours spent by the runs' own records
  (`tools/budget.py`, D0026; `evidence/budget-2026-11-12.json`), 60% of
  400. Past the 50% mark, below 80%.
- **Disk (B0004):** free disk was 26 GB at the start and 21 GB from
  23:38 on, from swap used by other jobs on the Mac. Launches held.

### Nov 11 findings

- **Option four built (v1 to v3) and piloted.** See the RQ1 section and
  Option 4. Main result: the remaining stall is a rolling sphere on the
  plate with a sphere pressed on it (E0039, E0040, D0020).
- **Nudge positive-residual cycles (E0031, checker item):** all four
  replay bit for bit. The nudge's own lift is at most 3.1e-13 of
  throughput, and no collision gains energy. Cause found: round-off in
  the engine's run-long energy totals. In one collision-heavy window,
  the residual is 2.1e-6 as run and 1.4e-11 with the totals started
  from zero, on the same trajectory
  (`evidence/E0031-positive-residuals.json`). Fix on
  `fix/energy-accumulators` (901a971): terms summed per call from zero,
  trajectories unchanged. Merge proposed (D0021). Until it is merged,
  audit failures in chatter cycles may be bookkeeping, for either engine.
- **Engine comparison, interim (E0031-interim-3):** in 2D at Gamma 5,
  L 100, the unmodified engine completed 0 of 15 ended 1000-cycle runs
  and the nudge 16 of 17. Still running: E0031's last unmodified runs,
  E0034 and the 3D nudge runs.
- **Case-b main baseline (E0037) registered and queued**, from the
  half-push start, seeds 1 to 4, both engines, 1000 cycles, 8 CPU-hour
  cap, burn-in fixed at 300 cycles (D0018). E0036 (C state) is kept as
  a cross-check.
- **Pass rule:** kept for 100-cycle windows. Whole runs are compared
  only across several starts. The noise study's estimate (effective
  threshold 3.43 rather than 3.61) is a point estimate, not a bound.
- **Queue (D0018):** `tools/qx4.sh`, 10 live in total, holds below
  25.5 GB free (hard floor 25 GB, Nov 11 instruction). Main queue spec:
  `runs/all-1111.rest.spec`.

### Nov 10 findings

- **Noise study, final (E0030, inconclusive):** all 48 runs done. The Nov 9
  interim reading is withdrawn, as the checker asked.
  - Using every 100-cycle block (ANOVA), starts differ by more than blocks
    predict only in horizontal kinetic energy and temperature at f* 0.3:
    between-start variance about twice the prediction at L 100 and L 400,
    not at L 200. Nothing at f* 0.5 (no pattern there).
  - No trend with width. Wavelength counts wander but agree between starts
    (7 at L 200 and 14 at L 400 over each start's last 1000 cycles).
  - Pass rule: the extra variance widens a judged 100-cycle deviation by at
    most 5.1%, so 3.61 acts as no less than 3.43. Recommendation: keep it;
    compare whole runs only across several starts.
- **Case-b pilot, final (E0032, supported):** an upward push of 1/2 or 3/4
  of the plate's peak speed gets the unmodified engine through 30 cycles at
  4 of 4 seeds (1 of 4 with 1/4). From the C state both engines ran 120
  cycles cleanly. Evidence file written, with the converter check
  recomputed (mean height within 0.38%, not the 0.2% stated Nov 9).
- **Engine comparison, interim (E0031):** 42 of 57 runs launched.
  - Unmodified engine at Gamma 5 (2D, L 100): no run has completed 1000
    cycles at any depth or frequency.
  - Nudge: every 1000-cycle run completed except the known overlap.
  - Audit failures: unmodified nearly all gains (13 of 15 failing cycles),
    nudge nearly all losses (664 of 668), counted over all run folders.
  - Every slow stretch of the unmodified engine starts in phase 0.825 to
    0.997, or just after phase 0 (31 of 1028 episodes): while the plate
    pushes upward, before release. Table: `evidence/E0031-interim-2.json`.
- **Disk (B0003):** free disk fell from 43 GB to below the 40 GB floor by
  23:11, from swap by another job on the Mac (not the program: sequel-data
  is 2.6 GB). No launches since. Held: 15 E0031 runs, 5 E0034 runs, 2 E0036
  runs.
- **Queue (D0017):** `tools/qx3.sh` caps live jobs across all experiments
  (8) and holds launches while free disk is under 40.5 GB.

### Nov 9 findings

- **Case-g baseline (E0029):** the unmodified engine completed 1020 cycles
  at seed 4 (1 of 5 seeds), with 3 positive residuals and 1 momentum-only
  audit failure. Seeds 3 and 5 overlapped.
- **Nudge vs case-g baseline (E0033):** all 3 seeds pass, but close to the
  threshold in height and horizontal energy. The baseline drifts for about
  300 cycles, and over the same window (cycles 20 to 120) the engines
  agree. The referee's 20-cycle settling is too short at case g.
- **Case b from the C state (E0032):** `tools/caseb_start.py` converts the
  C restart (cycle 2700).
- **E0027 superseded by E0035 (inconclusive):** registration departures stated; some
  slow within-run trends at L 400.
- Terminology from the Nov 9 instruction: "positive residual" for a
  failing cycle whose energy residual is positive. The audit's
  energy_gains counter counts collisions that gain energy.

### The engine on `main`

- It is the hardened import described in `README.md`. It fails loudly on
  physical violations, matches an all-pairs reference, and restarts bit for
  bit.
- Since Nov 12 it includes the accumulator fix (merge 997eb49, D0021,
  D0025): energy terms are summed per call from zero. Trajectories are
  unchanged. Not pushed.
- It stalls or overlaps in lasting contact:
  - at 3D Figure 1 case b, at the first landing, at all 4 seeds tried with
    the default start;
  - at case g: overlap at cycle 567 at seed 2; seed 1 ran 586 cycles to its
    CPU cap with 5 audit-failing cycles, all energy gains.
- Running (E0029): seeds 3 to 5 at case g, toward a 1020-cycle baseline.

### Branches and tests

- Contact methods are on branches with worktrees under
  `sequel-data/worktrees/`; merging needs Chris.
- The frozen referee tests pass on every branch (74 each), run with the
  branch's engine imported (Nov 7). They pass on `main` (Nov 8).

### Nov 8 findings

- **Plate-stick's overlap is a stall plus rounding (E0026).** In five
  replayed failures, every pressed-contact step belonged to the failing
  pair, and the grazing step never fired.
- **Wide 2D boxes (E0027, existing L = 400 baselines):**
  - Layers decorrelate within 5 to 13 cycles, and block standard deviations
    don't grow with block length.
  - The referee's drift test flags about a fifth of quantities even in
    cycles 520 to 1020, at both widths. The frequent flags come from
    autocorrelated per-period means, not unsettled layers.
  - At Gamma 3.5, f* 0.3, depth 5, the five seeds' 1000-cycle means differ
    by about twice what within-run blocks predict. This is not explained by
    the final wavelength count. It makes the pass rule stricter than
    intended there (effectively about 3.1 rather than 3.61 standard
    deviations).
- **Nudge depth-ten continuations (E0025):** both seeds completed 1000
  cycles, with long slow stretches.

### Nov 7 findings

- **Wider 2D boxes (L = 400):**
  - They hold 13 to 15 pattern wavelengths.
  - Over the judged window, run-to-run spread matches block spread, but so
    it did at L = 100 in the same pilot.
  - The unmodified engine fails more first landings at L = 400.
  - The C code aborts at two L = 400 conditions, so those have no baseline
    at this width.
- **Case-b baseline:** no start (default, hot, hot-dilute, cold-dilute) gets
  the unmodified engine through case b. Every failure is at phase 0.87 to
  0.95 (E0019).
- **Audit census:** E0023 (the nudge's counts there are now superseded by
  E0025).

### Tools (not in git, under `sequel-data/runs/tools/`)

- Launching: `launch.sh`, `q.sh` (queue under the core limit),
  `soft_start.py`.
- Replaying failures: `overlap_repro.py`, `stuck_overlap_replay.py`,
  `replay_pair.py`.
- Instrumented plate-stick replays: `e0026_replay_watch*.py` and
  `e0026_counters.patch`.
- Analysis: `spread.py`, `e0027_blocks.py`, `e0027_flags.py`,
  `judge_set.py`, `audit_census.py`, `ev_runs.py`.
- Status: `st.sh`, `watch.py`.

### Referee findings to bring to Chris

These are findings, not edits; the referee is his.

- `long_contact.py` has no way to set the initial condition. Soft starts go
  through a cycle-0 checkpoint and `--resume` (D0011). An option would be
  cleaner.
- Checkpoints are skipped during slow episodes, so hours of work can be
  lost to a kill. In E0008 at depth ten, the last checkpoint was four hours
  before the overlap. A mid-cycle checkpoint can't fix this without
  breaking bit-for-bit replay, because `save_checkpoint` rebuilds and
  re-sorts the state.
- The 1998 C code does not give 1020-cycle baselines at several 2D
  conditions (E0009), and none at two L = 400 conditions (E0024).
- `bulk.py`'s drift test treats per-period means as independent. With
  correlation times of 5 to 13 cycles, it flags about 20% of quantities in
  settled layers instead of 5% (E0027).

## Next

- **Collect the running loops.** Check `runs/active.jsonl`. E0060 (f\* 0.30,
  0.27), E0064 (slow loop), E0065 (nudge, queue `q-1117.spec` via
  `tools/qx6.sh`), then E0068 (baseline, `q-1117b.spec`, started by a
  waiter once `q-1117.log` says the first queue is done). A stopped loop
  resumes by rerunning its spec line (finished steps are skipped).
  Rebuild with `tools/fastpass_evidence.py` and `tools/e0064_evidence.py`;
  record outcomes against the registrations when loops end.
- **CPU-hours do not limit runs** (2000 a week, 100 per run); cores, disk
  and memory do.
- **Bigger box** (Chris: the next step): measurements listed in
  `evidence/wider-vs-deeper.md`; order is a question to Chris (default:
  after the nudge loops, before the baseline loops).
- **Slow loops** beyond E0064 are Chris's to place.
- **Deeper layers** (plan section 0b): a 20-cycle hold at depth 10.84
  first, then onset-only loops at four f\*. Wait for Chris.
- Option 4 stays paused. No design work on the multi-contact criterion
  unless asked.
- The frictionless stall (E0046, Gamma 5, f* 0.3, depth 15, seed 3) has
  not been examined. `tools/mu_switch.py` and `tools/collapse_trace.py`
  would do it. Proposed, not started: the Nov 13 instruction dropped the
  friction diagnostics.
- Option 4 is paused. E0045, E0047, E0048 and the unrun parts of E0042
  and E0043 are dropped (D0031); `runs/all-1112c.spec` is not to be
  restarted.
- Chris to decide: push `main` (merge 997eb49 and test commit 0b15165
  are local only, D0025).
- The intrinsic sweep (when a candidate survives) includes v_wakeup =
  v_sleep.
- Tools added Nov 14: `field_recorder.py`, `loop_analysis.py`,
  `loops_table.py`, `period_rule.py`, `continue_run.py`,
  `plan_costs_v2.py`, `e0053_identity.py`, `e0053_54_evidence.py`,
  `e0055_56_evidence.py`. Queue specs: `E0053.spec`, `all-1114.spec`,
  `all-1114b.spec`, `E0055b.spec`, `E0055d.spec`.
- Tools added Nov 13: `ramp.py`, `ramp_table.py`, `pattern_id.py`,
  `run_table.py`, `file_records.py`, `e0046_50_evidence.py`,
  `plan_costs.py`. Queue specs: `mu0-1113.spec`, `E0050.spec`,
  `E0052.spec`.
- Tools added Nov 12: `lc_counters.py`, `mu_switch.py`,
  `collapse_trace.py`, `tangential_variants.py`, `friction_evidence.py`,
  `e0042_table.py`, `e0037_judge.py`, `e0044_compare.py`, `budget.py`.
  `pc_stall_diag.py` is superseded by `mu_switch.py` (wrong time).

Earlier items (from Nov 8):

- Collect E0028 (nudge, 3D Gamma 5, 1000 cycles, seeds 2 to 5) and E0029
  (unmodified case g, seeds 3 to 5, 1020 cycles). If a case-g baseline
  completes, judge the nudge's case-g runs against it.
- Wait for Chris on:
  - how to treat the nudge's rare overlaps;
  - the Figure 1 comparison spec;
  - the case-b comparison;
  - the wide-box seed offsets (E0027).
