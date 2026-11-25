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

- **E0089, six of eight loops ended (Nov 24; f* 0.65 and 0.74 collected
  Nov 25 05:40Z run), all on the 48 CPU-hour step cap.** Exit 1 is by design (ramp.py ends the loop on the first up-branch
  step that does not finish); energy audit clean throughout. Per-step table
  for all six: `evidence/E0089-step-table.json`, built by
  `python3 tools/e0089_step_table.py <mirror job dir> <f*> <out.json>
  --ball evidence/E0089-interim-f0.57.json`, then merged (see the file's
  `loops` list).

  | f* | job | artifact | stopped at | cycles | CPU-s/cycle there | job CPU-h |
  |---|---|---|---|---|---|---|
  | 0.33 | 164655 | A0177 | 4.6 | 21/25 | 8,229 | 57.49 |
  | 0.38 | 164656 | A0180 | 4.55 | 14/25 | 12,344 | 57.92 |
  | 0.57 | 164659 | A0176 | 4.6 | 23/25 | 7,514 | 55.04 |
  | 0.65 | 164660 | A0184 | 4.6 | 10/25 | 17,280 | 65.29 |
| 0.74 | 164661 | A0183 | 4.6 | 21/25 | 8,229 | 63.49 |
| 0.84 | 164662 | A0181 | 4.6 | 24/25 | 7,201 | 58.11 |

  Corrected (step-difference) events per particle per cycle at 4.5 / 4.55
  / 4.6: f* 0.33 1,778 / 6,201 / 37,569; f* 0.57 1,351 / 4,378 / 33,296;
  f* 0.84 1,520 / 6,121 / 30,238. f* 0.38: 1,644 (4.45) / 5,575 (4.5) /
  49,631 (4.55). f* 0.65 2,048 / 7,960 / 71,158; f* 0.74 2,042 / 7,228 /
  33,318. CPU per event on Hatteras 3.6 to 4.2 microseconds, flat within 3%
  between the last two steps (Hatteras only; on the Mac it moves 0.54 to
  1.48 times step to step). The "Mac to Hatteras 1.6 to 2.0 times" ratio
  mixes machine and Gamma step: NOT a machine speed (checker Nov 24-3).
  Plate collisions per cycle at the stopping step: 6.4 to 16.3 times 4.5.
  Untested: whether the extra collisions are physics or nudge-made (compare
  with L0018 plain-engine loops at the same Gamma).

- **Counters are running totals.** Checkpoints carry the counters, and
  ramp.py starts each step from the previous step's checkpoint, so
  counters.json and the referee's events_per_particle_cycle add up the
  whole loop. Always difference consecutive steps. The interim f* 0.33 and
  0.57 files carry a `superseded` note. Question put to Chris (referee is
  Chris's).

- **E0089's loop-completion clause** ("falsified if the loops cannot
  complete above 5.0") has failed at f* 0.33, 0.38, 0.57, 0.65, 0.74, 0.84 under
  the registered 48-hour cap. Say so in the E0089 outcome. A raised cap or
  a probe is a NEW experiment. The partial last-step checkpoints are in the
  artifacts on Hatteras; continue_loop.sh as written would delete that
  unfinished step and redo it.

- **Checker Nov 24 (two reviews), answered:** cross-machine ratio, failed
  clause, per-run budget (D0072), running totals (Nov 24 run 3), B0008 is
  resolved (no longer listed open), D0072 wake re-set in run 3 (service
  replied "L0015 will be started at 03:00 EST on Nov 26"). There may be two
  timers for that time if the first was set too; harmless.

- **Record timestamps:** take `at` and `ended` from the clock when written
  (checker flagged future-dated stamps twice).

## Things noticed, not yet followed up

- The earlier note that CPU per event grows 5.5 times toward the wall was
  an artifact of the running totals; withdrawn. On the Mac, CPU per event
  jumps 1.4 to 1.5 times at single steps (f* 0.33 at 4.5, f* 0.38 at 4.4,
  f* 0.84 at 4.5) and falls at others; probably machine load. Not examined.
- Gamma 3.5 cost across frequencies is 13 to 22 s/cycle.

## What's next

- **D0072 budget guard, wake set for Nov 26 08:00Z (03:00 EST).** At that
  run: `program jobs`; for every E0089 job still running, look at which
  step is in progress in its mirror (the step folder whose summary.json is
  a stub with only `ramp`). If it is past 4.6, `program cancel <job>
  --reason "D0072: would pass 100 CPU-hours per run"` before 09:27Z.
  f* 0.44 (164657) in 4.6 hits its cap about 07:05 to 07:30Z at about 97.6
  CPU-hours: leave it, unless still running at 09:00Z. If Chris has
  answered the "per run" question first, follow the answer.
- **Collect the other two E0089 loops** (f* 0.44, 0.50, both still in
  4.6 at Nov 25 05:45Z) as they end (each ending starts this line); add
  each to `evidence/E0089-step-table.json` with tools/e0089_step_table.py.
- **D0071:** don't resubmit any loop alone. Once all eight have ended,
  ask Chris: (a) a bigger per-step cap at 4.6 to 5.0, or (b) a cheaper
  cost probe at 4.65 to 5.0 started from the 4.6 state (a new experiment).
  If resuming, change continue_loop.sh to keep the partial step instead of
  deleting it (check the referee resume counts CPU from zero).
- Then: overlay measured cost on the ball model; write the E0089 outcome
  (falsified_if: cost at 5.0 not within a factor 2 of the 4.3 level, or
  loops cannot complete above 5.0).

## Jobs in flight

| Experiment | Host | Job ID | f* | State on Nov 25 05:45Z |
|---|---|---|---|---|
| E0089 | hatteras | 164655 | 0.33 | ENDED (cap at 4.6), collected |
| E0089 | hatteras | 164656 | 0.38 | ENDED (cap at 4.55), collected run 3 |
| E0089 | hatteras | 164657 | 0.44 | running, step 4.6 |
| E0089 | hatteras | 164658 | 0.50 | running, step 4.6 |
| E0089 | hatteras | 164659 | 0.57 | ENDED (cap at 4.6), collected |
| E0089 | hatteras | 164660 | 0.65 | ENDED (cap at 4.6), collected Nov 25 |
| E0089 | hatteras | 164661 | 0.74 | ENDED (cap at 4.6), collected Nov 25 |
| E0089 | hatteras | 164662 | 0.84 | ENDED (cap at 4.6), collected run 3 |

(164647 to 164654 were the first, broken submission: failed in 20 s on a
wrong wrapper path; artifacts A0081 to A0088.)

## Key evidence files

- `evidence/E0089-step-table.json` (six ended loops, step differences)
- `evidence/E0089-interim-f0.57.json`, `-f0.33.json` (counter columns superseded)
- `evidence/E0089-budget-check.json` (worst case per running loop, D0072)
- `evidence/E0065-results.json` (all ten loops)
- `evidence/E0085-nudge-wall-fields.json` (wall analysis)
- `evidence/E0088-comparison.json` (inelastic ball vs nudge cost)
- `evidence/E0088-ball-f0.44.json` (ball model, f* 0.44)
- `evidence/E0059-results.json` (pilot)

## Tools committed

- `tools/ramp.py` — stepwise ramp driver (paths relative to repo)
- `tools/field_recorder.py` — height-field spectrum recorder (no grids by default)
- `tools/lc_counters.py` — counter recorder
- `tools/inelastic_ball.py` — completely inelastic ball model
- `tools/continue_loop.sh` — Hatteras loop continuation helper
- `tools/e0089_step_table.py` — per-step table from counter differences
