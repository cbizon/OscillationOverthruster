# Direction: sequel

Human-only. The agent reads this file and never edits it. Items marked
**[decide]** are proposals awaiting Chris's decision.

## The question

Make the event-driven simulation of vertically oscillated granular layers
(Bizon et al., PRL 80, 57, 1998) handle long-lasting contacts, in particular a
sphere resting on a plate that accelerates upward faster than gravity, without
non-physical fixes, and use it for experiments that were too slow in the
1990s: hysteresis in the transitions between patterns as the driving is
ramped up and down, and localized excitations (oscillons).

The two are expected to feed each other. Different ways of handling contacts
may change what the experiments show; experiments that are sensitive to the
contact method are evidence about the method. So this is one program, not a
sequence of phases.

## In scope / out of scope

- In: methods for long-lasting contacts (plate and particle–particle);
  correctness and performance work on the engine; hysteresis and oscillon
  experiments; comparison with the 1998 results and with the experimental
  literature.
- Out without asking: changing the collision model or its constants from the
  paper (restitution law, friction, rolling limit); adding physics the paper's
  model doesn't have (interstitial gas, cohesion); changing the reference data.

## What the program produces

- Contact-handling methods in the engine, each on its own branch until Chris
  approves merging it, with the evidence for and against.
- Experiment results (figures, movies, measured quantities) with the run
  configuration and code version that produced them.
- A short running report in `PROGRAM.md`.

Large outputs live outside git under `~/Projects/experiments/sequel-data/`;
`evidence/` records their paths and checksums.

## The referee

The agent can run these; it can't edit them. Details in `referee/`.

1. **Frozen engine tests**: copies in `referee/tests/` of the current
   correctness tests (an all-pairs reference event loop that must match event
   counts exactly and states to 1e-8; checkpoint-restart reproducibility; the
   plate-collision solver against brute force). Changes to `tests/` don't
   affect these.
2. **Figure 1 comparison**: the benchmark evaluator in
   `~/Projects/experiments/granular_mean` compares exported trajectories with
   the validated updated-C reference runs for the seven Figure 1 conditions
   (local bundle, 2.6 GB). Conditions where the reference itself is limited
   (the Gamma = 5 case aborted in cycle 4–5) are judged only over the valid
   span.
3. **Long-contact test**: the Gamma = 5, f* = 0.44 case (N = 2400, L = 20) must
   run a stated number of cycles **[decide: how many]** without stalling, with
   an energy audit showing no energy injected by the contact method.
4. **For experiments**: published experimental observations where they exist
   (the hysteresis and oscillon experiments of the 1990s), and Chris's blind
   rating of figures and movies, mixed with controls.

## Claim classes and their evidence

| Class | Required evidence | Forbidden evidence |
| --- | --- | --- |
| contact method works | frozen tests pass; Figure 1 agreement no worse than the baseline engine on every valid case; long-contact test passes; energy audit | tests the agent wrote itself as the only evidence; changed tolerances or time steps that weren't applied to the baseline too |
| physical result (a phenomenon occurs, a boundary lies here) | reproduced with at least two contact methods, or shown insensitive to the method; at least three random initial conditions; ramp-rate or run-length check where relevant; comparison with experiment where one exists | a single run; a single contact method; parameters chosen after seeing which ones show the effect |
| performance | timings on stated hardware with the same inputs for both versions | timings from different machines or problem sizes |

When a claim falls under several classes, the strictest rule applies.

## Known ways this goes wrong

For the checker to try against every claim:

- **Energy injection.** A contact method that quietly adds energy (the
  removed plate floor did exactly this). Check the energy audit.
- **Tuned to the test case.** A method that works at Gamma = 5, f* = 0.44 and
  fails at other driving; check neighbouring parameters.
- **Agreement from tolerances, not physics.** Figure 1 agreement improved by
  loosening a tolerance, changing output sampling, or shortening the
  comparison window.
- **Easy cases only.** Claims tested only on conditions without long contacts.
- **Contact-method artifacts read as physics.** A pattern, transition, or
  oscillon that appears with one contact method and not another.
- **Unequilibrated results.** Measurements taken before the layer forgot its
  initial state.
- **Silent substitution.** A slow calculation replaced with a cheaper
  approximation without saying so.

## Acceptance bar **[decide]**

Proposed: a contact method is ready to become the default when it meets the
"contact method works" evidence on all seven Figure 1 conditions and runs the
Gamma = 5 case for the agreed number of cycles at no more than twice the
baseline cost per event. A physical result is ready to report when it meets
its evidence class and Chris has rated the figures.

## Autonomy **[decide]**

- May, without asking: implement and compare contact methods on branches; run
  experiments within budget; read the literature; add tests in `tests/`;
  improve performance without changing results.
- Must ask first: changing the paper's collision model or constants; merging
  a contact method into the main branch; any single run expected to exceed
  the per-run budget; anything irreversible.
- May never: edit this file, `budgets.yaml`, `referee/` or `approvals.json`;
  change the reference data; delete results.

## Budgets

Limits live in `budgets.yaml` (human-only). The agent warns in its session
summary at 50% and 80%, and stops spending at 100% until Chris raises the limit.

## Cadence

- Sessions: locally on Chris's Mac, as a Claude Code (Code tab) scheduled task
  that runs only on this computer, **[decide: when and how long]**. Proposed:
  11 pm to 5 am. The Mac must be awake with the app open.
- Long simulations run as background processes with checkpoints, so they can
  continue between sessions; sessions pick up finished runs.
- Running locally is an experiment in itself: every session records its run
  conditions (see `CLAUDE.md`), and the checker reports on them, so we can
  decide from evidence whether to move to Sterling or Hatteras.
- Morning: a prepared debrief, as for miner2049er.
