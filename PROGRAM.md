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
  - Nov 18: pause lifted; held contacts built (normal velocity held at
    zero, sliding free, let go at a pull). No stall on the 2D grid or the
    stall runs; deep Gamma 5 layers are slow (see Option 4).
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
  - Nov 18 session: awake on AC, lid open, no sleep events. Free disk 30
    GB at the start and 29 at the end (other use of the Mac; program data
    8.6 GB), under the 40 GB floor all night, launches allowed down to 25.
    Ten cores full all night; three baseline loops paused 1.2 to 1.4 hours to
    give the held-contact runs cores.
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

- Branch: `method/nudge` (b608fef; 16f3334 with the accumulator fix).
- Frozen tests: 74 of 74 at b608fef (Nov 6, 7) and 16f3334 (E0103, Nov 24).
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
- **Nov 18: pause lifted; held contacts built** (`method/held-contact`,
  worktree `sequel-data/worktrees/held-contact`; pinned fixed-angle pilot
  `method/held-contact-fixed`). Decisions D0049 to D0052.
  - A chattering contact (slow hit on the plate, a side wall, or a held
    sphere; a free pair closing below 1e-10) is held: its normal relative
    velocity is kept at zero by impulses every 5e-4 time units, solved per
    held cluster (projected Gauss-Seidel, pushes only); sliding is free.
    It lets go when the impulse would be a pull, or when hit faster than
    0.01 (then an ordinary collision).
  - v1 09959f7, v2 9860a26 (fast hits free the sphere; warm-started,
    over-relaxed solve), v3 df3f4dc (round-off pair). Tests: 74 frozen and
    110 branch pass with the method on; with it off the engine is main's
    bit for bit.
  - Motion on the sphere lets go at the closed-form angle within 0.04
    degrees; the fixed-angle variant lets go 0.8 degrees after capture (its
    gap constant decides) and churns (`evidence/held-release-angle.json`).
  - Multi-sphere contacts are the rule (`evidence/held-cluster-sizes.json`).
  - Survival on the 2D grid and the stall runs: E0081 (sphere), E0082
    (fixed), `evidence/E0081-E0082-results.json`; see Current state.
- **Paused (Nov 13 instruction; lifted Nov 18).** No builds, no pilots; do not build on
  the plate-only rest rule. The step that was next, normal-only rest with
  friction, was not started. E0045 (held-hit pilot and sweep) and the
  rest of E0042's sweep were dropped with the friction diagnostics
  (D0031).

## Current state

### L0015 (nudge fast pass): f\* 0.65 and 0.74 loops ended at Gamma 4.6 (ran Nov 25 05:40Z)

Started by the service for jobs hatteras-164660 (f\* 0.65, A0184, 65.29
CPU-hours) and hatteras-164661 (f\* 0.74, A0183, 63.49 CPU-hours), both
FAILED (exit 1 by design on the 48 CPU-hour step cap; clean energy audit in
every step). Session summary: `sessions/2026-11-25-L0015.json`. Both added
to `evidence/E0089-step-table.json`, which now holds six loops.

- **Stops:** both at Gamma 4.6. f\* 0.65 completed only 10 of 25 cycles
  there, at about 17,300 CPU-seconds per cycle, the dearest step of any
  loop; f\* 0.74 completed 21, at about 8,200. Six of eight loops have now
  ended on the cap; none got above Gamma 4.6.
- In the stopping step, events per particle per cycle were 8.9 times (f\*
  0.65, about 71,200) and 4.6 times (f\* 0.74, about 33,300) the step
  before. CPU per event on Hatteras changed by 0.98 and 1.03 times.
- **Corrections asked for by the checker (Nov 24, third review):** "CPU per
  event stays the same" holds only for the last step on Hatteras; on the
  Mac it moved 0.54 to 1.48 times between neighbouring steps. The "Mac to
  Hatteras 1.6 to 2.0 times" figure above mixes the machine with a change
  of Gamma step and is not a machine speed; withdrawn as such. Whether the
  extra collisions near 4.6 are physics or come from the nudge method is
  untested (a comparison with plain-engine loops at the same Gamma would
  settle it).
- f\* 0.44 and 0.50 are still in Gamma 4.6; D0072 wake on Nov 26 08:00Z
  stands.

### L0015 (nudge fast pass): f\* 0.38 and 0.84 loops ended; per-step counters corrected (ran Nov 24 16:06Z)

Started by the service for jobs hatteras-164656 (f\* 0.38, A0180) and
hatteras-164662 (f\* 0.84, A0181), both FAILED (exit 1 by design on the CPU
cap). Session summary: `sessions/2026-11-24-L0015-3.json`. Evidence
`evidence/E0089-step-table.json` (all four ended loops, Gamma 4.3 up).

- **Stops:** f\* 0.84 stopped at Gamma 4.6 after 24 of 25 cycles, like
  f\* 0.33 and 0.57. f\* 0.38 stopped one step earlier, at Gamma 4.55,
  after 14 of 25 cycles (about 12,300 CPU-seconds per cycle). Four of eight
  loops have now ended, all on the 48 CPU-hour cap, none above 4.6.
- **Correction (checker, Nov 24, second review):** the counter columns of
  the earlier E0089 tables were loop running totals, because checkpoints
  carry the counters from step to step. Recomputed from step-to-step
  differences: from the step before the stop to the stop, events per cycle
  rose 4.9 to 8.9 times, while CPU per event stayed within 3% on the same
  machine. **The wall is more events, not slower events.** The earlier
  "1.34 times" (below) is wrong; it is 3.2 to 3.5 times from 4.5 to 4.55.
  Plate collisions per cycle at the last step are 6 to 14 times their 4.5
  level, not 5.5 times. The Mac to Hatteras step costs 1.6 to 2.0 times
  more CPU per event.
- The referee's `events_per_particle_cycle` is a loop running total
  whenever `tools/ramp.py` starts a step from a copied checkpoint (put to
  Chris; the referee is Chris's). `evidence/E0085-nudge-wall-fields.json`
  carried the same error in one table; noted in the file.
- **Budget guard (D0072):** wake re-set for Nov 26 08:00Z. Four loops
  (f\* 0.44, 0.50, 0.65, 0.74) are still in Gamma 4.6.

### L0015 (nudge fast pass): second continued loop ended at Gamma 4.6; per-run budget guard (ran Nov 24 15:03Z)

Started by the service for job hatteras-164655 (FAILED, artifact A0177).
Session summary: `sessions/2026-11-24-L0015-2.json`. Evidence
`evidence/E0089-interim-f0.33.json`, `evidence/E0089-budget-check.json`.

- **f\* 0.33 loop (E0089):** same as f\* 0.57. Finished Gamma 4.55 (1,332
  CPU-seconds per cycle on Hatteras), then stopped at 4.6 on the 48
  CPU-hour CPU cap after 21 of 25 cycles (8,229 CPU-seconds per cycle).
  Energy audit clean. The job used 57.5 CPU-hours.
- **E0089's "loops complete above Gamma 5.0" clause has failed** at f\*
  0.33 and 0.57 under the registered 48-hour cap. The cost-drop
  prediction of the inelastic ball model is still untested.
- **Correction (checker, Nov 24):** the "five times" rise in cost from 4.5
  to 4.55 at f\* 0.57 compared the Mac with Hatteras. In events, which do
  not depend on the machine, the rise is 1.34 times (1.44 at f\* 0.33).
  (Wrong, running totals: 3.2 and 3.5 times; see the Nov 24 16:06Z run.)
- **Budget guard (D0072):** the six loops still running should stop at
  58 to 98 CPU-hours each. A loop that finishes its current step could go
  past the 100 CPU-hour per-run limit, but not before Nov 26 09:27Z. A
  timer wakes L0015 at 08:00Z that day to cancel any such loop. The
  question of whether "per run" means a job or a step is put to Chris.

### L0015 (nudge fast pass): first continued loop ended at Gamma 4.6 (ran Nov 24 12:37Z)

Started by the service for job hatteras-164659 (FAILED, artifact A0176).
Session summary: `sessions/2026-11-24-L0015.json`. Evidence
`evidence/E0089-interim-f0.57.json`.

- **f\* 0.57 loop (E0089):** finished Gamma 4.55 (980 CPU-seconds per
  cycle on Hatteras) and stopped at 4.6 on its 48 CPU-hour step cap after
  23 of 25 cycles (7,514 CPU-seconds per cycle). The loop is built to end
  at the first step on the way up that does not finish; the energy audit
  stayed clean. Nothing above 4.6 has run, so the inelastic ball model's
  prediction (cost drops again by 5.0) is still untested.
- Plate collisions per particle per cycle: 1,319 at Gamma 4.5, 2,297 at
  4.55, 7,720 at 4.6. CPU per event also rose 2.5 times from 4.55 to 4.6
  on the same machine.
- The other seven loops are still running, all in their 4.55 or 4.6 step.
  D0071: no resubmission until all eight have ended; raising the cap again
  goes to Chris.

### Nov 23 instruction to L0009: option four from the paper (ran Nov 24 05:05Z)

Session summary: `sessions/2026-11-24-L0009.json`. A design on paper only,
with no code and no runs: `lines/L0009/design.md`.

- **Clusterlifter against the paper:** of the paper's seven elements, it
  kept one fully (a fast hit wakes the sphere), two partly, and four not
  at all. D0049 replaced the resting state with periodic pushes solved
  jointly. It cost a time step and five more numerical constants, energy
  removed at every step, overlaps under friction, and the paper's speed-up.
- **The resting-contact design:**
  - three states: free; riding (a lasting contact that keeps rolling or
    sliding, on the plate in closed form, on a still sphere integrated
    until the contact force reaches zero); still (the paper's frozen state
    carried with the plate, not integrated);
  - a sphere becomes still only if the balance test passes, so unstable
    stacks last until the upper sphere rolls off;
  - capture is the base collision with normal restitution zero;
  - the paper's restitution of 0.4 on frozen spheres, its periodic check
    and its energy return are dropped.
- Five choices for Chris end the design.

### L0009 instruction of Nov 24: implement the resting-contact design (ran Nov 25 04:40Z)

Session summary: `sessions/2026-11-24-L0009-2.json`. Building began on
branch `method/rest`; nothing is wired into the event loop or run yet.

- **Chris's answers built in** (D0073 to D0076, `lines/L0009/design.md`
  section 6): spheres may ride on rolling spheres (a moving stack,
  integrated as one smooth system, every contact change an event, no fixed
  step); wake speed 0.05 above rest speed 0.01, both parameters; hits in
  between bounce off the still sphere by the base collision law; no stored
  energy; friction in the balance test.
- **Built and tested in isolation (41 tests,
  `evidence/L0009-build-2026-11-25.json`):** the parameters; the balance
  test with friction; the closed-form ride on the plate (agrees with a
  numerical solve to 1e-13); a first-contact search on curved paths that
  cannot step past a contact; moving-stack motion with contact forces from
  a linear solve and contact changes as exact events (roll-off from a
  fixed sphere at the textbook angle to 1e-9, energy books to 3e-13); and
  compiled forms of the plate ride. Not yet in the event loop.

### Nov 23 instruction to L0001 (nudge): is anything left? (ran Nov 24 04:49Z)

### L0017 (slow loops): settle-then-step loop collected (ran Nov 24 06:11Z)

Started by the service for job hatteras-164664. Session summary:
`sessions/2026-11-24-L0017.json`. Evidence `evidence/E0090-results.json`
(tools/settle_loop_gap.py), artifact A0173.

- **E0090 (falsified on iii as registered):** all 29 steps settled under the
  stopping rule (D0056) in 200 to 400 cycles (14 at 200, 9 at 250, 4 at 300,
  2 at 400), none near the 3000 limit; 48.14 CPU-hours, no slow stretch, no
  audit failure.
- Gap over each whole step (the registered measure): largest 0.111 D at
  Gamma 2.25, 0.108 at 2.2, about the same as at 400 cycles a step (0.103).
- That measure includes the relaxation from the previous Gamma. The way-down
  step at 2.2 falls from 0.37 to a flat 0.15 D; over the settled window (last
  100 cycles) the gap is 0.021 D at 2.2 and 0.048 at 2.25. Largest
  settled-window gap 0.057 at 2.5, where each branch wanders by about 0.05 D.
- Reading, one seed only: at 2.2 the gap closes once the step is allowed to
  settle; at 2.25 a 0.05 D difference remains, the size of the wandering seen
  at 2.5. The stopping rule is lenient (one degree of freedom in its error).

### L0001 (nudge): frozen tests on 16f3334 (ran Nov 24 05:52Z)

Session summary: `sessions/2026-11-24-L0001.json`; evidence:
`evidence/E0103-results.json`, `evidence/L0001-closing-review-2026-11-23.json`
(with the checker's corrections).

- Frozen engine tests: 74 of 74 on the nudge at 16f3334 (E0103, Hatteras
  job 165153, main as control also 74). b608fef had passed them Nov 6
  and 7, so the Nov 23 run's "never run" was wrong.
- method/nudge is back in this clone at 16f3334 (bundle from A0172);
  B0008 resolved.
- Audit: only the two nudge runs rerun after the accumulator fix are
  shown clean (176 failing cycles, all round-off); the rest likely, not
  shown. Bulk check passes only where there are no lasting contacts.
- Next: Chris closes L0001. Nothing left that was asked.

### Jobs collected, run of Nov 24 (L0020, ran Nov 24 05:04Z)

Session summary: `sessions/2026-11-24-L0020.json`. No new instruction.

- **E0099 collected and closed (falsified on energy).** The last three
  spring runs completed 120 cycles (2D Gamma 5 depth 15 at both f*, and
  3D Gamma 5 f* 0.44 N 2400): all 13 spring runs at k = 1e7 survived, with
  no slow episode. But 1 to 16 cycles per run gained energy at six
  conditions, which meets the registration's falsification rule.
- **Checker's challenge on hidden friction gain (E0102).** A bookkeeping-only
  diagnostic (grapenuts branch `contact-energy` 8030406; dynamics
  bit-identical) sums each spring's work over its life. It closes the
  books exactly: summed contact work minus booked dissipation equals the
  run's residual. Whole contacts that gain energy: 0.2 to 2.7 percent;
  their total gain is 0.2 to 0.3 of the run's net residual. The tangential
  force alone gains over 1.5 to 6.6 percent of contacts (the limit set was
  1 percent), but only 2 to 7 percent of the kick-level friction gain
  survives a whole contact. Three conditions, 30 cycles, one seed.
- Withdrawn: "on your Mac these ran" (E0100). Sequel's baselines fail at
  Gamma 3.5 f* 0.3 depth 10 and Gamma 5 f* 0.5 depth 5 on the Mac too
  (E0031, other seeds), so it is not a machine difference.

### Nov 22 instruction, run 3 of Nov 23 (L0020, ran Nov 24 02:36Z)

Session summary: `sessions/2026-11-23-L0020-3.json`.

- **Grapenuts ran.** The clone is here (486d8eb, B0007 resolved). Code
  description for the checker: `lines/L0020/grapenuts.md`. The referee's
  `long_contact.py` would run grapenuts' hard engine and has no audit term
  for spring dissipation. So E0099 runs a step-for-step copy of it in
  grapenuts (`scripts/sequel_long_contact.py`, branch `sequel-eval`
  23a3676), D0066.
- **Survival (E0099, tc, k = 1e7, seed 1, 120 cycles):** 10 of the 12
  2D grid conditions completed 120 cycles, including Gamma 3.5 depth 15 and
  Gamma 5 depths 5 and 10, where sequel's engine stalls; Gamma 5 depth 15 (both f*) and the 3D
  case were at 60, 80 and 100 cycles and still running.
- **Energy:** with the springs' booked dissipation counted, the per-cycle
  residual's worst cycle per run is 1.5e-4 to 9.5e-3 of throughput, mostly a loss. A few cycles
  at Gamma 5 (mostly f* 0.3) gain, up to +9.5e-3 in one cycle (net over
  every run still a loss). That is far above the
  referee's 1e-8 rule, which a time-stepped spring can't meet. The
  referee's own sum, which leaves the springs out, is off by 6e-2 to 5e-1.
- **Bulk (E0100):** sequel's baselines ran on Hatteras at three of the five
  shallow conditions. The other two failed at seed 1 (pair overlap in cycle
  1, frozen time in cycle 5), the same way as grapenuts' hard mode. At k =
  1e7 grapenuts passes 2 of 3 and fails Gamma 3.5 f* 0.5 depth 10 on plate
  contact only (+3.8 sd). At k = 1e6 it fails Gamma 3.5 f* 0.5 depth 5
  and f* 0.5 depth 10; k = 1e8 passes all three (worst 2.2 sd) (E0101).
  The bulk result depends on the stiffness and converges as it grows, but
  at k = 1e8 one shallow run gained energy on net (+8e-6 of throughput).
  E0099's two deepest Gamma 5 runs and the 3D run were still going at the
  end of the run (none had failed).

### Nov 22 instruction, run of Nov 23 (L0020)

Session summary: `sessions/2026-11-23-L0020.json`.

- **Not started; blocked on the code (B0007).** The grapenuts clone
  (`sequel-data/grapenuts`, 486d8eb) isn't on this machine (Linux
  container), and a read-only Hatteras job (E0095, D0062) found no copy
  there either. Plan for the review, energies against baseline and phase
  diagram: `lines/L0020/progress.md`.

### Last Gamma 5 jobs collected, Nov 24 (L0019)

Session summary: `sessions/2026-11-24-L0019.json`. No instruction; started
because the last four E0098 jobs and their E0094 twins ended. Evidence:
`evidence/E0098-results.json`; E0098's outcome is written (supported).

- **Final E0098 count: eight of twelve 2D conditions completed 120 cycles**
  with ride, audit clean in every cycle of all twelve runs (worst 2.8e-13,
  no gains). Two of the eight are conditions the unmodified engine does not
  complete (Gamma 3.5 f\* 0.3 depth 15, Gamma 5 f\* 0.3 depth 15). At
  Gamma 3.5 f\* 0.5 depth 15 the unmodified engine does complete, in 2.9
  CPU-hours against ride's 188 CPU-seconds (correcting run 3's "three
  stalls", per the checker).
- **The four other Gamma 5 runs stopped at the 2 CPU-hour cap** after 52,
  48, 14 and 12 cycles (f\* 0.3 depths 5 and 10, f\* 0.5 depths 10 and 15);
  read as not survived, not proven stalled (D0067). In each, the unfinished
  last cycle holds 74-99% of the run's root-search limit hits (6.4-8.7
  million, 10000 steps each) and thousands to hundreds of thousands of
  captures; events per CPU-second drop to 1700-11000 against 72000-490000 in
  completed runs. The time goes into ride's own search for riding-pair
  contacts, not into tiny plate bounces (none in any run).

### Jobs collected, run 3 of Nov 23 (L0019)

Session summary: `sessions/2026-11-23-L0019-3.json`. No instruction; started
because eight E0098 jobs ended. Evidence: `evidence/E0098-interim.json`.

- **Eight of twelve E0098 jobs** (A0115-A0122) completed 120 cycles with
  every cycle's audit clean (worst 2.8e-13, no gains, no slow episodes):
  all six Gamma 3.5 conditions, Gamma 5 f\* 0.3 depth 15 and f\* 0.5 depth 5.
  This includes three conditions where the unmodified engine stalls in
  cycle 1 or 3.
- **Four Gamma 5 jobs are still running**, past the unmodified stall cycle and
  clean so far: f\* 0.3 depth 5 (cycle 52, in slow episodes near phase
  0.94), f\* 0.3 depth 10 (cycle 40), f\* 0.5 depths 10 and 15 (cycle 10).
  The last three have recorded no new cycle for 20 to 50 minutes. Their E0094
  twins are identical so far and stuck at the same cycles.
- Each E0098 job matches its E0094 twin cycle for cycle on Hatteras, so the
  booking fix did not change the motion there either. No scheduled
  release in any of the eight finished runs.

### Checker's challenges, run 2 of Nov 23 (L0019)

Session summary: `sessions/2026-11-23-L0019-2.json`. No instruction; started
for the checker's challenges.

- **Audit bug fixed** (E0096, D0063 corrects D0060): v2 booked plate
  captures twice in the audited terms. With 7ae3349 the audit is clean in
  every cycle with capture on; the motion is unchanged.
- **Sphere capture fires** (E0097) at all six deep 2D conditions (1 to 1072
  times); the Nov 23 "never fires" came from that check's own event cap.
  All six passed the cycle where the unmodified engine stalls, with clean
  audits.
- **E0094's audit is invalid** (double booking); its survival stands:
  120 cycles at all Gamma 3.5 conditions and two at Gamma 5, four jobs
  still running. Rerun on the fixed commit: E0098, jobs 164950-164962.

### Nov 22 instruction, run of Nov 23 (L0019)

Session summary: `sessions/2026-11-23-L0019.json`.

- **Branch recovered.** `method/ride` wasn't on this machine (a Linux
  container); v1 was copied from the engine checkout in A0098's Hatteras
  run folder (4d6c4e0, same files as 0600773).
- **v2 built** (3380eb3, 06be1f7; D0059 to D0061): sphere-on-sphere capture
  into rigid riding clusters (horizontal momentum conserved), release of
  dependents on a hit, captures booked in the audited terms (wrongly: booked twice, fixed in
  run 2), and a fix for
  a silent missed contact in the riding-pair root search. Frozen tests pass.
- **Sphere capture does not fire** (E0093): zero sphere captures in 20
  cycles at every 2D grid condition that ended; the deep stalls remain.
  The method does not yet act where it is needed. (Withdrawn by run 2:
  E0093's own event cap stopped the deep runs early; see E0097.)
- **E0092's six v1 jobs failed** in 29 s (referee refuses an existing
  output folder); they are labelled E0091 in the job records. B0006
  resolved.
- **E0094 submitted**: v2 at all 12 2D grid conditions, 120 cycles,
  Hatteras jobs 164936 to 164947.

### Nov 21 findings (L0019)

Instruction of Nov 21 (one item on L0019: unpaused). Session summary:
`sessions/2026-11-21-L0019.json`.

- **Analytical ride method designed and v1 built** (`method/ride`, D0058):
  replaces the clusterlifter's periodic impulses with closed-form sinusoidal
  trajectories. A sphere captured on the plate follows z = A sin(omega t) + r
  exactly and releases at the analytical phase where plate acceleration = minus g.
  No solver, no time step, no impulse stream. v_capture = 1e-4 (same as
  plate-stick's v_stick). 74 of 74 frozen tests pass with ride off
  (bit-identical to main).
- **v1 is plate-only:** does not capture sphere-on-sphere contacts, so the
  stalling conditions (Gamma 5 deep layers) overlap in cycle 1, same as
  plate-stick. v2 (sphere-on-sphere rigid-body capture) is designed but not
  built.
- **E0091 half-submitted:** 6 of 12 2D grid pilot jobs on Hatteras (the
  Gamma 3.5 conditions, jobs 164696-164701). The Gamma 5 conditions are blocked
  by the 48-slot limit.

### Nov 20 findings (L0016)

Instruction of Nov 20 (housekeeping only on L0016). Session summary:
`sessions/2026-11-20-L0016.json`.

- **E0073 collected:** all ten baseline loops (unmodified engine with
  friction, half-push start) are dead. Nine have usable data; f\* 0.27
  failed at step zero. The baseline covers Gamma 3.0 down to 2.15 to 2.5
  and up to 4.0 to 4.35, then fails (physical failure, frozen time, or CPU
  budget). The nudge reaches 0.1 to 0.4 higher in Gamma at every frequency.
  Total: 462 completed steps, 98.1 CPU-hours, 680 MB, no audit failures.
  Falsified on prediction (i).
- **Disk discrepancy explained:** `program check` sums only the `disk_gb`
  field from experiment outcomes. Most experiments (67 of 73) recorded zero
  (pre-dating the field), and 1.8 GB of reference data (`hvar`,
  `c-baseline`, `bulk-pilot`) predates the program. See
  `evidence/E0073-disk-discrepancy.json`.
- **"Push main" item:** already removed from Next by the Nov 20 L0009
  session.

### Nov 20 findings (L0018)

Instruction of Nov 20 (one item on L0018). Session summary:
`sessions/2026-11-20-L0018.json`.

- **Width-200 field storage cut (D0054):** no height-field arrays stored in
  fields.npz for the width-200 passes (E0074, E0075, E0076). The Fourier
  spectrum and variance are kept at every frame (121 KB per step compressed);
  the 80 by 80 height grid (2465 KB per step) is dropped. No analysis tool
  reads the stored grids: loop_analysis.py uses only the spectrum;
  pattern_id.py computes its own field from checkpoint.npz particle
  positions. Per loop at L 200 with 213 steps: about 390 MB, down from about
  880 MB. The 15 GB disk budget holds about 38 loops instead of 17.
- **E0071 collected:** the onset loop at L 200 (f\* 0.44, no friction)
  completed all 53 steps (Gamma 1.7 to 3.0 and back), 22.9 CPU-hours, no
  slow stretch, no audit failure, 311 MB.

### Nov 20 findings (L0015)

Instruction of Nov 20 (one item on L0015). Session summary:
`sessions/2026-11-20-L0015.json`.

- **Nudge wall is period-2 (E0085):** the cost wall at Gamma 4.4 in the
  nudge fast pass is caused by the layer bouncing on alternating cycles.
  One cycle the layer is airborne (58 to 850 events per particle per cycle
  between Gamma 4.0 and 4.5 at f\* 0.44); the next it chatters on the
  plate (268 to 9425). The CPU cost per cycle doubles between 4.4 and 4.45
  and again between 4.45 and 4.5. The spatial pattern disappears by
  Gamma 4.4 at f\* 0.44. At f\* 0.84 the wall is about 0.1 higher in
  Gamma. The E0072 continuations each got one step past E0065 and are dead.
- **All earlier background jobs dead:** E0069, E0071, E0073 and E0072 are
  all dead. Only E0083 (from L0009 tonight) is alive.

### Nov 20 findings (L0017)

Instruction of Nov 20 (housekeeping only on L0017). Session summary:
`sessions/2026-11-20-L0017.json`.

- **E0069 collected:** the 400-cycle-per-step slow loop at f\* 0.44
  finished: all 29 steps, 34.44 CPU-hours, 361 MB, no slow stretch, no
  audit failure. The gap between the branches is 0.103 D at Gamma 2.2
  (range 2.2 to 2.25), against 0.200 D over 2.2 to 2.3 at 100 cycles and
  0.242 D over 2.0 to 2.4 at 25. Within-step drift is larger at 400 than
  at 100 cycles at the gap edges (Gamma 2.25 up 0.113 vs 0.070, Gamma 2.2
  down 0.150 vs 0.095). Falsified on prediction (iii).

### Nov 23 findings (L0009)

Instruction of Nov 22 (three items on L0009). Session summary:
`sessions/2026-11-23-L0009.json`.

- **E0086 collected:** one of four deep Gamma 5 runs completed 120 cycles
  (Gamma 5, f\* 0.5, depth 15, seed 1); one ended in frozen time at cycle 96
  (Gamma 5, f\* 0.3, depth 15); two timed out without a CPU cap (110 and 70
  cycles). Survival is a partial advance over the unmodified engine (which
  stalls in cycles 1-2), but frozen time recurs.
- **Energy audit fails at deep Gamma 5 (E0086):** every cycle in every run
  fails (worst residual 2.0e-4, all negative). No energy is injected.
  The residuals equal the hold energy in EN\_HOLD, made visible in v4 by
  moving it out of plate dissipation. The same hold energy fraction
  (minus 1e-4 or less of plate work per cycle) was present but invisible in
  E0081 (v3). The audit threshold is 1e-8.
- **clusterlifter.md written:** `lines/L0009/clusterlifter.md` describes
  v4 (3983f59f, confirmed readable from A0090) and the v5 delta (D0055).
  Every deviation from the base model is listed with its decision record
  (or lack thereof). The post-hold-step overlap tolerance (`htol = 1e-3` in
  v4, `1e-6` in v5) has no decision record.
- **No code changes.** Chris is reviewing the design.

### Nov 21 findings (L0009)

Instruction of Nov 21 (three items on L0009). Session summary:
`sessions/2026-11-21-L0009.json`.

- **E0083 collected and abandoned:** the wrong-condition runs (width 20,
  depths 200/300 instead of 100/10/15) used 44.75 CPU-hours. All four
  entries cleared from active.jsonl.
- **E0086 submitted to Hatteras:** four corrected deep Gamma 5 runs (width
  100, N 1000/1500, seed 1, 120 cycles, no CPU cap) as jobs 164638-164641.
  Still compiling at the end of the session.
- **Bulk failure explained (E0087):** the clusterlifter with mu=0 passes
  every quantity against the mu=0 baseline at Gamma 3.5, f\* 0.3, depth 10
  (worst 0.69 sd). The E0084 failure was from comparing a frictionless
  engine against a friction-on baseline, not from the hold method.
- **Friction overlap root cause (D0055):** plate friction in hold steps
  drifts the held sphere 2.3e-7 diameters per dt\_hold toward touching
  neighbours (tolerance 2e-8). A gap limiter is implemented (`method/held-contact`
  8f8f999) that scales the friction impulse to prevent overlap, but it is
  partial: it delays failures from cycle 1 to cycle 10-11. Friction
  defaults to off.
- **Energy comparison built** (`evidence/E0086-energy-comparison.json`):
  per-cycle hold energy beside the unmodified engine's audit at six Gamma 5
  conditions. Hold energy always a loss (minus 2.6e-6 to minus 9.5e-5 of
  plate work).

### Nov 21 findings (L0017)

Instruction of Nov 21 (one item on L0017). Session summary:
`sessions/2026-11-21-L0017.json`.

- **Settle-then-step ramp built** (`tools/settle_ramp.py`, D0056): each step
  runs in blocks of 50 cycles, checking after at least 200 whether the pattern
  amplitude and layer height have settled (the mean of the last 100 cycles
  within 2 block standard errors of the previous 100). Maximum 3000 cycles per
  step. Tested on a small 2D case on the Mac.
- **E0090 submitted to Hatteras:** the settle-then-step loop at f\* 0.44 on
  the frictionless unmodified engine, same box and seed as the 25, 100 and
  400-cycle loops (29 steps, Gamma 1.9 to 2.6 and back). Job 164664, single
  core, 5-day wall time, estimated 80 CPU-hours.

### Nov 25 findings, second run (L0018, started by the service for job 164681)

No instruction. Session summary: `sessions/2026-11-25-L0018-2.json`.
Evidence: `evidence/E0076-interim.json` (nudge f\* 0.38 loop added),
`evidence/E0076-results.json` (one sentence corrected).

- **Nudge (E0075) f\* 0.38 at width 200 (job 164681, A0186):** floor
  Gamma 2.45 (2.0 CPU-hour cap at 2.4 after 24 of 25 cycles), highest
  Gamma 4.35; at 4.4 time froze (a stall) in cycle 25, at 6.5 CPU-hours,
  under the 8.0 cap. 50 steps completed, 75.1 CPU-hours, no energy gains,
  audit failures or slow stretches. The width-100 nudge loop (E0065) covered
  2.25 to 4.35: its floor and its stop at 4.4 were both 0.5 CPU-hour cap
  stops. So the top is the same last completed step (the wall at Gamma 4.4
  appears in the wider box too); the floors are cost floors and not
  comparable. A matched step costs 7.6 times as much at width 200 going
  down and 10.3 times going up (medians, 11 and 38 pairs). Slurm says
  FAILED; that is how a loop ends.
- **Checker's point (Nov 25 review):** "width 200 never reached further"
  was false at the f\* 0.50 floor (2.35 against 2.4, both cap stops).
  Narrowed in `evidence/E0076-results.json`, the line state and progress:
  no end where the comparison means something reached further.

### Nov 25 findings (L0018, started by the service for job 164691)

No instruction. Session summary: `sessions/2026-11-25-L0018.json`.
Evidence: `evidence/E0076-interim.json` (f\* 0.38 loop added; cost jump
near Gamma 3.35), `evidence/E0076-results.json` (working ranges, all ten
E0076 loops).

- **Baseline (E0076) f\* 0.38 at width 200 (job 164691, A0185), the last
  E0076 loop:** floor Gamma 2.45 (CPU cap at 2.4, 23 of 25 cycles),
  highest Gamma 4.0 (8.0 CPU-hour up-leg cap at 4.05 after 17 of 25
  cycles). Width 100: 2.35 (overlap at 2.3) to 4.0 (stall at 4.05).
  43 steps, 65.5 CPU-hours, no energy gains, audit failures or slow
  stretches. At 4.05 the cost per cycle rose 14 times at width 200 and
  17 times at width 100: the same slow-down at the same Gamma. This is the
  first width-200 top set by the up-leg cap.
- **E0076 working ranges, all ten f\*:** at no end where the comparison
  means something did width 200 reach further than width 100 (corrected
  in the second run: at the f\* 0.50 floor, a cap stop at both widths, it
  went 0.05 lower). Of four ends where both widths stopped for a
  physical reason, width 200 reached 0.15 to 0.2 less far at three (f\*
  0.65 both ends, 0.57 top) and the same at one (0.44 top). At f\* 0.74 and
  0.50 width 200 overlapped at 4.05, a Gamma width 100 completed. Four
  floors are cost floors at both widths. Four of ten width-200 loops broke
  in their first step, against one of ten at width 100. One seed each.
  343.6 CPU-hours for the ten loops.
- **Checker's points (Nov 24 third review):** corrected the f\* 0.57 up-leg
  median to 11.4 (it was written 11.5 in the third run's text above). Agreed
  that the high up-leg medians at f\* 0.44 and 0.57 come from the width-100
  cost halving near Gamma 3.35, not from width 200 being dearer; withdrew
  the proposal to size up-leg caps from them. At f\* 0.38 the width-100
  cost instead rises 1.7 times at 3.35, with more of the height variance
  in the same spectral ring (0.61 to 0.67), and no change of ring.
- E0076's outcome is not written: its registered test is on where the
  pattern appears, and no onset has been measured at either width. A pilot
  at f\* 0.38 (`evidence/E0076-onset-pilot.json`, ad hoc measure, no claim):
  the pattern wavelength is the same at both widths (22 to 25 sphere
  diameters). The pattern is lost between Gamma 2.5 and 2.45 on the way down
  at both widths, and back at 2.65 (width 100) and 2.7 (width 200) on the
  way up. So the test can be applied once the measure is decided.

### Nov 24 findings, third run (L0018, started by the service for job 164686)

No instruction. Session summary: `sessions/2026-11-24-L0018-3.json`.
Evidence: `evidence/E0076-interim.json` (f\* 0.74 loop added; up-leg cost
ratio).

- **Baseline (E0076) f\* 0.74 at width 200 (job 164686, A0182):** floor
  Gamma 2.25 (CPU cap at 2.2, 23 of 25 cycles), highest Gamma 4.0 (sphere
  overlap at 4.05 after 24 cycles completed). Width 100: 2.15 (CPU cap at
  2.1) to 4.1 (CPU cap at 4.15). 51 steps, 60.0 CPU-hours, no energy gains,
  audit failures or slow stretches. Nothing to relaunch. The floor is a cost
  floor at both widths. The top is one-sided: width 200 broke at a Gamma
  that width 100 completed.
- **Up-leg cost ratio (checker, Nov 24):** matched steps above Gamma 3.0 cost
  a median of 7.3 times as much at width 200 (94 pairs, f\* 0.44 to 0.74).
  The median is 11.5 at f\* 0.44 and 0.57. The up cap was scaled only four
  times, so tops that stop on the cap are cost limits too.
- Ten of 30 width-200 loops have ended. One baseline loop (f\* 0.38) is still
  running.

### Nov 24 findings, second run (L0018, started by the service for jobs 164689 and 164690)

No instruction. Session summary: `sessions/2026-11-24-L0018-2.json`.
Evidence: `evidence/E0076-interim.json` (two loops added, width-100 stop
modes, per-step cost ratio).

- **Baseline (E0076) f\* 0.50 at width 200 (job 164689, A0178):** floor
  Gamma 2.35 (CPU cap at 2.3, 23 of 25 cycles), highest Gamma 4.0 (sphere
  overlap at 4.05 in cycle 1). Width 100: 2.4 (CPU cap at 2.35) to 4.05 (CPU
  cap at 4.1). 47 steps, 56.9 CPU-hours.
- **Baseline (E0076) f\* 0.44 at width 200 (job 164690, A0179):** floor 2.4
  (CPU cap at 2.35, 22 of 25 cycles), highest 4.0 (overlap at 4.05 in cycle
  16). Width 100: 2.3 (CPU cap at 2.25) to 4.0 (stall at 4.05). 45 steps,
  56.9 CPU-hours. Neither loop had energy gains, audit failures or slow
  stretches. Nothing to relaunch.
- **Correction (checker, Nov 24):** at f\* 0.57, 0.50 and 0.44 the floor was a
  CPU cap stop at both widths, so those floors are cost floors and are not
  comparable. The caps were scaled four times (D0046) while a down-leg step
  costs 6.6 to 8.4 times as much at width 200 (median 7.4 over 49 matched
  steps at four f\*), replacing the earlier "five to seven times".
  Comparable ends so far: f\* 0.65 (overlaps at both widths at both ends:
  2.4 to 3.9 against 2.25 to 4.1) and the upper end at f\* 0.57 (3.8 against
  4.0) and 0.44 (4.0 at both).

### Nov 24 findings (L0018, started by the service for job 164688)

No instruction. Session summary: `sessions/2026-11-24-L0018.json`.
Evidence: `evidence/E0076-interim.json` (loop added).

- **Baseline (E0076) f\* 0.57 at width 200 (job 164688, A0175) ended
  under its own rules.** Down to a floor at Gamma 2.35: the step at 2.3
  reached its 2 CPU-hour cap after 23 of 25 cycles (a cost stop, not an
  overlap). Up to 3.8; at 3.85 it stalled in cycle 11. Width 100 at the
  same f\*: 2.2 to 4.0. 43 steps completed, 53.0 CPU-hours, median 1.02
  CPU-hours per 25-cycle step. No energy gains, no audit failures, no slow
  stretches. Nothing to relaunch.
- **Corrections to the Nov 23 section (from the checker's review):** the
  E0075 caps were not "kept by Chris on Nov 22". The Nov 21 question about
  them went unanswered, so its default applied (let the loops run and
  stop). The width-200/width-100 cost ratio is about five to seven times,
  not measured like-for-like, and is not shown to agree with E0070's 4.7
  to 5.6.

### Nov 23 findings (L0018, started by the service for job 164687)

No instruction. Session summary: `sessions/2026-11-23-L0018.json`.
Evidence: `evidence/E0076-interim.json`.

- **Six of the 30 width-200 loops have ended** (all FAILED in Slurm terms;
  each stopped under its own rules, none needs relaunching):
  - Baseline (E0076) f\* 0.84, 0.33, 0.30, 0.27: sphere overlap in the
    first step at Gamma 3.0 (0 or 1 of 50 cycles). At width 100 (E0073)
    only f\* 0.27 failed there.
  - Baseline f\* 0.65 (job 164687, A0171): down to a floor at Gamma 2.4
    (overlap at 2.35), up to 3.9, overlap at 3.95. Width 100 at the same
    f\*: floor 2.25, ceiling 4.1. 46.1 CPU-hours; median 0.91 CPU-hours
    per 25-cycle step, about 5.5 times width 100 (E0070 measured 4.7 to 5.6).
    No energy gains, no audit failures.
  - Nudge (E0075) f\* 0.27 (job 164684): hit its 4 CPU-hour first-step
    cap after 49 of 50 cycles at Gamma 3.0. No data past the first step.
- One seed. A larger box has four times the particles, so more chances per
  cycle for the unmodified engine's overlap; a narrower working range at
  width 200 is what that predicts, not yet a measured size effect.

### Nov 21 findings (L0018)

Instruction of Nov 21 (two items on L0018). Session summary:
`sessions/2026-11-21-L0018.json`.

- **Width-200 passes launched on Hatteras (E0074, E0075, E0076):** 30 jobs
  total, ten frequencies each. E0074 (no friction, jobs 164665-164674,
  5-day wall time), E0075 (nudge, 164675-164684, 7 days), E0076 (baseline
  with friction, 164685-164694, 7 days). No longer blocked by the Mac's
  disk floor.
- **Storage rule applied (D0057):** checkpoints at Gamma multiples of 0.5
  (changed from 1.0 in D0054), no height grids, spectrum kept. E0074 about
  640 MB per loop on Hatteras (36 MB fetched); E0075/E0076 about 690 MB
  (41 MB fetched). Hatteras checkpoints excluded from fetch.
- **caseb\_start.py committed** to `tools/` with relative paths for
  Hatteras (the baseline loops need the half-push start).

### Nov 20 findings (L0009)

Instruction of Nov 20 (four items on L0009). Session summary:
`sessions/2026-11-20-L0009.json`.

- **Clusterlifter v4** (`method/held-contact` 3983f59): hold energy booked
  in EN_HOLD only, not in plate dissipation. The referee's energy audit now
  shows hold energy as a residual per cycle. EN_HOLD_GAINS tracks per-cycle
  sum of positive hold-step net values.
- **Friction code** (D0053): written for plate, wall and sphere-sphere
  contacts (mu times each step's normal impulse, up to rolling limit, spin
  updated). Defaults to off: the velocity change from friction exposes
  pre-existing position-space overlaps in dense layers, triggering the
  engine's fail-fast overlap check.
- **Bulk check (E0084):** clusterlifter passes at Gamma 3.5 at both
  depth-5 conditions (worst 1.29 standard deviations) and at depth-10
  with f\* 0.5 (worst 0.80). Fails at depth-10 with f\* 0.3: horizontal
  energy 36% higher, every quantity off by many standard deviations.
- **Deep Gamma 5 uncapped runs (E0083):** launched at wrong conditions;
  collected and abandoned on Nov 21.

### Nov 18 findings

Instruction of Nov 18 (five items). One seed everywhere; nothing below is a
physical result. Session summary: `sessions/2026-11-18.json`.

- **CPU limits advisory** (item 1, D0046): the half-hour step cap is the
  floor rule going down only; going up a step gets a 2 CPU-hour guard
  (8 at L 200). Big costs are listed in the summary, not cut.
- **Nudge pass (E0065, falsified on (ii)):** every loop that started hit a
  wall going up at Gamma 4.35 to 4.45 (cost per cycle up 3 to 10 times
  between 4.3 and 4.45, at every f\*), clean audit, no slow stretch; f\* 0.27
  never finished its first step. Floors 2.0 (f\* 0.84) to 2.35 (0.33, 0.30).
  Continuation above the wall (E0072) is queued after the baselines (D0047):
  its cost is unknown, at least 0.5 to 1 CPU-hour a step.
- **No-friction pass (E0060) complete:** 2130 steps clean, 150 CPU-hours. At
  f\* 0.33 to 0.27 the way down is still patterned at the bottom of the loop
  (1.10 D at Gamma 1.8, f\* 0.27): the gap extends below 1.7 there.
- **Slow loops (E0064 done, E0069 running):** at 100 cycles a step the gap is
  0.20 D at most (2.25) and spans 2.2 to 2.3, against 0.24 D over 2.0 to 2.4
  at 25; edge steps still drift (up to 0.11 D). 400 cycles a step running,
  about 43 CPU-hours, 1.8 days; the next rate (1600) about 172, 7 days.
  Table: `evidence/E0069-results.json` (tools/rates_table.py).
- **Bigger box (E0070, E0071):** L 200 costs 4.7 to 5.6 times the paper's box
  per cycle (same events per sphere, 1.2 to 1.4 times the CPU per sphere);
  twice as deep costs 12 to 18 times (4 to 6 times the events per sphere),
  not the 3.8 scaled from 2D. Onset loop at L 200 running.
- **Baselines (E0073, supersedes E0068):** started by hand, running.
- **Width-200 passes (E0074 to E0076):** queued after the nudge
  continuations. No friction about 43 to 129 CPU-hours a loop (1.8 to 5.4
  days on one core), 765 for ten; nudge and baseline unknown above Gamma
  4.45. About 1 GB each: the 15 GB disk budget holds only a few; the queue
  holds at 14 GB.
- **Held contacts (item 5, option four; E0081 inconclusive, E0082
  falsified):** 2D grid and the settled-layer stall runs, 17 runs each
  variant, seed as the stall runs. Nothing stalled with motion on the
  sphere; 13 of 17 completed, including all Gamma 3.5 and 6 runs and all
  seven stall replays (to 20 cycles past the unmodified engine's stall);
  four deep Gamma 5 runs reached their 1 CPU-hour cap at 12 to 88 cycles
  with no slow stretch (the unmodified engine: 2 to 4 cycles there). Fixed
  angle: 14 of 17, one run with slow stretches. Audit clean in every cycle;
  hold energy a net loss in every run (up to 1e-4 of the plate's work). Most
  holds last one step and are captured again, which makes deep Gamma 5
  layers cost 30 to 300 CPU-seconds a cycle. Not checked yet: bulk physics,
  3D, Figure 1.
- **Queue:** `runs/q-1118.spec` via `tools/qx7.sh` (hard disk floor 25 GB,
  data cap 14 GB, live limit in `runs/q-1118.maxlive`). Tools on
  `tools/phase-diagram` (80782cd).

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

- **Nudge fast pass (L0015, Nov 25 05:40Z run):** collect the two E0089
  loops still in Gamma 4.6 (f\* 0.44, 0.50) as they end, adding each to
  `evidence/E0089-step-table.json`; D0072 wake on Nov 26 08:00Z. Then ask
  Chris for a bigger allowance or a cheaper cost probe above 4.6 (D0071),
  and write the E0089 outcome.
- **Nudge (L0001):** waiting for Chris: close now, or after a frozen-test
  run on 16f3334 (needs the nudge branch on this machine, B0008).
- **Grapenuts (L0020):** collect the rest of E0099 (deep 2D, 3D) and
  E0101 (stiffness); write their outcomes. Then a k = 1e8 pass over the
  grid with more seeds where the judge is close, and the phase-diagram fast
  pass with grapenuts (`lines/L0020/progress.md`).
- **Option four from the paper (L0009):** continue the build on
  `method/rest` (`lines/L0009/design.md` section 6 lists what is done):
  sphere states and capture in the event loop, still spheres moving with
  the plate, a single rider on still spheres, then moving stacks; then the
  frozen engine tests and the replayed stalls. Clusterlifter
  (`method/held-contact`) is stopped as built: no fixes, no runs.

- **Grapenuts (L0020):** all of E0099 to E0102 collected. Next: bulk
  judge at the conditions where sequel's engine fails, against the 1998 C
  code (`referee/c_baseline.py`); k = 1e8 over the grid with three seeds;
  the phase-diagram fast pass with grapenuts (`lines/L0020/progress.md`).
  Waiting on Chris for the overlap and energy-tolerance questions.
- **Clusterlifter design review (L0009):** `lines/L0009/clusterlifter.md`
  describes the current code (v4/v5). E0086 collected: energy audit fails
  every cycle at Gamma 5 deep conditions (hold energy ~1e-4 of plate work,
  all negative, no injection). Frozen time recurred at Gamma 5 depth 15
  f\* 0.3. No code changes pending — waiting for Chris's design direction.
- **Overlap tolerance (L0009):** the post-hold-step prediction uses
  `htol = 1e-3` (v4) or `1e-6` (v5) when friction is on. No decision
  record. No friction-on run completed.
- **Complete the friction gap limiter**: extend to cluster members and wall
  friction z-components. Test at the full 2D grid with friction on.
- **With friction working**: rerun the E0084 bulk check at Gamma 3.5,
  f\* 0.3, depth 10 with friction on (the mu=0 test shows the hold method
  passes).
- **Width-200 passes running** (E0074-E0076): 30 loops on Hatteras (jobs
  164665-164694), submitted Nov 21. E0074 no friction (5-day wall time),
  E0075 nudge (7 days), E0076 baseline (7 days). Checkpoints at Gamma
  multiples of 0.5 (D0057); about 36-41 MB fetched per loop. As of Nov 25,
  18 still running (ten E0074, eight E0075); all ten E0076 loops and E0075
  f\* 0.27 and 0.38 have ended (see Nov 23 to Nov 25 findings, L0018). E0076's
  working ranges are tabled (`evidence/E0076-results.json`); its registered
  judgement (where the pattern appears, within 0.1 in Gamma of width 100)
  still needs an onset measurement at both widths, then its outcome.
- **Nudge loops above the wall** (E0089): eight continuations on Hatteras
  (jobs 164655-164662), f\* 0.33 to 0.84, 48 CPU-hour per step guard.
  The inelastic ball model (E0088) predicts cost peaks near Gamma 4.6
  and drops by 5.0.
- **Slow loops (L0017):** E0090 collected (see Current state). Waiting for
  Chris: more seeds of the settle-then-step loop at f\* 0.44 with a stricter
  stopping rule, a second f\*, or stop. No jobs running.
- **Ride v2 (L0019)**: E0098 is collected (eight of twelve completed; four
  Gamma 5 runs at the CPU cap, time in the riding-pair root search). Next,
  if Chris agrees: count root-search steps from the A0129 checkpoint on
  Hatteras and make the search cheaper, then rerun the four; or the bulk
  check at the eight completed conditions first. No jobs running.
- **Disk:** free disk 14 GB, program data 10 GB of 15 GB.
- Option-four earlier branches (`method/persistent-contact*`) are superseded
  by `method/held-contact`; kept, not deleted.

Earlier items (before Nov 18) are in the git history of this file.
