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
  - See Current state.

### RQ2: Do the pattern transitions show hysteresis, and where?

- Hypothesis: ramping Gamma up and then down at fixed frequency crosses some
  pattern transitions (e.g. flat to stripes or squares, or hexagons) at
  different Gamma, as seen in experiments.
- Falsified if: with ramps slow enough that the result doesn't depend on ramp
  rate, up and down transitions coincide within run-to-run spread.
- Depends on RQ1 for any condition with long contacts.
- Status: open.

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

- Redesign proposed Nov 9: `evidence/D0016-option4-redesign.md` (D0016).
- Not approved. Plate-stick's failures are exactly the pair contacts it is
  designed to handle.
- A design for a vibrated layer is in
  `evidence/D0015-option4-design.md` (proposed, with five choices for
  Chris).

## Current state

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

- Three queues are waiting on free disk (`sequel-data/runs/*.queue.log`):
  the last 15 E0031 runs and E0034 (`E0031-34.rest.spec`), and the case-b
  baseline E0036 (`E0036.spec`). They launch by themselves at 40.5 GB free.
  If they are not running at the next session, check `ps` for `qx3.sh` and
  restart them from the specs (lines already launched are in the logs).
- Then: record E0031's and E0034's outcomes with
  `tools/e0031_evidence.py`; judge the nudge against the E0036 baseline
  (`bulk.py baseline`, `judge`); judge the nudge's case-g runs on settled
  cycles once continued to 1020.
- Wait for Chris on D0016, and on whether small runs may launch below the
  disk floor when the program is not the cause.
- Tools added Nov 10: `noise_final.py`, `e0032_evidence.py`,
  `e0031_evidence.py`, `qx3.sh`, `e0036_run.sh`.

Earlier items (from Nov 8):

- Collect E0028 (nudge, 3D Gamma 5, 1000 cycles, seeds 2 to 5) and E0029
  (unmodified case g, seeds 3 to 5, 1020 cycles). If a case-g baseline
  completes, judge the nudge's case-g runs against it.
- Wait for Chris on:
  - the option-4 design (D0015);
  - how to treat the nudge's rare overlaps;
  - the Figure 1 comparison spec;
  - the case-b comparison;
  - the wide-box seed offsets (E0027).
- If option 4 is approved, build it on `method/persistent-contact` from
  plate-stick's plate frame.
