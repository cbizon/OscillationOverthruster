# Referee

Human-only. What judges the program's work. The agent runs what's here and
never edits it. After any change, Chris records new hashes in
`approvals.json`.

## 1. Frozen engine tests (built)

`referee/tests/` holds copies of the engine's correctness tests as of
commit `8fd052b`: the plate-root solver against brute force and its edge
cases, an all-pairs reference event loop that must match event counts
exactly and states to 1e-8, and checkpoint-restart equivalence. Run:

```bash
uv run pytest referee/tests
```

About ten seconds. Every contact method must pass these unchanged. The
agent may add tests in `tests/`; those don't count as referee evidence.

## 2. Figure 1 comparison (to build with Chris)

Compares exported trajectories with the validated updated-C reference runs
for the seven Figure 1 conditions, using the evaluator in
`~/Projects/experiments/granular_mean` and the local reference bundle.

To decide:

- the exact command, and which of the evaluator's measures count;
- the tolerance for "no worse than the baseline engine", per measure;
- the valid span for the Gamma = 5 case, where the reference aborted in
  cycle 4-5;
- how long each condition takes locally, so the agent can budget it.

## 3. Long-contact test (to build with Chris)

The Gamma = 5, f* = 0.44 case (N = 2400, L = 20) must run a stated number
of cycles without stalling, with an energy audit showing the contact method
injects no energy.

To decide:

- the number of cycles;
- what "stalling" means in numbers (for example, events per unit simulated
  time above some multiple of the run's median);
- the energy audit: per cycle, the work done by the plate, the energy lost
  in collisions, and the change in the layer's energy must balance to a
  stated tolerance; any energy a method adds by fiat (a position snap, a
  velocity floor) is counted separately and must be zero or reported;
- the neighbouring conditions used to check that a method isn't tuned to
  this one case.

## 4. Experiments (later)

Published observations for hysteresis and oscillons, and Chris's blind
rating of figures and movies mixed with controls. Defined when RQ2 and RQ3
start.

## The checker's brief

`checker.md` is the prompt for the morning checker session, which tries to
break each session's claims and reports on how running locally is working.
