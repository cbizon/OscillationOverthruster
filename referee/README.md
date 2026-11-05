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
- **Bulk quantities across parameters.** Compare macroscopic quantities
  with and without the contact method in this same code (so the only
  difference is the contact handling), and with the reference C runs where
  they exist:
  - layer depth (thickness, for example the spread of heights);
  - centre-of-mass height, as a function of phase in the cycle;
  - total kinetic energy, and its vertical and horizontal parts, as a
    function of phase;
  - potential energy, and the phases at which the layer takes off from and
    lands on the plate.

  Not collision rate: methods model the resting state differently (long
  contacts in some, many tiny collisions in others), so the rate describes
  the method, not the physics.

  Each run settles for 20 cycles and is measured over the next 10, averaged
  over those 10. One initial state per condition: chaotic mixing at the
  particle level forgets the initial state quickly. When the baseline grid
  is first run, check the 10 measured cycles for a remaining trend; if
  there is one, lengthen the settling time.

  Where the baseline works, the method must agree with it; disagreement
  means the contact handling is changing the physics. Where only the method
  runs (long contacts), the quantities should vary smoothly from the
  neighbouring conditions where both run.

  The grid, coarse first:
  - **2D, as a fast filter.** Gamma = 3.5 and a higher value in the
    subcritical pattern regime **[pick]**, each at a low and a high
    frequency **[pick]**, at depths 5, 10 and 15 particle diameters: 12
    runs. 2D can behave slightly differently, so it filters but doesn't
    decide. The engine runs 2D disks with `dim=2` (branch `engine-2d`).

    Pilot (Nov 5, L = 100, two starts each, 30 cycles, Gamma = 5 as a
    trial higher value, f* = 0.3 and 0.5): the baseline engine without
    contact handling stalls in most of this grid. At Gamma = 3.5 it ran
    only at depth 5 (both frequencies) and at depth 10, f* = 0.5 for one
    of two starts; depths 10 and 15 otherwise stalled in the first or
    second cycle. At Gamma = 5 it stalled everywhere except depth 5,
    f* = 0.5. So the with/without comparison is only available for
    shallow layers; deeper conditions need another baseline **[decide]**.
    Runs that work take 0.01 to 0.13 s per cycle.
  - **3D, N = 60000, L = 100, depth 5.42.** Gamma = 3 and a high Gamma
    **[pick]** at the stripe frequency, plus Gamma = 5, f* = 0.44 (the
    stuck case, method only).

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
