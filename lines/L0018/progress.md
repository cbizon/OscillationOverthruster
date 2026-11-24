# L0018: Wider or deeper box

## Status

Active. 23 of the 30 width-200 fast-pass loops still running on Hatteras
(as of Nov 24, 11:50 UTC). Seven have ended (see below); none needs
relaunching under the loops' own stopping rules.

## What is done

- Cost holds (E0070, Nov 18): twice as wide costs 4.7 to 5.6 times the
  paper's box per cycle; twice as deep costs 12 to 18 times, not the 3.8
  scaled from 2D.
- Onset loop at L 200 (E0071, completed Nov 20): f* 0.44, Gamma 1.7 to
  3.0 and back, 25 cycles per step, no friction. 53 steps, all completed,
  no slow stretch, no audit failure. 22.9 CPU-hours, 311 MB.
- Tradeoff written (evidence/wider-vs-deeper.md).
- Field storage reduction (D0054, Nov 20): width-200 passes store no
  height-field arrays in fields.npz (only spectra and variances). Per loop:
  about 390 MB with checkpoints at Gamma multiples of 1.0.
- Checkpoint interval tightened (D0057, Nov 21): checkpoints at Gamma
  multiples of 0.5, step 0, and the latest completed step. This matches the
  instruction's storage rule.

- Ended loops examined (Nov 23 run, evidence/E0076-interim.json):
  - E0076 baseline f* 0.84 (164685, A0095), 0.33 (164692, A0089),
    0.30 (164693, A0096), 0.27 (164694, A0097): sphere overlap in the
    first step at Gamma 3.0, 0 or 1 of 50 cycles. Width 100 lost only 0.27.
  - E0076 baseline f* 0.65 (164687, A0171): floor 2.4 (overlap at 2.35),
    ceiling 3.9 (overlap at 3.95); width 100: 2.25 and 4.1. 46.1 CPU-hours,
    median 0.91 CPU-hours per 25-cycle step (five to six times width 100,
    not like-for-like; see the checker's review of Nov 23).
  - E0075 nudge f* 0.27 (164684, A0094): first-step cap (4 CPU-hours)
    after 49 of 50 cycles. Raising its cap is Chris's call. The Nov 21
    question on the caps went unanswered, so its default applies (let the
    loops run and stop); Chris did NOT reply about caps on Nov 22.

- E0076 baseline f* 0.57 (164688, A0175; Nov 24 run): floor 2.35 (CPU cap,
  2 CPU-hours, at 2.3 after 23 of 25 cycles), highest Gamma 3.8 (stalled at
  3.85, cycle 11). Width 100: 2.2 and 4.0. 53.0 CPU-hours, median 1.02
  CPU-hours per 25-cycle step. Added to evidence/E0076-interim.json.

## Jobs in flight

| Experiment | Host | Jobs | f* | Description | Wall time |
|---|---|---|---|---|---|
| E0074 | hatteras | 164665-164674 (all running) | 0.27-0.84 | no friction, L 200, N 240000, 213 steps | 5 days |
| E0075 | hatteras | 164675-164683 running; 164684 ended | 0.27-0.84 | nudge, L 200, N 240000, 239 steps | 7 days |
| E0076 | hatteras | 164686, 164689-164691 running (f* 0.74, 0.50, 0.44, 0.38); others ended | 0.27-0.84 | baseline (friction, main), L 200, N 240000, 239 steps | 7 days |

E0074: Gamma 1.7 to 7.0 and back, 25 cycles per step, 4 CPU-hour cap.
E0075: Gamma 3.0 down to 1.7, up to 7.0, back, 50/25 cycles first/rest,
  2/8 CPU-hour cap down/up, turn on stop. Engine: method/nudge.
E0076: same loop as E0075, half-push start (caseb_start.py). Engine: main.

Storage rule: no height grids (SEQUEL_FIELD_FRAMES=none, default in
field_recorder.py); checkpoints at Gamma multiples of 0.5
(--keep-checkpoints-every 0.5); spectrum and variance at every frame.

Size per loop:
- E0074: about 640 MB on Hatteras (23 checkpoints), about 36 MB fetched.
- E0075/E0076: about 690 MB on Hatteras (25 checkpoints), about 41 MB fetched.
- Hatteras checkpoints excluded from fetch (fetch_exclude in program.toml).

## What is next

- As each E0076 loop ends, append it to evidence/E0076-interim.json (same
  per-step summary.json fields: step, gamma, outcome, cycles, cpu_h,
  energy_gains, audit_failures, slow, sha256 of summary.json). When the
  last four end, write E0076's outcome: one table of floor and highest
  Gamma per f* against width 100 (evidence/E0073-results.json). Say which
  floors are cost stops (CPU cap) and which are overlaps or stalls.
- Collect the first completed jobs and check per-step cost against E0070.
- Compare the E0071 onset at L 200 with E0060 at L 100 for f* 0.44.
- The nudge loops (E0075) will likely stop at the period-2 wall above
  Gamma 4.4. If E0089 (the L 100 continuations) shows the cost drops above
  4.65, raise the E0075 caps and continue.

## Key evidence

- evidence/E0070-results.json (cost holds)
- evidence/wider-vs-deeper.md (tradeoff)
- evidence/D0054-width200-fields.json (field storage reduction)
- sequel-data/runs/E0071/ (onset loop data, 311 MB)
