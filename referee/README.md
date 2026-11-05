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
    decide. 2D here means spheres confined to a plane, the model of the
    1998 C code's 2D mode (decided by Chris, Nov 5): sphere masses and
    inertia, all centres on one plane. This engine runs it with `dim=2`
    (branch `engine-2d`).

    Pilot (Nov 5, L = 100, two starts each, 30 cycles, Gamma = 5 as a
    trial higher value, f* = 0.3 and 0.5): the baseline engine without
    contact handling stalls in most of this grid. It ran 30 cycles only
    at Gamma = 3.5 with depth 5 (both frequencies) or depth 10 at
    f* = 0.5, and at Gamma = 5 with depth 5 at f* = 0.5. Everything
    else stalled, mostly in the first few cycles; Gamma = 5, depth 5,
    f* = 0.3 lasted 14 and 20 cycles. Runs that work take 0.01 to 0.08 s
    per cycle.

    So the with/without comparison is only available for shallow layers.
    Decided (Chris, Nov 5): where this engine can't run, the baseline is
    the C code's approach (snap onto the plate after a plate hit), using
    the 1998 C code itself in its 2D mode (`DIMENSION 2`; the
    reproduction port in `grains_July23_1998/reproduction/src` builds with
    it). Its parameters are compile-time, so each grid point is its own
    build. It also aborts in some dense states, so some deep conditions
    may have no baseline.

    The script is `referee/c_baseline.py` (one grid point; seeds tried in
    order after an abort, every attempt kept). Its output has the same
    keys as `granular/export.py`, in sequel units and frame. Smoke test at
    Gamma = 3.5, f* = 0.5, depth 5: centre-of-mass height above the plate,
    by phase over cycles 20 to 30, agrees with this engine within 0.03 D.

    C pilot on the same grid (Nov 5, 30 cycles, seeds 16532, 1, 2): it
    completed every Gamma = 3.5 point, including depths 10 and 15 where
    this engine stalls, in 1 to 40 s each. At Gamma = 5 it completed only
    depth 5 (both frequencies); every depth 10 and 15 point aborted in its
    plate root finder (`detect.c` lines 787 and 840) within 2 to 11 cycles
    for all three seeds. So at Gamma = 3.5 the C code covers the deep
    layers; at Gamma = 5 deep layers have no baseline from either code,
    and the contact methods there can only be compared with each other
    and judged by the energy audit and smoothness across neighbouring
    conditions.

    Measurement tool: `referee/bulk.py`. `measure` reads either code's
    trajectory and gives, by phase over the response period (2 cycles by
    default) and as overall means: centre-of-mass height above the plate,
    layer thickness (spread of heights), kinetic energy per particle
    (vertical, horizontal), granular temperature (the same about the
    centre-of-mass velocity), and the fraction of particles touching the
    plate, with take-off and landing phases. It flags a quantity as
    drifting when its change across the window differs from zero at 95%.
    `compare` aligns two measurements on the best whole-cycle shift and
    reports differences.

    First comparison, sequel versus the C code (Nov 5, 2D, settle 20,
    measure 10, one start each), at the four points both codes run:

    | point | largest difference in a mean | take-off and landing |
    | --- | --- | --- |
    | Gamma 3.5, f* 0.3, depth 5 | horizontal energy 7% (others under 2%) | same to 1/32 cycle |
    | Gamma 3.5, f* 0.5, depth 5 | 2.5% (vertical temperature) | same to 1/32 cycle |
    | Gamma 3.5, f* 0.5, depth 10 | 9% (horizontal energy; others under 5%) | identical |
    | Gamma 5, f* 0.5, depth 5 | 2.7% (horizontal temperature) | identical |

    How big a difference is just noise: the C code at Gamma 3.5, f* 0.3,
    depth 5, run 60 cycles and measured in five 10-cycle windows, varies
    between windows by about 2% in centre-of-mass height, 4% in thickness
    and vertical energy. The differences above are of that size, so the
    two codes agree within the scatter of a single 10-cycle measurement.
    Small quantities (horizontal energy, about a tenth of the vertical)
    scatter more. Settling: that run's values rise through cycles 10 to
    20 and then fluctuate without a trend, so 20 cycles of settling looks
    sufficient there; across the four points, 4 of 56 drift flags fired,
    about what chance gives at 95%.

    So the acceptance tolerance should come from this window-to-window
    scatter, measured per condition, rather than a fixed percentage
    **[decide]**: for example, a method passes a quantity when its mean is
    within twice the baseline's window-to-window spread.
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
