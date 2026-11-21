# L0009 Option four (clusterlifter) — progress

## Current state (after Nov 20 session)

Branch `method/held-contact` commit 3983f59 (v4): hold energy is now booked
in EN_HOLD only, not in plate dissipation, so the referee's energy audit
shows hold energy as a residual per cycle. EN_HOLD_GAINS tracks the sum of
positive hold-step net values. Friction infrastructure is coded (plate, wall,
sphere-sphere) but defaults to off (D0053): any velocity change from friction
in a hold step exposes pre-existing position-space overlaps in dense layers.

## Bulk check results (E0084)

- Gamma 3.5, f* 0.3, depth 5: pass (worst 1.10 sd)
- Gamma 3.5, f* 0.5, depth 5: pass (worst 1.29 sd)
- Gamma 3.5, f* 0.5, depth 10: pass (worst 0.80 sd)
- Gamma 3.5, f* 0.3, depth 10: FAIL (every quantity; horizontal energy +36%)

## Jobs in flight

E0083: four clusterlifter runs and four baseline runs at Gamma 5 deep
layers (depths 10 and 15, f* 0.3 and 0.5), launched 2026-11-20 23:30 as
background jobs. PIDs: held 10215, 10230, 10245, 10260; main 10286, 10301,
10316, 10331. Expected: hours (the f* 0.5 depth 15 run may take 10 hours).

## What's next

1. Collect E0083 when finished: per-cycle audit data with hold energy
   visible as the residual, events per sphere per cycle; build the
   energy comparison table (item 4).
2. Investigate the depth-10 bulk failure.
3. Fix friction: resolve the overlap handling so friction can run.
