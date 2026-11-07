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
- Status: open. Nov 6: option 3 (elastic window) tried and does not help;
  option 1 (nudge) survives every stalled condition so far. See Current state.

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
  `method/elastic-window-v003`, v_el = 0.03). Tried Nov 6. Survives no
  better than the unmodified engine at 6 of 8 stalled conditions: slow
  stretches with 1e7 to 1e8 collisions slower than 1e-10, then overlaps or
  CPU caps. v_el = 0.03 does worse than 0.01 in 3D. Passes bulk physics at
  the shallow condition and at the deep Gamma 3.5 f* 0.5 condition (2 of 3
  seeds; the third run sits in a different pattern state). Not a candidate.
- **Option 1, position nudge** (`method/nudge`). Tried Nov 6. Completes 120
  cycles at all 8 stalled conditions, and 1000 cycles at every condition
  finished so far (E0008). Adds 1e-15 to 1e-13 of the plate's work. Passes
  bulk physics against the unmodified engine (shallow) and the C code
  (deep Gamma 3.5 f* 0.5, 3 seeds). Remaining slow stretches come from
  lasting pair contacts in the dense Gamma 5 layers, not the plate. The
  leading candidate, but Figure 1 comparison and 3D bulk checks aren't
  done, and it is the 'baseline only' option in the notes.
- Options 2 and 4 change the restitution law (e = 0 capture), so they need
  Chris's go-ahead before implementation.

## Current state

The engine on `main` is the hardened import described in `README.md`: it
fails loudly on physical violations, matches an all-pairs reference, and
restarts bit-for-bit, but stalls or overlaps in lasting contact. Nov 6
showed this is wider than the Gamma = 5 cases: at 3D N = 60000 it fails in
the first landing at Figure 1 case b (overlap at seed 1, frozen time at
seed 2; E0011, E0012) and overlapped at cycle 567 of case g (seed 2,
E0017), always at drive phase 0.90 to 0.94.

It also runs 2D (spheres confined to a plane, `dim=2`).

Contact methods, on branches with worktrees under
`sequel-data/worktrees/` (merging needs Chris):

- `method/nudge` (b608fef): survives everything tried so far. 120 cycles
  at all 8 stalled conditions at seeds 1, 2, 3 (E0003, E0016); 1000
  cycles at 6 of them (E0008; two Gamma 5 f* 0.3 runs, depths 10 and 15,
  are inside long slow stretches at cycles 162 and 246 and still running).
  3D N = 60000: 120 cycles at cases b and g and Gamma 5 (E0013). Nudge energy 1e-15 to 1e-13 of plate work.
  Audit failures happen only in many-collision cycles and are always
  energy losses, never gains. Bulk physics passes against the unmodified
  engine (2D shallow), the C code (2D Gamma 3.5 f* 0.5 depth 15, 3
  seeds), and provisionally at 3D case g (2 of 3 seeds; the third fails
  plate contact, as does the unmodified engine's own control).
- `method/elastic-window` (90ee7d2) and `-v003` (b1e4086): not a
  candidate; no better survival than the unmodified engine.

What the remaining slow stretches are: with the plate fixed by the nudge,
they are lasting pair contacts inside dense Gamma 5 layers (millions of
pair collisions slower than 1e-10, a few thousand plate ones).

Referee findings to bring to Chris (not edits; the referee is his):

- The 1998 C code does not give 1020-cycle baselines at 2D Gamma 3.5
  f* 0.3 depth 15 or Gamma 5 f* 0.3 depth 5 (aborts at 20 to 61 cycles,
  3 seeds each); the 30-cycle pilot overstated coverage (E0009).
- The bulk pass rule's block spread from one run understates run-to-run
  spread for horizontal energy (2D, E0007) and plate contact (3D case g,
  E0017), so unmodified-engine controls fail or nearly fail it.
- At deep layers the bulk quantities depend on the selected pattern
  wavelength (2D Gamma 3.5 f* 0.5 depth 15: three wavelengths across the
  box versus two; E0010). `sequel-data/runs/tools/wavelength.py` reports it.

Tools (not in git): `sequel-data/runs/launch.sh` starts a long_contact run
in the background and records it in `active.jsonl`; `runs/tools/` has the
queue scripts and the evidence helpers (`surv.py`, `cpu_session.py`,
`wavelength.py`).

## Next

- Collect the runs left going (E0008 two runs, E0014 seed-1 case-g
  baseline; see `sequel-data/runs/active.jsonl`) and record E0008's outcome.
- If the E0014 seed-1 baseline reaches 1020 cycles, judge the case-g nudge
  runs against a full 10-block baseline.
- Wait for Chris on options 2 and 4 (they change the restitution law), the
  Figure 1 comparison spec, and how the pass rule should treat run-to-run
  spread and pattern state. Meanwhile: more nudge bulk checks where a
  baseline runs, and characterize the lasting pair contacts that still
  slow the nudge.
