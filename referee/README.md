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

    Differences of the means, sequel relative to C:

    | point | height | thickness | vertical energy, temperature | horizontal energy, temperature | plate contact | take-off and landing |
    | --- | --- | --- | --- | --- | --- | --- |
    | Gamma 3.5, f* 0.3, depth 5 | -0.3% | -1.6% | -1.5%, -3.6% | -7.2%, -7.7% | +4.9% | same to 1/32 cycle |
    | Gamma 3.5, f* 0.5, depth 5 | 0.0% | +0.7% | 0.0%, +2.5% | +1.5%, +3.0% | -1.4% | same to 1/32 cycle |
    | Gamma 3.5, f* 0.5, depth 10 | +0.9% | +2.1% | +1.3%, +5.2% | +9.4%, +8.3% | +0.1% | identical |
    | Gamma 5, f* 0.5, depth 5 | +0.4% | +1.5% | -0.1%, +0.1% | +1.3%, +2.7% | -3.6% | identical |

    How big a difference is just noise: the C code at Gamma 3.5, f* 0.3,
    depth 5 was run 60 cycles and measured in 10-cycle windows. After
    cycle 20 the window means scatter (standard deviation over mean) by
    0.7% in height, 0.8% in vertical energy, 2.3% in vertical
    temperature, 3.3% in thickness, 4.1% in horizontal energy and
    temperature, and 4.6% in plate contact. At that point every sequel
    difference in the table is within two of those standard deviations
    (the largest, vertical energy, at about two). Settling: that run's
    values rise through cycles 10 to 20 and then fluctuate without a
    trend, so 20 cycles of settling looks sufficient there; across the
    four points, 4 of 56 drift flags fired, about what chance gives at 95%.
    The scatter has only been measured at this one point.

    Pass rule (decided by Chris, Nov 5; final form): measure the method
    for 100 cycles after 20 of settling. Run the baseline once, settle 20
    cycles, then measure 10 consecutive 100-cycle blocks (`bulk.py
    baseline --cycles 100 --blocks 10`). A method passes a quantity when
    its 100-cycle mean is within 3.61 of the baseline's block standard
    deviations of the baseline mean (`bulk.py judge`). 3.61 keeps the
    chance that a method identical to the baseline fails any of the seven
    quantities at 5%; it allows for the method's own scatter and for the
    uncertainty of a standard deviation from ten blocks (the threshold
    for other block counts is in `bulk.py`). One long run with blocks,
    rather than independent runs, because the layer forgets its state
    quickly: with four independent runs per code, block means within a run
    predicted the spread between runs, and one run pays for settling
    once.

    Validation (Gamma 3.5, f* 0.3, depth 5): a 1020-cycle C baseline (34 s)
    against four independent sequel runs and four independent C runs. All
    eight pass every quantity; the largest deviation is 1.15 standard
    deviations. What the test can detect there, in percent of the mean:
    height 1.8%, vertical energy 4.3%, plate contact 6.5%, thickness 8.7%,
    vertical temperature 10%, horizontal energy and temperature about 30%.
    It is sharp for height and vertical energy and weak for horizontal
    motion.

    How the rule was reached (Nov 5): a first version judged one 10-cycle
    method window against 10-cycle windows of the baseline at 2 standard
    deviations. Its first use failed sequel on two quantities that a
    longer measurement showed agree; 10-cycle windows are too short for
    the slow fluctuations, and testing seven quantities at 2 standard
    deviations fails identical methods about 30% of the time.

    Cycle-to-cycle variation in each code (Gamma 3.5, f* 0.3, depth 5,
    cycles 20 to 60, means of each 2-cycle period, 20 periods each):

    | quantity | C: sd of period means | sequel: sd | ratio | period-to-period correlation, C / sequel |
    | --- | --- | --- | --- | --- |
    | height | 1.1% | 1.3% | 1.23 | -0.29 / 0.17 |
    | thickness | 5.4% | 4.5% | 0.81 | 0.08 / 0.23 |
    | vertical energy | 2.2% | 2.5% | 1.12 | 0.06 / 0.47 |
    | vertical temperature | 6.4% | 8.0% | 1.24 | -0.13 / 0.28 |
    | horizontal energy | 7.1% | 12.5% | 1.82 | 0.11 / 0.44 |
    | horizontal temperature | 7.1% | 12.4% | 1.77 | 0.11 / 0.43 |
    | plate contact | 6.0% | 4.8% | 0.79 | 0.11 / -0.18 |

    That looked like a difference in horizontal motion, so it was
    checked (Nov 5) with four runs of each code, 100 measured cycles each
    after 20 of settling. It isn't one: the variation overlaps completely.

    | quantity | C: sd of period means, 4 runs | sequel, 4 runs | period-to-period correlation, C / sequel |
    | --- | --- | --- | --- |
    | height | 1.0 to 1.2% | 1.2 to 1.3% | -0.15 to 0.32 / 0.03 to 0.20 |
    | thickness | 4.2 to 6.6% | 4.5 to 7.1% | 0.21 to 0.53 / 0.20 to 0.69 |
    | vertical energy | 2.4 to 2.9% | 2.1 to 3.4% | 0.19 to 0.66 / 0.24 to 0.74 |
    | vertical temperature | 8.1 to 8.5% | 7.2 to 10.1% | 0.06 to 0.48 / 0.08 to 0.47 |
    | horizontal energy | 12 to 18% | 10 to 17% | 0.35 to 0.70 / 0.46 to 0.71 |
    | plate contact | 4.2 to 5.1% | 4.3 to 4.8% | -0.09 to 0.38 / 0.01 to 0.17 |

    The first C run happened to be quiet in horizontal motion over its 40
    cycles. The C code's plate collision (`collide.c`, `ballwall`) also
    rules out the suggested cause: the snap only sets the height to the
    plate surface; horizontal velocity changes only through the same Walton
    friction update sequel uses, with the same crossover speed
    (VMIN = sqrt(g D)).

    What this does show: horizontal energy (and to a lesser degree
    thickness and vertical energy) fluctuates slowly in both codes, with
    period-to-period correlation up to 0.7. A 10-cycle window holds barely
    more than one independent sample of it, so a 10-cycle measurement of
    horizontal energy is uncertain by more than 10%. Even 100-cycle means
    differ between runs: horizontal energy 0.38 to 0.43 in C and 0.40 to
    0.43 in sequel (about 5% spread), against about 0.3% for height, 0.5%
    for vertical energy and 1% for thickness. The two codes' 100-cycle
    means overlap on every quantity.

    So measurement windows have to be longer than 10 cycles, at least for
    horizontal quantities, and the allowance between models should be set
    from the spread of long-run means across independent runs of one
    code, which is what the four-run table measures.

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
