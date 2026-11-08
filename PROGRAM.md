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
- Status: open. Nov 6: option 3 (elastic window) tried and does not help.
  Option 1 (nudge) completes 120 cycles at every stalled condition and
  seed, but fails the survival test at 2D Gamma 5, f* 0.3, depth 10 (overlap
  at cycle 163, seed 1) and survives depth 15 only after hours of slow
  stretches. Nov 7: option 2 (plate-stick) tried and gets no further than the
  unmodified engine: the lasting contact moves to stuck-free sphere pairs.
  See Current state.

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

## Approaches under consideration

The five options in `notes/contact-options.md`.

- **Option 3, elastic window** (`method/elastic-window`, v_el = 0.01;
  `-v003`, v_el = 0.03). Not a candidate (Nov 6): no better survival than
  the unmodified engine.
- **Option 1, position nudge** (`method/nudge`, b608fef). The only method
  that gets through the stalled conditions: 120 cycles at all 8 stalled 2D
  conditions and 3D Gamma 5 at seeds 1 to 3, and 1000 cycles at 7 of 8
  (seed 1). It does fail: overlap at 2D Gamma 5 f* 0.3 depth 10 (cycle 163,
  seed 1); depth 15 completed with 71% of its CPU in slow stretches. Every
  audit failure is an energy loss. Bulk physics passes wherever a baseline
  exists (2D shallow and deep against the unmodified engine and C code; 2D
  L = 400 at three conditions, 3 seeds each, Nov 7; provisional 3D case g).
- **Option 2, plate-stick** (`method/plate-stick`, 3900896; v_stick 1e-4;
  `method/plate-stick-v1e-3` for the pilot). Built and tested Nov 7 (frozen
  tests pass, capture/ride/release verified against the closed form, energy
  books balance to round-off). Fails survival like the unmodified engine (23
  of 24 runs overlap, at the same cycles), because every failure is a free
  sphere pressed obliquely on a stuck one. Captured spheres are always freed
  by collisions before their release phase. Where baselines exist it barely
  captures, so its bulk passes are uninformative. Not a candidate as it
  stands; transitive sticking (a model change Chris ruled out by default)
  or option 4 would be needed for the stuck-free pairs.
- **Option 4** (persistent contact) is not approved. Plate-stick's failures
  are exactly the pair contacts option 4 is designed to handle.

## Current state

The engine on `main` is the hardened import described in `README.md`: it
fails loudly on physical violations, matches an all-pairs reference, and
restarts bit-for-bit, but stalls or overlaps in lasting contact, including
at 3D Figure 1 case b (first landing, all 4 seeds tried with the default
start) and case g (overlap at cycle 567, seed 2; seed 1 ran 586 cycles to
its CPU cap with 5 audit-failing cycles, all energy gains).

Contact methods are on branches with worktrees under
`sequel-data/worktrees/` (merging needs Chris); frozen referee tests pass on
every branch (74 each), run with the branch's engine imported (Nov 7).

Nov 7 findings:

- Wider 2D boxes (L = 400): 13 to 15 pattern wavelengths; run-to-run spread
  over the judged 100-cycle window matches block spread (but so it did at
  L = 100 in the same pilot, so the earlier excess wasn't reproduced). The
  unmodified engine fails more first landings at L = 400 (depth 10: 2 of 5
  seeds at f* 0.5, 2 of 2 at f* 0.3), and the C code aborts at L = 400 at
  Gamma 3.5 f* 0.3 depth 10 and Gamma 5 f* 0.5 depth 5, so those have no
  baseline at this width.
- Case-b baseline: default start fails the first landing at seeds 1 to 4.
  Soft starts (engine constructor arguments via a cycle-0 checkpoint,
  decision D0011): hot fails in cycle 1 or slows; hot-dilute gets through
  cycle 1 and fails in cycle 2 at both seeds; cold-dilute (fill 0.10,
  v_init 0.1) passes cycle 1 and fails in cycle 2, its first dense landing,
  at both seeds (E0019). No start gets the unmodified engine through case b;
  every failure is at phase 0.87 to 0.95.
- Audit census (E0023) over every run: see evidence/E0023-results.json.

Tools (not in git): `sequel-data/runs/launch.sh` and `runs/tools/q.sh`
(queue under the core limit), `soft_start.py`, `overlap_repro.py` and
`stuck_overlap_replay.py` (replay a failure from a checkpoint or the start),
`spread.py` (run-to-run versus block spread), `judge_set.py`,
`audit_census.py`, `ev_runs.py`, `st.sh` (status), `watch.py`.

Referee findings to bring to Chris (not edits; the referee is his):

- long_contact.py has no way to set the initial condition; soft starts go
  through a cycle-0 checkpoint and --resume (D0011). An option would be
  cleaner.
- Checkpoints are skipped during slow episodes, so hours of work can be
  lost to a kill (E0008 depth 10: last checkpoint four hours before the
  overlap).
- The 1998 C code does not give 1020-cycle baselines at several 2D
  conditions (E0009) and none at two L = 400 conditions (E0024).

## Next

- Collect the two E0025 depth-10 nudge continuations.
- Nov 7: the nudge's depth-10 overlap (E0018) is a free sphere pressed
  obliquely on a sphere at the plate, the same configuration that ends every
  plate-stick failure (E0022).
- Case b has no baseline from either engine; ask Chris whether the C code at
  3D case b, or comparing methods with each other, should stand in.
- Wait for Chris on: transitive sticking or option 4 for the stuck-free
  pairs; how to treat the nudge's rare overlaps (the notes predict them);
  the Figure 1 comparison spec.
