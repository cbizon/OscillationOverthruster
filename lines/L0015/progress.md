# L0015: Fast pass, nudge

## What's done

- **E0065 (fast pass, ten frequencies):** Complete to the wall. Each loop
  starts at Gamma 3.0, goes down to a floor (Gamma 2.0 to 2.35), up to a
  wall at Gamma 4.35 to 4.50, clean audit. The wall is period-2 bouncing:
  the layer alternates between a high-bounce cycle (airborne, few collisions)
  and a low-bounce cycle (chattering on the plate, many collisions).

- **E0072 (continuations above the wall):** Each of the eight loops got
  one step past E0065's wall (Gamma 4.50 or 4.55) and hit the 2 CPU-hour
  per step guard. All processes dead; superseded by E0089.

- **E0085 (wall analysis):** The period-2 is documented at f* 0.44 and
  0.84. CPU per cycle doubles between 4.4 and 4.45 and again between 4.45
  and 4.5 at f* 0.44. The spatial pattern disappears by Gamma 4.4. (Its
  `cpu_and_events_at_wall` events column is a running total; noted in the
  file.)

- **E0088 (inelastic ball model):** Computed at all ten frequencies,
  Gamma 3.0 to 7.0. The model is frequency-independent. Period-2 onset at
  Gamma 3.7, both landings soft at 4.6 (impact 0.25 and 0.73 g/omega),
  period-1 returns at 4.65 (impact 1.59), impact back to 6.5 by 5.0.
  The stuck fraction peaks at 0.47 at 4.6 and drops to 0.27 by 5.0.
  Prediction: cost peaks near 4.6 and drops back by 5.0. (Uses CPU only;
  not affected by the running-total error.)

- **E0089 is over: all eight loops ended on the 48 CPU-hour step cap**
  (f* 0.44, job 164657, A0200, collected Nov 26 service run; 97.82 CPU-hours,
  the most of any job, under the 100 per-run limit). Outcome recorded:
  falsified (no loop above Gamma 4.6), 537.6 CPU-hours in all.

  | f* | job | artifact | stopped at | cycles | job CPU-h |
  |---|---|---|---|---|---|
  | 0.33 | 164655 | A0177 | 4.6 | 21/25 | 57.49 |
  | 0.38 | 164656 | A0180 | 4.55 | 14/25 | 57.92 |
  | 0.44 | 164657 | A0200 | 4.6 | 1/25 | 97.82 |
  | 0.50 | 164658 | A0194 | 4.6 | 1/25 | 82.38 |
  | 0.57 | 164659 | A0176 | 4.6 | 23/25 | 55.04 |
  | 0.65 | 164660 | A0184 | 4.6 | 10/25 | 65.29 |
  | 0.74 | 164661 | A0183 | 4.6 | 21/25 | 63.49 |
  | 0.84 | 164662 | A0181 | 4.6 | 24/25 | 58.11 |

- **Per-cycle costs (D0090, supersedes D0086; checker Nov 25-2):** take
  them from each cycle's audit.json count, never from step averages.
  `python3 tools/e0089_cycle_table.py <out> 0.33=<mirror>/hatteras-164655 ...
  --steps 3` -> `evidence/E0089-cycle-table.json`. Every stopping step
  alternates cheap and expensive cycles (T0049): expensive means 55,120
  (0.84) to 118,314 (0.65) events per particle, cheap 1,269 to 7,114, per
  pair 56,390 to 121,010 (f* 0.38 at 4.55: 88,588).
- **f* 0.44 and 0.50 at 4.6:** one cheap completed cycle (636, 456), then an
  unfinished cycle of at least 697,738 (0.81 cycle) and 725,554 (0.86).
  Three times any other loop's costliest cycle (230,431 at 0.65). Tiny
  sphere-pair collisions per cycle up 255 and 299 times from 4.55; tiny
  plate collisions not. Tiny ones are still only 0.02 to 0.03% of pair
  collisions: the events are ordinary pair collisions (pair collisions per
  cycle up 17.5 and 26 times, plate 9.8 and 12.9). The old "f* 0.50
  outlier, 389,000 per cycle" figure is withdrawn (describes no cycle).
- `evidence/E0089-step-table.json` has all eight loops (f* 0.44 merged Nov
  26); its per-cycle averages for stopped steps are superseded (note in
  `findings`). Counters are running totals: always difference steps.
- **Pinned phase diagram** (Chris pinned Nov 25):
  `lines/L0015/pinned/phase-diagram.svg`, from
  `python3 tools/l0015_phase_diagram.py lines/L0015/pinned/phase-diagram.svg`.
  Colour = pattern amplitude A (E0065); open circles = Hatteras steps with
  no amplitude computed; crosses = CPU-cap stops. No pattern type (the
  pass kept ring spectra only): asked Chris whether that suffices.
  Redraw it whenever new nudge data arrive.

- **Checker Nov 24 (two reviews) and Nov 25-2: answered** (Nov 25-2 in the
  Nov 26 run: cycle table, D0090, T0049/T0047, tiny collisions).

- **Record timestamps:** take `at` and `ended` from the clock when written.

## Things noticed, not yet followed up

- The earlier note that CPU per event grows 5.5 times toward the wall was
  an artifact of the running totals; withdrawn. On the Mac, CPU per event
  jumps 1.4 to 1.5 times at single steps (f* 0.33 at 4.5, f* 0.38 at 4.4,
  f* 0.84 at 4.5) and falls at others; probably machine load. Not examined.
- Gamma 3.5 cost across frequencies is 13 to 22 s/cycle.

## What's next

- Nothing runs. Waiting for Chris (questions in sessions/2026-11-26-L0015.json):
  (a) bigger per-step cap from 4.6 to 5.0, or (b) a cost probe from the
  saved 4.6 state at 4.65 to 5.0 (new experiment; not f* 0.44/0.50, where
  one cycle costs about 25 CPU-hours); "per run" meaning; pattern type on
  the diagram.
- Default if no answer: nothing more is spent on this line.
- If resuming a loop: change continue_loop.sh to keep the partial step
  instead of deleting it; partial checkpoints are in the artifacts on
  Hatteras.
- Physics or method: compare collisions near 4.5 to 4.6 with L0018's plain
  engine loops (another line's data), tiny pair collisions included.
- D0072 wake (Nov 26 08:00Z) is moot: no E0089 job is running.

## Jobs in flight

None. All E0089 jobs (164655 to 164662) ended and are collected. (164647
to 164654 were the first, broken submission; A0081 to A0088.)

## Key evidence files

- `evidence/E0089-cycle-table.json` (per cycle, eight loops, last three steps)
- `evidence/E0089-step-table.json` (per step, eight loops)
- `evidence/E0065-results.json` (all ten loops, amplitude per hold)
- `evidence/E0085-nudge-wall-fields.json` (wall analysis)
- `evidence/E0088-comparison.json` (inelastic ball vs nudge cost)

## Tools committed

- `tools/ramp.py`, `tools/field_recorder.py`, `tools/lc_counters.py`,
  `tools/inelastic_ball.py`, `tools/continue_loop.sh`
- `tools/e0089_step_table.py` (per step), `tools/e0089_cycle_table.py` (per cycle)
- `tools/l0015_phase_diagram.py` (pinned diagram)
