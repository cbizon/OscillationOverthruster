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
  and 4.5 at f* 0.44. The spatial pattern disappears by Gamma 4.4.

- **E0088 (inelastic ball model):** Computed at all ten frequencies,
  Gamma 3.0 to 7.0. The model is frequency-independent. Period-2 onset at
  Gamma 3.7, both landings soft at 4.6 (impact 0.25 and 0.73 g/omega),
  period-1 returns at 4.65 (impact 1.59), impact back to 6.5 by 5.0.
  The stuck fraction peaks at 0.47 at 4.6 and drops to 0.27 by 5.0.
  Prediction: cost peaks near 4.6 and drops back by 5.0.

- **E0089, f* 0.57 (job 164659, artifact A0176), ended Nov 24:** completed
  Gamma 4.55 (980 CPU-s/cycle, Hatteras), then stopped at Gamma 4.6 on the
  48 CPU-hour step cap after 23 of 25 cycles (7,514 CPU-s/cycle; 55.04
  CPU-hours for the job). Exit 1 is by design (ramp.py ends the loop on the
  first up-branch step that does not finish), not a crash; audit clean.
  Plate collisions per particle per cycle 1,319 (4.5), 2,297 (4.55), 7,720
  (4.6). Evidence `evidence/E0089-interim-f0.57.json` (table with
  ball-model columns). The step-084 checkpoint (23 cycles at 4.6) is in
  A0176 on Hatteras; continue_loop.sh as written would delete that
  unfinished step and redo 4.6 from the 4.55 checkpoint.

- **E0089, f* 0.33 (job 164655, artifact A0177), ended Nov 24 15:01Z:**
  same as f* 0.57. Completed 4.55 (1,332 CPU-s/cycle, Hatteras), stopped
  at 4.6 on the cap after 21 of 25 cycles (8,229 CPU-s/cycle); 57.49
  CPU-hours for the job; audit clean. Plate collisions per particle-cycle
  1,336 / 2,405 / 7,398 at 4.5 / 4.55 / 4.6; events 13,967 / 20,168 /
  61,579. Evidence `evidence/E0089-interim-f0.33.json` (same columns and
  formulas as f* 0.57; the script reproduced the f* 0.57 table exactly).
- **E0089's loop-completion clause** ("falsified if the loops cannot
  complete above 5.0") has failed at f* 0.33 and 0.57 under the registered
  48-hour cap. Say so in the E0089 outcome. A raised cap or a probe is a
  NEW experiment.
- **Checker Nov 24, answered this run:** (1) "five times" at 4.55 vs 4.5
  was Mac vs Hatteras; in events it is 1.34x (f* 0.57), 1.44x (f* 0.33).
  (2) loop-completion clause stated as failed (above). (3) per-run budget:
  `evidence/E0089-budget-check.json` + D0072 guard (below).

## Things noticed, not yet followed up

- CPU per event rises much faster than any event counter: on the Mac,
  0.044 microseconds per event at 4.3 to 0.242 at 4.5 (5.5 times) while
  pair checks per event stay at 50 (50 at 4.3 to 56 at 4.6) and root
  calls per event go from 1.28 to 1.59. Same-machine 4.55 to 4.6 on
  Hatteras: 2.5 times. Something uncounted (queue work, nudge iterations,
  or machine load) is growing. Not examined.
- Gamma 3.5 cost across frequencies is 13 to 22 s/cycle (Nov 21 summary
  said 15 to 22; corrected in the Nov 24 note).

## What's next

- **D0072 budget guard, wake set for Nov 26 08:00Z (03:00 EST).** At that
  run: `program jobs`; for every E0089 job still running, look at which
  step is in progress in its mirror (the step folder whose summary.json is
  a stub with only `ramp`). If it is past the step listed in
  `evidence/E0089-budget-check.json` (f* 0.38: 4.55; others: 4.6),
  `program cancel <job> --reason "D0072: would pass 100 CPU-hours per run"`
  before 09:27Z. f* 0.44 (164657) in 4.6 hits its cap about 07:05 to
  07:30Z at about 97.6 CPU-hours: leave it, unless still running at 09:00Z.
  If Chris has answered the "per run" question first, follow the answer.

- **Collect the other seven E0089 loops** as they end (each ending starts
  this line). Add each to an E0089 interim table like the f* 0.57 one.
- **D0071:** don't resubmit f* 0.57 alone. Once all eight have ended,
  if they all stop at 4.6, ask Chris: (a) a bigger per-step cap at 4.6 to
  5.0 (4.6 alone needs about 52 CPU-hours per loop on Hatteras; per-run
  limit in budgets.yaml is 100), or (b) a cheaper cost probe at 4.65 to
  5.0 started from the 4.6 state (a new experiment, not a loop). If
  resuming, change continue_loop.sh to keep the partial 4.6 step instead
  of deleting it (check the referee resume counts CPU from zero).
- Then: overlay measured cost on the ball model; write the E0089 outcome
  (falsified_if: cost at 5.0 not within a factor 2 of the 4.3 level, or
  loops cannot complete above 5.0).

## Jobs in flight

| Experiment | Host | Job ID | f* | State on Nov 24 15:08Z |
|---|---|---|---|---|
| E0089 | hatteras | 164655 | 0.33 | ENDED (cap at 4.6), collected |
| E0089 | hatteras | 164656 | 0.38 | running, step 4.55 (since Nov 22 15:11Z; cap due about now) |
| E0089 | hatteras | 164657 | 0.44 | running, step 4.6 |
| E0089 | hatteras | 164658 | 0.50 | running, step 4.6 |
| E0089 | hatteras | 164659 | 0.57 | ENDED (cap at 4.6), collected |
| E0089 | hatteras | 164660 | 0.65 | running, step 4.6 |
| E0089 | hatteras | 164661 | 0.74 | running, step 4.6 |
| E0089 | hatteras | 164662 | 0.84 | running, step 4.6 |

(164647 to 164654 were the first, broken submission: failed in 20 s on a
wrong wrapper path; artifacts A0081 to A0088.)

## Key evidence files

- `evidence/E0089-interim-f0.57.json` (f* 0.57 above the wall)
- `evidence/E0089-interim-f0.33.json` (f* 0.33 above the wall)
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
