# L0018: Wider or deeper box

## Status

Active. The wider box (L 200) is the cheaper step and the one that opens
low frequencies. Deeper layers wait.

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
  about 390 MB, down from about 880 MB. Applied to the queue spec for
  E0074, E0075, E0076.

## What is next

- E0074, E0075, E0076: width-200 fast passes (no friction, nudge,
  baseline) at all ten frequencies. Queued in q-1118.spec after the nudge
  continuations. The queue is held by disk (17 GB free, floor 25.5 GB).
- Collect E0071 results once somebody looks at the onset data: does the
  onset at L 200 agree with the paper's box at f* 0.44?

## Jobs in flight

None for this line. The queue (qx7.sh, PID 75429) holds E0074-E0076 until
disk frees up.

## Key evidence

- evidence/E0070-results.json (cost holds)
- evidence/wider-vs-deeper.md (tradeoff)
- evidence/D0054-width200-fields.json (field storage reduction)
- sequel-data/runs/E0071/ (onset loop data, 311 MB)
