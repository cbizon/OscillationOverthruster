# Phase diagram plan

Written in the session of 2026-11-13 for the instruction of that date. A plan
only: the sweep has not been started. Numbers come from tonight's pilots and
earlier runs; each is in the evidence file named beside it.

Terms used throughout:

- **Gamma**: peak plate acceleration over g. **f\***: drive frequency times
  sqrt(H/g), H the layer depth. **Depth**: layer depth in particle diameters
  (5.42 in 3D, the paper's; 5, 10, 15 in 2D).
- **The three engines**:
  - *nudge*: the paper's model with friction, plus the position nudge
    (`method/nudge`);
  - *frictionless*: the unmodified engine with friction switched off
    (`method/mu0-unmodified`), the comparison model approved for this purpose;
  - *baseline*: the unmodified engine with friction, where it runs.
- **Ramp**: Gamma changed in small steps at fixed f\*, holding each value for
  a set number of drive cycles. **Loop**: a ramp one way and back.
- **Hold**: a long run at one fixed Gamma.

## 1. What tonight's pilots change

Four things the plan is built around. All are from one seed and short runs, so
they shape the plan and are not results.

- **The frictionless engine runs everywhere tried, cheaply.** 29 of 29 pilot
  runs from Gamma 2 to 7 completed with no slow stretch, at about a third of
  the nudge's cost in 3D (`E0050-results.json`). It is not stall-free,
  though: one of tonight's 39 frictionless baseline runs stalled
  (`E0046-results.json`).
- **Both engines with friction stop just below the pattern onset.** At
  Gamma 2.0 to 2.2 the layer spends most of the cycle on the plate. There the
  nudge is 6 to several hundred times slower than at Gamma 3,
  and the baseline does not run at all. In a 2D ramp down from Gamma 3.0 the
  nudge got to 2.15 and the baseline to 2.25; the pattern had died away by
  about 2.25 to 2.3 (`E0052-results.json`). A hysteresis loop at onset has to
  turn around in exactly this range.
- **A pattern can be told from a flat layer automatically; stripes cannot yet
  be told from squares in runs of 1000 cycles.** On the seven labelled
  Figure 1 reference runs the identifier is right 7 of 7. On our own 1000-cycle
  stripe runs it calls 4 of 8 stripes, because the stripes still carry
  defects (`E0051-results.json`).
- **Ramps work without touching the engine or the referee.** A ramp step
  with Gamma unchanged reproduces a continuous run bit for bit, and the
  energy audit stays clean across steps (`E0052-results.json`).

## 2. What is known from experiment and earlier simulation

Read tonight through a literature check (arXiv full texts and abstracts,
paraphrased; I did not open the journal versions). To be re-read before any
comparison is reported.

- **Sequence with Gamma** (Melo, Umbanhowar, Swinney, PRL 75, 3838, 1995):
  flat; squares or stripes at half the drive frequency from Gamma about 2.4;
  hexagons from about 3.9; flat with kinks; squares or stripes at a quarter
  of the drive frequency from about 5.7; hexagons again; disorder from
  about 7.6.
- **Squares or stripes**: squares at low frequency, stripes at high, changing
  over at f\* about 0.33 (Umbanhowar and Swinney, Physica A 288, 344, 2000).
- **Hysteresis**: flat to squares is hysteretic, flat to stripes little or
  not at all. The sizes disagree between papers:
  - about 20% in Gamma (Melo 1995);
  - onset near 2.6 going up, back to flat near 2.2 going down, the gap
    shrinking with f\* and growing with depth (Umbanhowar and Swinney 2000);
  - under 1% for squares in stainless steel (Goldman, Swift, Swinney, PRL
    92, 174302, 2004).
- **Ramp rate used in experiment**: Gamma changed by about 0.002 per drive
  cycle, about 20 ramps averaged (Umbanhowar and Swinney 2000).
- **Wavelength**: lambda/H = 1.0 + 1.1 f\*^(-1.32) (same paper).
- **Without friction** (Moon, Swift, Swinney, PRE 69, 031301, 2004, abstract
  only): onset about 30% lower in acceleration, and only stripes form;
  squares and hexagons need friction. A frictionless simulation at f\* 0.42
  found onset at Gamma 2.15 (Bougie et al., PRE 71, 021301, 2005), from
  separate runs at each Gamma, 400 cycles to settle and 100 measured.
- **Not found**: any simulation that measured the flat-to-squares hysteresis
  or its dependence on ramp rate. The oscillon paper (Nature 382, 793, 1996)
  and the 1998 PRL were not readable tonight.

What this means for the plan:

- The frictionless phase diagram is expected to differ from the paper's:
  lower onset, stripes only. A difference between the nudge and the
  frictionless engine is therefore not by itself evidence about the nudge.
  The check on the nudge is the baseline, which has the same model.
- The hysteresis worth finding is at flat to squares, f\* below about 0.33,
  with friction. That is the hardest corner for the engines we have (item 2
  of section 1).

## 3. The grid

### 3D (depth 5.42, the paper's layer)

- **Box**: L = 100, N = 60000, as in the paper and the referee.
  - The reference runs hold 2.8 to 5.1 wavelengths at L = 100: wavelength
    35 at f\* 0.27, 20 at 0.44, 24 at 0.38 (Gamma 4), and 35, 19, 24 for the
    three quarter-frequency cases (`E0051-results.json`).
  - L = 50 would hold 1.4 to 2.6 wavelengths. Too few to name a pattern, and
    the box would pick the wavelength. Cost per particle is the same at
    L = 50 and L = 100 (0.11 ms per particle per cycle, frictionless), so a
    smaller box saves a factor of four and nothing more. Not proposed.
- **f\***: 0.27, 0.33, 0.38, 0.44, 0.60, 0.84. These include Figure 1's
  values, the expected squares-to-stripes changeover (0.33), and one value
  in the gap.
- **Gamma**: not a grid of separate runs. Covered by ramps:
  - onset loops, Gamma 1.7 to 2.7 (frictionless) or 3.0 down to the lowest
    value the engine reaches (with friction), steps of 0.05;
  - a scout loop above onset, 2.7 to 7.0, steps of 0.1;
  - holds at the seven Figure 1 conditions, for the patterns themselves.

### 2D (the fast filter)

- **Depths** 5, 10, 15 and **f\*** 0.3, 0.5: the referee's grid, so the
  existing baselines apply.
- **Gamma**: 1.8 to 7.0 by ramp, steps of 0.05.
- **Box**: L = 200 at depth 5; L = 400 at depths 10 and 15.
  - Measured wavelength at f\* 0.3, depth 5 is 27 to 29 (14 or 15 across
    L = 400, `E0020-results.json`), close to the dispersion relation's 32.
    At f\* 0.5, depth 10 it is 29 to 31 (relation: 38).
  - The relation gives about 64 at depth 10 and 96 at depth 15 for f\* 0.3,
    so L = 400 holds about six and four.
- In 2D there are only waves or no waves; no squares, stripes or hexagons.
  2D gives onset, the change from half to quarter frequency, wavelength,
  and whether the engines agree.

## 4. Identifying a pattern

Tool: `sequel-data/runs/tools/pattern_id.py`. It works on the layer's height
field: mean particle height in bins of 2.5 D (2 D in 2D).

### Automatic

- **Pattern or flat: contrast.** Power of the strongest ring of wavenumbers
  over the median ring.
  - Reference runs: 45 to 127 for the six patterned cases, 1.9 for the flat
    case, at most 2.9 for shuffled fields. Our runs at stripe conditions: 60
    to 78 (Gamma 3) and 13 to 23 (Gamma 6).
  - Threshold 8, set before the reference runs were read.
  - Not usable in 2D as it stands: a flat 2D layer has box-sized sloshing
    modes that score high. In 2D the measure is the height field's
    root-mean-square amplitude inside a band around the expected wavelength.
- **Wavelength**: from the same ring. All eight of our Gamma 3 runs give
  19.4 to 19.8.
- **Temporal period** (half or quarter of the drive frequency): correlation
  of the field with itself one, two and four cycles later.
  - The rule I registered got 6 of 7 reference cases; the squares at a
    quarter frequency came out unclear.
  - A simpler rule (the smallest lag at which the correlation exceeds 0.5)
    gets 7 of 7, but I chose it after seeing the failure. It needs a test on
    data it was not chosen on.
- **Amplitude**, the quantity the hysteresis loops are drawn in:
  root-mean-square of the height field, averaged over the frames of each
  hold. See "Needs building".
- **Planform** (stripes, squares, hexagons): two measures on the field
  filtered to the pattern's wavelength.
  - Coherence: 1 when the pattern is locally parallel lines, 0 when it is a
    lattice. Reference: 0.79 and 0.53 for stripes, 0.07 to 0.23 for squares
    and hexagons.
  - Skewness: three wave directions at 60 degrees make peaks or cells.
    Reference: -0.82 and -0.60 for hexagons, at most 0.11 in size for the
    other patterned cases.
  - Our 1000-cycle stripe runs give coherence 0.42 to 0.65: between
    reference stripes and reference squares. Coherence rises with run
    length (0.21 to 0.27 at 120 cycles, 0.39 to 0.75 at 1020, Gamma 6). The
    reference stripes had 2700 cycles.
  - So the planform label is reported with its two numbers, never alone,
    and is trusted only where the numbers are far from the thresholds.

### For Chris to rate by eye

Top views of the height field at the frame of largest amplitude, blind,
mixed with controls (the labelled reference runs, and the other engine at
the same condition):

- the planform at every hold;
- anything the identifier puts between stripes and squares (coherence 0.3
  to 0.6);
- the flat-with-kinks range (Gamma about 4.5 to 5.5), which the identifier
  will call flat;
- oscillon candidates, when RQ3 starts.

### Needs building (no engine or referee change)

- **A field recorder.** The referee saves bulk quantities at 32 frames per
  cycle but not the height field, so tonight's amplitudes are single
  snapshots at the end of a hold and scatter by about 20%. A wrapper like
  `lc_counters.py` can save the height field's spectrum at every frame, and
  the field itself twice a cycle, without changing the run. About 13 MB per
  1000 cycles in 3D.
- **The 2D amplitude band** and the test of the temporal-period rule on new
  data.
- Thresholds are fixed in the registration before the sweep.

## 5. Hysteresis

### Protocol

- **Stepwise ramps**, `sequel-data/runs/tools/ramp.py`: each step starts
  from the previous step's final state with only Gamma changed, at a
  whole-cycle boundary where the plate is at its mean height. Each step is
  a complete referee run with its own audit.
- **Step** 0.05 in Gamma at onset, 0.1 in the scout.
- **Rates**: 25 cycles per step of 0.05 is the experimental rate (0.002 per
  cycle). Also 100 cycles per step; 400 where a loop is seen.
- **Direction**:
  - frictionless: up from flat (Gamma 1.7 or 1.8), then down;
  - with friction: down from a patterned state (Gamma 3.0), turn at the
    lowest step the engine completes, then up. The engines cannot start
    below onset.

### Defining a transition point

- The order parameter is the hold's mean amplitude A.
- **Gamma_up**: on the up branch, the first step where A exceeds the flat
  level by more than five times the flat level's scatter between holds, and
  stays above for the next two steps. **Gamma_down**: on the down branch,
  the last such step.
- Flat level and scatter are measured in the same run, from the steps at
  the low end of the ramp.
- Also reported: A squared against Gamma near onset. A continuous onset
  gives a straight line reaching zero at the threshold; a jump is a
  discontinuous one.
- **Hysteresis width** = Gamma_up minus Gamma_down.

### Telling hysteresis from a ramp that is too fast

A pattern takes time to grow and to die, longest near threshold. A ramp
faster than that draws a loop even when there is no hysteresis. Four checks,
all pre-registered:

1. **Rate.** Repeat the loop at 25, 100 and (where a loop is seen) 400
   cycles per step. A real loop keeps its width as the ramp slows. A lag
   shrinks toward zero.
2. **Stationarity within a hold.** Compare A in the first and second half
   of each hold. A step where they differ by more than the flat-level
   scatter is not settled, and the transition point is not taken from it.
3. **Two starts at one Gamma.** Pick a Gamma inside the loop. Hold it for
   1000 cycles starting from the up branch's state (flat) and from the down
   branch's state (patterned). Hysteresis means both stay as they started.
   If they converge, there is no hysteresis at that Gamma, whatever the
   ramps showed. This is the decisive check.
4. **Against seed scatter.** The width counts only if it exceeds the spread
   of Gamma_up and of Gamma_down across seeds (RQ2's own falsification
   rule).

What the pilot showed about this (2D, f\* 0.3, depth 5, frictionless, one
seed): up and down branches agree in layer thickness to 0.09 on average at
25 cycles per step and 0.055 at 100, with thickness running from 1.5 to 5
over the ramp. No loop at either rate, as expected without friction. It
also shows the snapshot amplitude is too noisy to place a threshold to
better than about 0.1 in Gamma, hence the field recorder.

### The risk

With friction, the loop has to go below the pattern's lower threshold while
the engine still runs. In the 2D pilot the margin was 0.1 in Gamma for the
nudge and none to spare for the baseline. In 3D at Gamma 2.2 the nudge ran
24 cycles at 45 seconds per cycle in a quarter-size box. If the 3D lower
threshold is near 2.2, as in experiment, the nudge may not reach it at
affordable cost. The 2D stage will show how the nudge's floor depends on
depth and f\* before any 3D time is spent on it.

## 6. Seeds and comparing engines

- **Three seeds** for every loop and hold that a statement rests on. Scout
  ramps use one seed; nothing is claimed from a scout.
- **Per engine and condition**, reported: Gamma_up, Gamma_down and width
  (mean and spread over seeds), A against Gamma on both branches,
  wavelength, temporal period, and planform numbers at the holds.
- **Nudge against baseline** (same model): wherever both run, the same
  ramp, seeds and analysis. Differences beyond seed spread are charged to
  the nudge. At holds, the referee's bulk rule as well. In the 2D pilot
  their thickness agreed within 0.075 at all 16 common steps.
- **Nudge against frictionless** (different models): a comparison of
  physics, expected to differ in onset and planform. Agreement is evidence
  that a feature does not depend on friction or on the nudge. Disagreement
  cannot be assigned to either.
- **For a "physical result" claim**, DIRECTION asks for two contact methods
  or insensitivity to the method. Nudge plus baseline meets that only where
  the baseline runs. Where it does not, results are reported as "nudge
  only".
- **Same treatment**: any change of window, threshold or sampling applies
  to every engine.

## 7. Cost

Measured rates (`E0050-results.json`), CPU per particle per cycle. They were
taken with six jobs of another program running, so they are upper estimates.

| | frictionless | nudge | baseline |
| --- | --- | --- | --- |
| 3D, Gamma 3, f\* 0.44 | 0.11 ms | 0.32 ms | 0.32 ms |
| 3D, Gamma 3, f\* 0.3 | 0.23 ms | 0.46 ms | 0.42 ms |
| 3D, Gamma 4, f\* 0.3 | 0.14 ms | 0.28 ms | 0.27 ms |
| 3D, Gamma 2.2, f\* 0.3 | 0.34 ms | 3.0 ms | does not run |
| 2D, depth 5 | 0.09 ms | 0.035 ms (Gamma 2.5 and up) | 0.033 ms |
| 2D, depth 10 | 0.17 ms | 0.23 ms (Gamma 2.5 and up) | 0.15 ms |
| 2D, depth 15 | 0.45 ms | not measured | not measured |

- In 3D at N = 60000 that is 6.5 seconds per cycle frictionless and 19
  with the nudge at Gamma 3, f\* 0.44; and 21 against 180 at Gamma 2.2,
  f\* 0.3.
- Cost goes as 1/f\* at fixed Gamma, falls as Gamma rises, and for the
  nudge rises steeply below Gamma 2.5.

Estimates (`phase-diagram-plan-costs.json`), in CPU-hours:

| Stage | What | CPU-hours |
| --- | --- | --- |
| A | 2D, depths 5 and 10: scout loops over Gamma 1.8 to 7 (one seed) and onset loops (three seeds, two rates), frictionless and nudge | 22 |
| B | 2D, depth 15, the same | 92 |
| C | 3D frictionless onset loops, f\* 0.27, 0.33, 0.44, three seeds | 48 |
| D | 3D frictionless onset loop at the slow rate, f\* 0.44, one seed | 16 |
| E | 3D frictionless scout above onset, six f\*, one seed | 25 |
| F | 3D frictionless holds at the seven Figure 1 conditions (2000 cycles, plus two seeds of 1000) | 49 |
| G | 3D nudge holds at the five Figure 1 conditions not yet run, three seeds of 1000 cycles | 96 |
| H | 3D nudge onset loops, f\* 0.27 and 0.44, three seeds | 62, uncertain by a factor of two or more |
| | Total | 410 |

- The baseline is not costed separately. Where it runs it costs what the
  nudge does, and its ramps end at the first step that stalls.
- The largest single run is about 13 CPU-hours (one nudge onset loop at
  f\* 0.27), inside the 40-hour per-run limit.
- **Against the budget**: 242 of 400 CPU-hours are spent since November 5.
  If the 400 is per calendar week, stages A, C, D, E and F (160) fit in one
  week and G and H need a second. If it is for the program so far, there
  are 158 left, just short of A, C, D, E and F together.

## 8. What to run first

1. **Build and test the field recorder and the 2D amplitude band**; register
   the thresholds. No simulation cost.
2. **Stage A** (22 CPU-hours, one night): the whole 2D picture at depths 5
   and 10 for all three engines, with the rate check and the two-start
   holds. This tests the hysteresis protocol end to end where it is cheap,
   and measures the nudge's floor against depth and f\*.
3. **Stage C at f\* 0.27 and 0.44, then 0.33** (48): the first 3D onset
   loops, frictionless. Prediction stated in advance: onset near Gamma 2.1
   to 2.2, stripes at both f\*, no loop.
4. **Stage F** (49): the frictionless Figure 1, for Chris to rate beside the
   reference.
5. **Stages D and E**, then **G**.
6. **Stage H last**, and only if stage A shows the nudge reaching the flat
   state with room to spare.
7. **Stage B** (depth 15 in 2D) is the poorest value: 92 CPU-hours for the
   filter. Proposed at one seed and one rate (about 20) unless depth 15
   shows something depths 5 and 10 do not.

## 9. Choices that are Chris's

- Whether the 400 CPU-hours is per week or for the program so far.
- Whether a 3D loop with friction that cannot reach the flat state is worth
  running as a down-branch only.
- The f\* list and the Gamma range.
- Whether stage B is wanted at all.
