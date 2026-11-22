# L0018: Wider or deeper box

## Status

Active. All 30 width-200 fast-pass loops running on Hatteras.

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

## Jobs in flight

| Experiment | Host | Jobs | f* | Description | Wall time |
|---|---|---|---|---|---|
| E0074 | hatteras | 164665-164674 | 0.27-0.84 | no friction, L 200, N 240000, 213 steps | 5 days |
| E0075 | hatteras | 164675-164684 | 0.27-0.84 | nudge, L 200, N 240000, 239 steps | 7 days |
| E0076 | hatteras | 164685-164694 | 0.27-0.84 | baseline (friction, main), L 200, N 240000, 239 steps | 7 days |

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
