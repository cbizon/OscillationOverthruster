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
- Candidates, to be compared, not assumed:
  - a co-moving "stuck" state on the plate, with an explicit release
    condition when the plate decelerates below -g relative motion;
  - an inelastic-collapse cutoff (treat collisions closer together than a
    small time as fully inelastic, in the spirit of Luding's TC model);
  - the original C code's approach (snap onto the plate surface after a plate
    hit, 1e-9 root tolerance), as a baseline to understand, not adopt;
  - switching persistent contacts to a soft-sphere treatment.
- Status: open.

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

See RQ1's candidates. None tried yet.

## Current state

The engine is the hardened import described in `README.md`: it fails loudly
on physical violations, matches an all-pairs reference, and restarts
bit-for-bit, but stalls in the Gamma = 5 resting-contact regime, and in 2D
at depths 10 and 15 for most of the grid.

It also runs 2D (spheres confined to a plane, `dim=2`).

The referee (`referee/README.md`) has:

- the frozen tests;
- a script that runs the 1998 C code in 2D as the baseline where this
  engine stalls (it covers Gamma = 3.5 at all depths; at Gamma = 5 it also
  aborts at depths 10 and 15);
- the bulk-quantity measurement with its pass rule.

In 2D, this engine and the C code agree on bulk physics wherever both run.

Not built yet: the stall detector, the energy audit, the 3D baselines, the
Figure 1 comparison.

## Next

Finish the referee with Chris: the energy audit and stall detector, then
one 3D baseline to measure its cost. Scheduled sessions start after he
approves it.
