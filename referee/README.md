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

Two parts: a quick one run on every candidate method, and a slow one run
rarely.

### 3a. Survival, energy and bulk physics (every candidate, every change)

- **Survival.** The Gamma = 5, f* = 0.44 case (N = 2400, L = 20) runs a
  stated number of cycles without stalling.
- **Energy audit.** Per cycle, the work done by the plate, the energy lost
  in collisions, and the change in the layer's energy balance to a stated
  tolerance. Any energy a method adds by fiat (a position snap, a velocity
  floor) is counted separately and must be zero or reported.
- **Bulk quantities across parameters.** At a grid of driving conditions
  (Gamma and frequency, including ones where the baseline engine never has
  long contacts), compare the method with the baseline engine, and with the
  reference C runs where they exist, on quantities that settle within a few
  cycles:
  - layer depth (thickness, for example the spread of heights);
  - centre-of-mass height, as a function of phase in the cycle;
  - total kinetic energy, and its vertical and horizontal parts, as a
    function of phase;
  - potential energy, and the phases at which the layer takes off from and
    lands on the plate;
  - collision rate.

  Each is averaged over cycles after a short transient, over several random
  initial conditions, so differences can be compared with run-to-run
  spread. Where the baseline works, the method must agree within that
  spread; disagreement means the contact handling is changing the physics.
  Where only the method runs (long contacts), the quantities should vary
  smoothly from the neighbouring conditions where both run.

### 3b. Patterns (infrequent)

The patterns themselves (stripes, squares, hexagons, flat) at a few
conditions, compared with the baseline and with Figure 1. Patterns take
many cycles to form, so this runs only when a method is a candidate to
become the default, or after a change that 3a can't rule out.

To decide:

- the number of cycles for survival;
- what "stalling" means in numbers (for example, events per unit simulated
  time above some multiple of the run's median);
- the energy balance tolerance;
- the parameter grid for 3a, the transient and averaging lengths, and the
  number of random initial conditions;
- which conditions 3b covers and how many cycles each needs.

## 4. Experiments (later)

Published observations for hysteresis and oscillons, and Chris's blind
rating of figures and movies mixed with controls. Defined when RQ2 and RQ3
start.

## The checker's brief

`checker.md` is the prompt for the morning checker session, which tries to
break each session's claims and reports on how running locally is working.
