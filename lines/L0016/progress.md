# L0016: Fast pass, baseline

## Status

Complete. All ten baseline loops (E0073) collected; nine provide usable
comparison data.

## What is done

- E0073: ten baseline loops (unmodified engine with friction, half-push
  start, Gamma 3.0 down to the floor, up to 7.0 or failure, back), one per
  frequency from f* 0.27 to 0.84. All dead; outcome recorded as falsified
  on prediction (i).
  - f* 0.27: failed at step zero (physical failure at Gamma 3.0).
  - f* 0.30 to 0.84: 46 to 57 completed steps each. Down floors 2.15
    (f* 0.74) to 2.5 (f* 0.30); up ceilings 4.0 (f* 0.38, 0.44, 0.57) to
    4.35 (f* 0.33). Failure modes on the way up: 4 physical failure, 3 CPU
    budget, 2 frozen time.
  - Total: 462 completed steps, 98.1 CPU-hours, 680 MB on disk.
  - No audit failures, 3 slow episodes (all at f* 0.38).
  - Evidence: `evidence/E0073-results.json`.
- Disk discrepancy explained: `evidence/E0073-disk-discrepancy.json`.
  `program check` sums only the `disk_gb` field from experiment outcomes;
  67 of 73 experiments with outcomes recorded zero (pre-dating the field),
  and 1.8 GB of reference data predates the program's tracking.

## What is next

No new runs planned for this line. The data is ready for cross-engine
comparison (amplitude-versus-Gamma figures for all three engines at the nine
frequencies where all have data).

## Jobs in flight

None.
