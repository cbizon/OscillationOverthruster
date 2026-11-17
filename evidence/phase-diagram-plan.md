# Phase diagram plan

Written in the session of 2026-11-13 for the instruction of that date,
revised in the session of 2026-11-14 (no new instruction that night) in
answer to the checker's review of Nov 13, and added to on 2026-11-15
(section 0a). A plan only: the sweep has not been
started. Numbers come from pilots and earlier runs; each is in the evidence
file named beside it. "Tonight" in sections 1 and 2 means Nov 13.

**Nov 16: the sweep has started, on a different footing (section 0b).
Where section 0b and the sections after it disagree, 0b holds.**

## 0b. What changed on Nov 16

The instruction of Nov 16 replaces the staged plan below with a fast pass
and Chris's own placing of slow loops. Prices are in
`phase-diagram-plan-costs-v3.json`; progress is in `E0060-results.json` and
the figures in `fastpass-figures/`.

- **No transition point.** The transition rule, the comparison against the
  no-friction loop and the two-start holds (section 5) are dropped from
  what is delivered. A sweep is shown as it is: amplitude against Gamma,
  the way up and the way down marked, steps not done shown. One figure per
  frequency and model. The rule's code stays in `loop_analysis.py` and is
  not applied.
- **The 2D stages (A, B) are dropped.** 3D only.
- **Fast pass.** The paper's layer (N 60000, L 100, depth 5.42), ten f\*
  (0.27, 0.30, 0.33, 0.38, 0.44, 0.50, 0.57, 0.65, 0.74, 0.84: Figure 1's
  range and values, the expected squares-to-stripes changeover, the rest
  spaced evenly in log f\*; D0039), Gamma 1.7 to 7.0 and back in steps of
  0.05, 25 cycles per step, one seed. That is 213 holds and 5,325 cycles a
  loop, at the experiments' ramp rate (0.002 in Gamma per cycle).
- **Models, in this order:** no friction, nudge, baseline.
  - No friction: all ten loops are running or queued (E0060). Priced at
    80 CPU-hours; repriced from the first 680 steps at about 154, because
    the cost per cycle above Gamma 2.7 is about 8.6 seconds at f\* 0.44 (I
    had assumed 4) and the other frequencies run 1.1 to 1.3 times the
    scaled f\* 0.44 cost (the first hour alone suggested 190). Ten jobs
    were running, so this is somewhat high. No loop is near the 40
    CPU-hour per-run limit (the dearest, f\* 0.27, is about 25); each loop
    stops itself at 38.
  - Nudge: it cannot hold the flat state cheaply (its cost climbs from 15
    seconds per cycle at Gamma 3.0 to 55 at 2.25 and it does not finish a
    step at 2.2 in half a CPU-hour, `E0059-results.json`), so its loop is
    the branch it can run: default start at Gamma 3.0, down to its floor,
    up to 7.0 and back down to just above the floor. Priced at 16 to 35
    CPU-hours for f\* 0.84 down to 0.38, and 40, 44 and 49 for 0.33, 0.30
    and 0.27, which are at or over the per-run limit and would be reported,
    not started. About 300 CPU-hours for the ten on that price, and more if
    the no-friction correction carries over. None is running: two were
    queued and withdrawn before starting (D0041).
  - Baseline (friction, no contact method): not priced as loops. In 3D it
    needs an upward push to start at Gamma 3 and stops below Gamma 2.3 to
    2.8 and at Gamma 5; its loops would be short branches. To be run where
    it can, after the nudge, with the start of `E0032`.
- **Budget.** The weekly limit is 400 CPU-hours and 167 were counted
  before tonight. The no-friction pass alone takes the week to about 80
  percent on the repriced figure. The nudge and baseline passes need
  further weeks at this limit, or a larger limit, or fewer frequencies.
- **Slow loops** are Chris's to place from the figures. Nothing slow is
  running. Candidates are listed in the session summary of Nov 16; the
  first is at f\* 0.44 without friction, Gamma 1.9 to 2.6 and back, where
  the pilot's two branches differ: 8 CPU-hours at 100 cycles per step
  (four times slower), 32 at 400 (sixteen times slower).
- **Deeper layers, next** (item 5 of the instruction: hysteresis should be
  more obvious in deeper layers). Not measured in 3D yet; the figures below
  scale tonight's prices by the number of spheres and by the 2D cost per
  sphere at each depth.
  - Twice the depth (10.84, N 120000): about 3.8 times the cost. Ten
    no-friction loops about 300 CPU-hours on the first price, more on the
    repriced one; f\* 0.30 and 0.27 would pass the per-run limit.
  - Three times the depth (16.26, N 180000): about 15 times the cost;
    every loop passes the per-run limit. Not proposed as full loops.
  - The wavelength grows with depth (lambda/H = 1.0 + 1.1 f\*^-1.32), so
    at L 100 and depth 10.84 the box holds 3.9 wavelengths at f\* 0.84,
    2.8 at 0.57, 2.2 at 0.44 and 1.3 at 0.27. Low frequencies, where
    squares and the larger hysteresis are expected, need a wider box,
    which multiplies the cost again (four times for L 200).
  - Proposed order: (1) one 20-cycle hold at depth 10.84, f\* 0.57, Gamma
    3, about 0.2 CPU-hours, to replace the 2D-derived factor with a
    measurement; (2) no-friction loops at depth 10.84 over the onset only
    (Gamma 1.7 to 3.0 and back, 53 steps instead of 213) at four
    frequencies, 0.84, 0.74, 0.65, 0.57, where the box still holds about
    three wavelengths; (3) the full Gamma range and the lower frequencies
    only where step 2 shows the branches apart. Step 2 is about a quarter
    of the full loops' cost.

## 0. What changed on Nov 14

The checker asked for four things before the first stage starts; each is
answered here, and the tools the plan listed as "needs building" are built.

- **(a) What the nudge's 3D diagram consists of.** On Nov 13 the nudge had
  no scan in Gamma in 3D, so "a phase diagram for each" was true only of
  the frictionless engine. The plan now has a stage I: a nudge scan above
  onset at the same six f\* as the frictionless one (74 CPU-hours, an upper
  estimate). The nudge's 3D diagram is then stage I, the holds of stage G
  and the onset loops of stage H. Section 3 says so. In 3D every engine has
  one depth, 5.42, the paper's.
- **(b) Stage A repriced, with the baseline.** Each engine is now priced
  from its own measured ramp at each of the four conditions, slow steps and
  capped step included, plus the two-start holds, which the Nov 13 price
  left out: 64 CPU-hours (frictionless 14, nudge 35, baseline 14), against
  22 on Nov 13. Section 7.
- **(c) The budget** is 400 CPU-hours in any seven days (`budgets.yaml`,
  as `program check` counts it), not for the program. Section 7.
- **(d) The transition point is redefined** so that it can be applied to an
  engine that stops soon after its pattern dies, and the up branch starts
  from the step where the engine turns. Section 5.
- **Built and tested** (`E0053-results.json`, `E0054-results.json`,
  `E0056-results.json`): the field recorder, the amplitude the loops are
  drawn in, the transition rule as code, the turn at an engine's floor, and
  the temporal-period rule tested on runs it was not chosen on (16 of 16).
- **Three things the Nov 14 pilots changed** (`E0055-results.json`,
  `E0056-results.json`; one seed each, so they shape the plan and are not
  results):
  - Measured by the new amplitude, the nudge reaches the flat state with
    room: its pattern is gone 0.13 to 0.43 in Gamma above its floor, with
    6 to 17 flat holds in a loop (five loops, four conditions). The Nov 13
    figure (a margin of 0.1 at depth 5, f\* 0.3, where it is now 0.43)
    came from an amplitude that included shot noise. The margin is
    smallest at depth 10, f\* 0.3 (0.13 and 0.18 at two seeds).
  - The baseline with friction is of little use at depth 10, f\* 0.3: it
    does not start from rest at Gamma 3.0 and, started from the nudge's
    state, stops at Gamma 2.8, while still patterned.
  - In 2D at depth 5, f\* 0.5 there is no pattern between Gamma 1.8 and
    3.0 with any engine; at depth 10, f\* 0.5 the onset is weak and gradual.
    The f\* 0.3 conditions are where a 2D onset loop can be read.

## 0a. What changed on Nov 15

No instruction again; the sweep is still not started. The checker's review
of Nov 14 asked for three things about the measuring choices (D0035). The
rule itself is not changed: it stays as fixed in section 4.

- **(a) Steadiness of the amplitude the plan uses**
  (`E0057-results.json`). On the 100-cycles-per-step frictionless loop the
  noise-corrected amplitude A differs between up and down branches by 7.2%
  of its range, against 7.0% for single snapshots and 3.6% for the plain
  band amplitude first registered. So "about twice as steady as a
  snapshot" in section 5 describes the plain amplitude, not A. A is better
  at telling flat from patterned (it does not rise in a layer with no
  pattern); it is no steadier than a snapshot.
- **What width of loop the rule can resolve.**
  - At 25 cycles per step: eight frictionless loops, where no hysteresis is
    expected, give widths of 0 or +0.05; the checker's baseline ramp gives
    -0.1; and a transition point moves by up to 0.1 with the analysis
    choices in (b). A single loop at this rate cannot show a width under
    about 0.15 in Gamma. Three seeds narrow that; by how much is not
    measured.
  - At 100 cycles per step: one loop exists (width 0). Its resolution is
    not measured and cannot be finer than the step, 0.05.
- **(b) A second band and a second tolerance floor**
  (`E0057-results.json`). The six frictionless f\* 0.3 loops were
  reanalysed with the band widened (modes 2 to L/8), narrowed (5 to L/12),
  and the floor at 0.05 D and 0.2 D, one change at a time. 45 of 48
  transition points move by one step (0.05) or less; 3 move by two steps,
  all on one loop (depth 5, seed 1, 25 cycles per step). No transition
  appears or disappears. I had predicted none would move by more than one
  step, so that prediction failed. At depth 5, f\* 0.5 no variant finds a
  transition, including the 0.05 floor.
- **(c) The baseline started from the nudge's state is not an independent
  check.** Where the unmodified engine with friction cannot start from
  rest and is handed the nudge's state (section 5, "Where an engine with
  friction turns"), its run is not used for any comparison between the two
  engines. It can show only where the unmodified engine stops.
- Still open from the same review: the 0.1 D floor is an absolute height
  set in 2D at depths 5 and 10. Whether it suits the 3D box is what the
  3D pilot of Nov 15 is for (below, when collected); depth 15 is unchecked.

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
- **Both engines with friction stop just below the pattern onset.**
  (Revised Nov 14, section 0: with the noise-corrected amplitude the nudge's
  pattern ends 0.13 to 0.43 above its floor.) At
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
- **What each engine gets in 3D** (revised Nov 14):
  - frictionless: onset loops at f\* 0.27, 0.33, 0.44 (stages C, D), the
    scout above onset at all six f\* (E), holds at all seven Figure 1
    conditions (F);
  - nudge: the same scout above onset at all six f\*, Gamma 2.7 to 7.0
    (stage I, new), holds at the seven Figure 1 conditions (two exist,
    five in stage G), and onset loops at f\* 0.27 and 0.44 down to its
    floor (H);
  - baseline: holds only where it runs (cases b and g so far). No ramps in
    3D: it fails at start-up and below about Gamma 2.3 to 2.8 in the
    pilots.
  - One depth, 5.42, for every engine. A second depth in 3D is not in this
    plan.

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
    modes that score high. In 2D the measure is the band amplitude A
    defined under "Amplitude" below.
- **Wavelength**: from the same ring. All eight of our Gamma 3 runs give
  19.4 to 19.8.
- **Temporal period** (half or quarter of the drive frequency): correlation
  of the field with itself one, two and four cycles later.
  - The rule I registered got 6 of 7 reference cases; the squares at a
    quarter frequency came out unclear.
  - A simpler rule (the smallest lag at which the correlation exceeds 0.5)
    gets 7 of 7, but I chose it after seeing the failure.
  - Tested Nov 14 on runs it was not chosen on (`E0054-results.json`):
    16 of 16. Ten of our case-b runs (expected period 2) and six case-g
    runs (expected 4), each continued nine cycles with the recorder. The
    winning correlations are 0.89 to 0.90 (case b) and 0.68 to 0.69
    (case g) against the threshold 0.5. It is two conditions with repeats,
    both patterned: no flat case and no period-1 case were in the test.
- **Amplitude A**, the quantity the hysteresis loops are drawn in (defined
  and tested Nov 14, `tools/loop_analysis.py`):
  - From the recorder: the variance of the height field carried by each
    Fourier mode of the box, at all 32 frames of every cycle, averaged over
    the hold.
  - Band: modes 3 to L/8 (wavelengths from a third of the box down to 8 D).
    Modes 1 and 2 are box-sized sloshing.
  - Noise-corrected: A squared is the band's total minus the band's width
    times its median mode. Shot noise in the bin means is spread evenly
    over modes and grows with the layer's thickness; a pattern is a peak.
    Without the correction the amplitude rises smoothly with Gamma in a
    layer with no pattern (depth 5, f\* 0.5) and the transition rule
    reported an onset there.
  - On the frictionless pilot loop (depth 5, f\* 0.3): flat level 0.09 D,
    patterned 0.9 to 1.0 D.
  - In 3D the same with rings of wavenumber instead of modes, from ring 2
    (at L 100 the patterns sit at rings 3 to 5; rings 1 and 2 hold under
    2% of the variance in patterned states). On the 16 recorded 3D holds
    (`E0054-results.json`) A is 0.41 to 0.42 D at case b, the same for
    the nudge and the baseline, and 0.44 to 0.46 at case g. No flat 3D
    state has been recorded and no 3D ramp run, so the 3D flat level and
    the choice of ring 2 are to be checked on the first 3D loop.
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

### Built on Nov 14 (no engine or referee change)

- **The field recorder**, `tools/field_recorder.py`: wraps the referee's
  run and saves the height field's spectrum at every frame and the field
  itself four times a cycle.
  - It changes nothing: all 147 steps of the three frictionless pilot
    loops, rerun with it, end in checkpoints identical to those without it
    (`E0053-results.json`). A run stopped mid-cycle and resumed gives the
    same record as an uninterrupted one.
  - Size of the field record: 4.8 kB per cycle in 2D at L 200, 9.3 at
    L 400, 27 in 3D (27 MB per 1000 cycles). Totals in section 7.
- **The thresholds, fixed here before the sweep** (all in
  `tools/loop_analysis.py` and `tools/period_rule.py`; a change after this
  is a new registration):
  - band: modes 3 to L/8; noise correction by the band median;
  - flat level: median of A over the five lowest-Gamma holds of the ramp;
    scatter: 1.4826 times their median absolute deviation;
  - patterned: A above the flat level by more than five times the scatter
    or 0.1 D, whichever is larger;
  - unsettled hold: halves differing by more than the same tolerance or
    10% of A;
  - temporal period: smallest of 1, 2, 4 cycles with correlation above
    0.5; contrast below 8 is flat;
  - planform thresholds as on Nov 13 (coherence 0.5, skewness 0.3),
    reported with their numbers and not trusted alone.
- The tools are now on a branch, `tools/phase-diagram`, with tests.

## 5. Hysteresis

### Protocol

- **Stepwise ramps**, `tools/ramp.py`: each step starts from the previous
  step's final state with only Gamma changed, at a whole-cycle boundary
  where the plate is at its mean height. Each step is a complete referee
  run with its own audit, recorded with the field recorder.
- **Step** 0.05 in Gamma at onset, 0.1 in the scout.
- **Rates**: 25 cycles per step of 0.05 is the experimental rate (0.002 per
  cycle). Also 100 cycles per step; 400 where a loop is seen.
- **Direction**:
  - frictionless: up from flat (Gamma 1.8), then down;
  - with friction: down from a patterned state (Gamma 3.0), turn, then up.
    The engines cannot start below onset.
- **Where an engine with friction turns** (added Nov 14,
  `ramp.py --turn-on-stop --turn-above-fraction 0.5`):
  - Each step has a CPU cap: 0.1 hours per 25 cycles for the nudge, 0.05
    for the baseline, four times that at 100 cycles per step.
  - The ramp turns at the first down step that uses more than half its cap,
    or at the last completed step if one stops outright. That Gamma is the
    engine's **floor** for the loop. The up branch starts from that step's
    final state.
  - Why half the cap: in the pilot the nudge at depth 10, f\* 0.5 completed
    Gamma 2.2 going down (245 of 360 seconds) and then did not complete it
    going up from 2.15. Turned at 2.2 it completed the loop
    (`E0055-results.json`).
  - If the baseline cannot start from rest at Gamma 3.0, it starts from the
    nudge's state there (same model, same seed). Said in the results where
    used.

### Defining a transition point

Revised Nov 14; the rule is code, `tools/loop_analysis.py`.

- The order parameter is the hold's amplitude A (section 4).
- **Flat level F and scatter s**: the median of A over the five
  lowest-Gamma holds of the ramp, both branches, and 1.4826 times their
  median absolute deviation. Median, so that one hold that is still
  patterned among the five does not set the level.
- **Patterned hold**: A above F by more than max(5 s, 0.1 D).
- **Gamma_up**: on the up branch, the midpoint between the lowest step that
  is patterned together with the two steps above it, and the flat step
  below it. **Gamma_down**: the same on the down branch.
- **Hysteresis width** = Gamma_up minus Gamma_down.
- Also reported: the zero crossing of a straight line through A squared
  minus F squared against Gamma, over the patterned steps within 0.4 of
  the transition. A continuous onset gives a straight line reaching zero
  at the threshold; a jump is a discontinuous one. Where the onset is weak
  and gradual (2D, depth 10, f\* 0.5) the step rule moves by 0.1 to 0.15
  with the choice of flat holds and the fit is the steadier number.
- **An engine that turns with few flat holds** (the checker's point):
  - Three or more holds that are not patterned: F and s come from the
    engine's own lowest five holds, as above. In the pilots the nudge had
    6 to 17 flat holds per loop where there is a pattern, and the baseline
    10 at depth 10, f\* 0.5.
  - Fewer than three: F and s are borrowed from the frictionless ramp's
    flat holds at the same condition, and said to be borrowed.
  - A branch whose lowest step is still patterned has **no transition
    point**: the transition is reported as "below the floor", with the
    floor's Gamma, and the fit's zero crossing is given as an
    extrapolation only. No width is reported for that loop. (Pilot: the
    baseline at depth 10, f\* 0.3.)
  - The up branch starts at the floor, so Gamma_up is defined whenever the
    floor is flat.
- **Tested on a seed it was not set on** (`E0056-results.json`): the rule
  and amplitude were fixed on seed-1 pilots and then run unchanged on seed
  11. Four of five predictions held: the three frictionless ones
  (transition within 0.1 of seed 1 at depth 5 and depth 10, f\* 0.3; none
  at depth 5, f\* 0.5) and the nudge at depth 10, f\* 0.3 (2.43 at both
  seeds, from its own flat holds). The fifth failed: for the nudge at
  depth 5, f\* 0.3 I predicted 2.15 to 2.40 from the Nov 13 snapshot
  amplitude and the rule gives 2.53. The uncorrected amplitude of the same
  run does fall until about 2.3, as on Nov 13; between 2.3 and 2.5 it is
  the layer thinning, with no peak in the spectrum. So the prediction was
  wrong because of the measure it was drawn from, and with friction the
  2D pattern ends near 2.5, not 2.25 (one seed).
- What the rule gave on the pilots, to show it can be applied (one seed
  each, 25 cycles per step unless said; not results):

  | 2D condition | engine | floor | flat holds | Gamma_down | Gamma_up |
  | --- | --- | --- | --- | --- | --- |
  | depth 5, f\* 0.3 | frictionless, seed 1 (three loops) | none | 10 to 12 | 2.03 to 2.08 | 2.08 |
  | depth 5, f\* 0.3 | frictionless, seed 11 | none | 12 | 2.08 | 2.08 |
  | depth 5, f\* 0.3 | nudge, seed 11 | 2.10 | 17 | 2.53 | 2.53 |
  | depth 5, f\* 0.5 | all three | 2.05 to 2.2 with friction | all | none | none |
  | depth 10, f\* 0.3 | frictionless, seed 1 | none | 16 | 2.18 | 2.23 |
  | depth 10, f\* 0.3 | frictionless, seed 11 | none | 17 | 2.18 | 2.23 |
  | depth 10, f\* 0.3 | nudge, seed 1 | 2.25 | 9 | 2.43 | 2.53 |
  | depth 10, f\* 0.3 | nudge, seed 11 | 2.30 | 6 | 2.43 | 2.48 |
  | depth 10, f\* 0.3 | baseline, seed 1 | 2.85 | 0 | below the floor | none |
  | depth 10, f\* 0.5 | frictionless, seed 1 | none | 36 | 2.73 | 2.78 |
  | depth 10, f\* 0.5 | frictionless, seed 11 | none | 37 | 2.68 | 2.73 |
  | depth 10, f\* 0.5 | nudge, seed 1 | 2.20 | 15 | 2.53 | 2.63 |
  | depth 10, f\* 0.5 | baseline, seed 1 | 2.35 | 10 | 2.63 | 2.58 |

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

What the pilots showed about this (2D, f\* 0.3, depth 5, frictionless, one
seed): up and down branches agree in layer thickness to 0.09 on average at
25 cycles per step and 0.055 at 100, with thickness running from 1.5 to 5
over the ramp. No loop at either rate, as expected without friction.

With the recorder (Nov 14, same loops): the hold-mean amplitude's up-down
difference is 3.6% of its range at 100 cycles per step, against 7.0% for
the snapshot amplitude. About twice as smooth, a little short of the factor
of two I registered (`E0053-results.json`); at 25 cycles per step the gain
is smaller (6.6% against 9.7%), because the pattern's own amplitude wanders
over tens of cycles. So a 25-cycle hold places a transition to one step
(0.05), not better, and three seeds are needed for anything finer.

At depth 10, f\* 0.3 the frictionless up branch lags the down branch at 25
cycles per step (A of 0.95 against 1.64 at Gamma 2.3). That is the
too-fast ramp these checks exist for, and a reason to expect the deep
layers to need the 100-cycle rate.

### The risk

Revised Nov 14. With friction, the loop has to go below the pattern's
lower threshold while the engine still runs.

- By the noise-corrected amplitude the nudge manages it in 2D at all four
  conditions piloted: the pattern is gone 0.13 to 0.43 in Gamma above its
  floor (least at depth 10, f\* 0.3). Its cost per cycle rises 8 to 110
  times between Gamma 3 and the floor, which the caps bound.
- The baseline does not at depth 10, f\* 0.3, and has little room
  elsewhere (floors 2.2 to 2.35). Loops with friction therefore rest on the
  nudge, with the baseline as a check on the down branch where it runs.
- In 3D at Gamma 2.2 the nudge ran 24 cycles at 45 seconds per cycle in a
  quarter-size box. Whether its 3D floor leaves the same room is not
  known; stage H is still last and still uncertain.

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

Estimates, in CPU-hours. Stage A and stage I are from the Nov 14 repricing
(`phase-diagram-plan-costs-v2.json`); the rest are the Nov 13 prices
(`phase-diagram-plan-costs.json`), unchanged.

| Stage | What | CPU-hours |
| --- | --- | --- |
| A | 2D, depths 5 and 10, three engines: onset loops (three seeds, two rates), two-start holds (three seeds), scout above Gamma 3 (one seed) | 64 |
| B | 2D, depth 15, the same (Nov 13 price; nudge rate assumed, baseline not priced) | 92 |
| C | 3D frictionless onset loops, f\* 0.27, 0.33, 0.44, three seeds | 48 |
| D | 3D frictionless onset loop at the slow rate, f\* 0.44, one seed | 16 |
| E | 3D frictionless scout above onset, six f\*, one seed | 25 |
| F | 3D frictionless holds at the seven Figure 1 conditions (2000 cycles, plus two seeds of 1000) | 49 |
| G | 3D nudge holds at the five Figure 1 conditions not yet run, three seeds of 1000 cycles | 96 |
| H | 3D nudge onset loops, f\* 0.27 and 0.44, three seeds | 62, uncertain by a factor of two or more |
| I | 3D nudge scout above onset, Gamma 2.7 to 7.0, six f\*, one seed (new) | 74, an upper estimate |
| | Total | 525 |

Stage A by condition and engine (each from that engine's measured ramp at
that condition: `E0052`, `E0053`, `E0055`, `E0056`):

| 2D condition | frictionless | nudge | baseline |
| --- | --- | --- | --- |
| depth 5, f\* 0.3 | 0.4 | 2.8 | 0.8 |
| depth 5, f\* 0.5 | 0.2 | 2.3 | 0.3 |
| depth 10, f\* 0.3 | 9.5 | 19.9 | 7.2 |
| depth 10, f\* 0.5 | 4.4 | 10.3 | 6.0 |
| all four | 14.4 | 35.3 | 14.3 |

- How stage A is priced: a loop at 25 cycles per step costs what the
  measured loop cost, slow steps and capped step included; a loop at 100
  cycles per step four times that; three seeds of each. Two-start holds
  are two 1000-cycle runs per seed at the Gamma just above the engine's
  own down transition. The scout runs 3.0 to 7.0 and back at the engine's
  rate at Gamma 3 (an upper estimate, cost falls with Gamma).
- **Caps**: per step, 0.1 CPU-hours per 25 cycles for the nudge and the
  frictionless engine, 0.05 for the baseline; four times that at 100
  cycles per step. A loop cannot cost more than its steps times its cap.
- The Nov 13 price for stage A was 22. The difference: the baseline (14)
  was not priced, the nudge's slow steps near its floor were not priced
  (a 25-cycle loop costs 0.15 to 0.17 hours at depth 5, 13 to 15 times
  the Nov 13 figure, and 0.5 to 0.8 at depth 10, 1.5 to 2.6 times), and
  the two-start holds were left out.
- The nudge at depth 10 is 30 of the 64.
- One seed stands behind each price, and the timings were taken beside 3
  to about 10 jobs of another program.
- **Stage I** uses the nudge's rate at Gamma 3, f\* 0.44 (0.32 ms per
  sphere per cycle) scaled by 0.44 / f\*, as stage E does for the
  frictionless engine. Cost falls with Gamma (0.6 of this at Gamma 4), so
  it is an upper estimate. Tonight's nine-cycle continuations at case b
  ran at 0.24 ms per sphere per cycle with either engine, on a quieter
  machine.
- The largest single run is still about 13 CPU-hours (one nudge onset loop
  at f\* 0.27 in 3D), inside the 40-hour per-run limit.
- **Against the budget** (corrected Nov 14): the limit is 400 CPU-hours in
  any seven days. `program check` counted 208 of 400 at the start of the
  Nov 14 session, before that session's own few hours. The plan in full is
  about 525, so it takes at least two weeks of budget whatever the order;
  stage A fits in the current week with room to spare.
- **Disk**: the field record and per-step checkpoints of stage A come to
  about 3 GB (a three-seed, two-rate set of loops is 0.17 GB at depth 5 and
  0.35 GB at depth 10, per engine and f\*). 3D adds 27 MB per 1000 cycles.
  The program's data is 3.5 of 15 GB now.

## 8. What to run first

1. ~~Build and test the field recorder and the 2D amplitude band; register
   the thresholds.~~ Done Nov 14 (section 4).
2. **Stage A** (64 CPU-hours, two nights at ten cores or fewer): the 2D
   picture at depths 5 and 10 for all three engines, with the rate check
   and the two-start holds. This tests the hysteresis protocol end to end
   where it is cheap. The f\* 0.3 conditions carry the onset loops; at
   f\* 0.5 the pilots found no pattern (depth 5) or a weak one (depth 10)
   below Gamma 3, so there the scout above 3 matters more than the onset
   window.
3. **Stage C at f\* 0.27 and 0.44, then 0.33** (48): the first 3D onset
   loops, frictionless. Prediction stated in advance: onset near Gamma 2.1
   to 2.2, stripes at both f\*, no loop.
4. **Stage F** (49): the frictionless Figure 1, for Chris to rate beside the
   reference.
5. **Stages D and E**, then **I and G**: the nudge's scan above onset
   beside the frictionless one, then its holds.
6. **Stage H last.** Stage A no longer decides it alone (the nudge has room
   in 2D); what is unknown is its cost at Gamma 2.2 to 2.5 in the full 3D
   box. A single nudge down-ramp at f\* 0.44 with the caps on would
   measure that for a few CPU-hours before the three-seed loops are
   committed.
7. **Stage B** (depth 15 in 2D) is the poorest value: 92 CPU-hours for the
   filter. Proposed at one seed and one rate (about 20) unless depth 15
   shows something depths 5 and 10 do not.

## 9. Choices that are Chris's

- Whether to start stage A.
- Whether the nudge's 3D diagram as now listed (section 3: scan above onset
  at six f\*, seven holds, two onset loops) is what "a phase diagram for
  each" should mean, or whether three f\* would do for the scan (about
  half the 74 CPU-hours).
- Whether a 3D loop with friction that cannot reach the flat state is worth
  running as a down-branch only.
- The f\* list and the Gamma range.
- Whether stage B is wanted at all.
- Settled since Nov 13: the 400 CPU-hours are per seven days
  (`budgets.yaml`).
