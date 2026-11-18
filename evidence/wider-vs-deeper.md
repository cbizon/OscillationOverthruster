# Wider versus deeper (Nov 17, item 3)

No new runs. Numbers are in `wider-vs-deeper.json` (built by
`sequel-data/runs/tools/wider_deeper.py`). **Measured** means taken from the
ten no-friction fast loops in the paper's box (E0060: L 100, depth 5.42,
N 60000, one seed, 213 steps of 25 cycles, ten jobs sharing the machine, so
a little high). Everything else is **scaled** and says how.

## What a loop costs

Per loop of the fast pass (Gamma 1.7 to 7.0 and back), no friction.
The friction models cost more: the nudge's price is about 2 to 3 times
these (E0065 is running and will measure it).

| f\* | paper's box (measured) | wider, L 150 | wider, L 200 | deeper x2, L 100 | deeper x2 and L 200 |
| --- | --- | --- | --- | --- | --- |
| 0.84 | 8.4 | 19 | 34 | 32 | 128 |
| 0.57 | 11.7 | 26 | 47 | 45 | 178 |
| 0.44 | 13.9 | 31 | 56 | 53 | 211 |
| 0.33 | 18.1 (projected, 209 of 213 steps) | 41 | 72 | 69 | 275 |
| 0.27 | 23.5 (projected, 93 of 213 steps) | 53 | 94 | 89 | 357 |
| ten loops | 145 | 326 | 580 | 551 | 2200 |

CPU-hours. How scaled:

- **Wider**: cost per sphere per cycle does not change with width (measured
  equal at L 50 and L 100, E0050), so cost goes as N, i.e. (L/100)^2:
  2.25 times for L 150, 4 times for L 200 (N 240000). Memory about 0.8 GB
  per loop at L 200. Every no-friction loop at L 200 stays under the
  100 CPU-hour per-run limit (f\* 0.27 just: 94); nudge loops at L 200
  would not at f\* 0.50 and below (their price times four is 106 CPU-hours at 0.50).
- **Deeper**: twice the spheres, and each sphere costs more because the
  layer is denser and collides more. The factor 3.8 for twice the depth is
  from 2D runs at depths 5 and 10 (plan section 0b), **not measured in 3D**.
- **Deeper and wider together** multiplies the two: about 15 times; every
  loop passes the per-run limit.

## How many wavelengths fit

Wavelength from the experimental relation lambda/H = 1.0 + 1.1 f\*^-1.32
(Umbanhowar and Swinney 2000, with friction), so it grows in proportion to
the depth H. **Scaled from experiment**; in our box the measured wavelength
at the first strong pattern is 20 to 33 D (rings 3 to 5), which the box
quantises to 100/k (33, 25, 20 ...).

| f\* | lambda at depth 5.42 | across L 100 | across L 150 | across L 200 | lambda at depth 10.84 | across L 100 | across L 200 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.84 | 12.9 | 7.7 | 11.6 | 15.5 | 25.8 | 3.9 | 7.7 |
| 0.65 | 15.9 | 6.3 | 9.4 | 12.5 | 31.9 | 3.1 | 6.3 |
| 0.57 | 17.9 | 5.6 | 8.4 | 11.2 | 35.9 | 2.8 | 5.6 |
| 0.44 | 23.0 | 4.3 | 6.5 | 8.7 | 46.1 | 2.2 | 4.3 |
| 0.38 | 26.8 | 3.7 | 5.6 | 7.5 | 53.6 | 1.9 | 3.7 |
| 0.33 | 31.2 | 3.2 | 4.8 | 6.4 | 62.4 | 1.6 | 3.2 |
| 0.30 | 34.6 | 2.9 | 4.3 | 5.8 | 69.3 | 1.4 | 2.9 |
| 0.27 | 39.0 | 2.6 | 3.9 | 5.1 | 78.0 | 1.3 | 2.6 |

## Which frequencies each opens up

Taking three wavelengths across the box as the least that lets a pattern
choose its own wavelength (it is also where the amplitude used until
tonight stopped counting):

- **Paper's box**: f\* 0.31 and up. f\* 0.30 and 0.27 are already under
  three.
- **Wider, L 150**: down to f\* 0.22. **L 200**: down to f\* 0.17, so the
  whole squares side (f\* below about 0.33, where flat-to-squares
  hysteresis is expected) with room, and the allowed wavelengths are twice
  as finely spaced (200/k).
- **Deeper x2 in the same box**: only f\* 0.62 and up (0.84, 0.74, 0.65 of
  our ten). It closes the low frequencies rather than opening anything,
  because the wavelength doubles with the depth.
- **Deeper x2 at L 200**: the same frequencies as the paper's box today
  (f\* 0.31 and up), at about 15 times the cost.

So deeper and wider are not alternatives: going deeper at the same
frequencies needs the box widened in proportion. Wider alone is the
cheaper step and is the one that opens the frequencies where the expected
hysteresis is.

## What each should do to hysteresis (expectations, not results)

- **Deeper**: experiments report the flat-to-pattern gap growing with depth
  and shrinking with f\* (Umbanhowar and Swinney 2000). A larger gap is
  easier to tell from ramp lag with one loop, whose resolution at 25 cycles
  a step is about 0.15 in Gamma (E0057). But in a box of fixed width it
  pushes the frequencies where the gap is largest out of the box.
- **Wider**: no change to the bifurcation itself is expected; it removes
  what the box adds.
  - In a box that holds three or four wavelengths, only wavelengths 100/k
    fit. A pattern whose own wavelength lies between two allowed ones is
    strained; that can move the onset and the offset, and it can make or
    hide a gap (a pattern held at a wrong wavelength on one branch).
  - A wide box lets the two states coexist in domains separated by fronts,
    which is how an extended system goes from one branch to the other. In
    a small box the whole layer tends to switch at once, which sharpens
    apparent transitions.
  - Tonight's redrawn figures show structure the size of the box that
    the earlier amplitude did not count (next section). A wider box would
    show whether it is box-sized because of the box.
- What the fast pass already shows (one seed, fast rate, no friction): at
  the first onset, the way down stays above the way up over a range that
  widens as f\* falls: none above 0.1 D at f\* 0.50 to 0.84; Gamma 2.15
  to 2.3 at 0.44 (largest 0.26 D); 1.9 to 2.1 at 0.38 (0.48 D); at 0.33 still
  patterned at 1.9 on the way down. This is the trend the experiments
  report, and also what a pattern that needs time to grow would give.

## Where the box holds under three wavelengths (measured)

Steps where the strongest mode over every wavelength is the whole box (100
D) or half the box (50 D), with at least 0.1 D of amplitude. All ten
figures in `fastpass-figures/` are redrawn with these wavelengths included
(solid line), the earlier amplitude dashed and the two long rings dotted,
with a small triangle at each such step.

| f\* | way up | way down |
| --- | --- | --- |
| 0.84 | 4.25 to 4.65 | none |
| 0.74 | 4.1 to 7.0 | 3.9 to 6.95 |
| 0.65 | 4.05 to 4.2 | none |
| 0.57 | 4.0 to 4.35 (and 7.0) | single steps 5.75 to 6.95 |
| 0.50 | 4.0 to 4.4, most of 5.1 to 7.0 | 4.6 to 6.95 |
| 0.44 | 4.25 to 4.45, 5.15 to 7.0 | 4.25 to 6.95 |
| 0.38 | 4.7 to 7.0 | 4.45 to 6.95 |
| 0.33 | 1.9 (one step), 5.05 to 7.0 | 4.7 to 6.95 |
| 0.30 (running) | 1.85 to 1.9, 5.05 to 7.0 | 6.9 to 6.95 so far |
| 0.27 (running) | most steps from 2.65 to 6.3 so far | not reached |

By the experimental relation the pattern's own wavelength already fits
fewer than three times at f\* 0.30 and 0.27 at onset.

What the box-sized structure is, at the two places the checker named
(`field-f0.84-g4.5-up.png`, `field-f0.50-g4.0-up.png`, two consecutive
cycles at phase 0 and 0.5, red up, blue down): the whole-box Fourier
component changes sign every cycle at the same phase. Part of the layer
bounces on even cycles and the rest on odd cycles, with a front between
them: a straight front across the box at f\* 0.50, Gamma 4.0, and one
patch in a corner at f\* 0.84, Gamma 4.5. This is what "flat with kinks"
between the half-frequency and quarter-frequency patterns looks like in
experiments (Melo et al. 1995); I have not checked the period of the
bouncing beyond this sign change. At f\* 0.84 it appears only on the way up
(`field-f0.84-g4.5-down.png` has no such front).

## Short runs that would replace the scaled numbers

1. **Cost against depth**: 20-cycle holds at depth 10.84 (N 120000, L 100),
   no friction, f\* 0.57, at Gamma 2.0, 3.0 and 5.0. About 0.5 CPU-hours.
   Replaces the 2D factor 3.8.
2. **Cost against width**: the same three holds at L 200, depth 5.42
   (N 240000). About 0.5 CPU-hours. Checks cost going as N and the memory.
3. **Wavelength against depth in this model**: one 100-cycle hold at depth
   10.84, L 200, f\* 0.57, Gamma 3.0 (5.6 wavelengths by the relation).
   About 3 CPU-hours on the scaled price.
4. **The box's effect on onset and offset directly**: the f\* 0.44
   no-friction loop over the first onset only (Gamma 1.7 to 3.0 and back,
   53 steps) at L 200, against tonight's at L 100. About 12 CPU-hours.
