# L0009 Option four (clusterlifter) — progress

## Current state (after Nov 23 session)

Branch `method/held-contact` tip commit **8f8f999** (v5).  No code changes were
made tonight.  The session wrote `lines/L0009/clusterlifter.md`: a full
description of the method (step-by-step mechanics, deviation table with every
parameter and its decision record, runs table for all ten experiments).

Waiting for Chris's direction on the two open design problems:

1. **Energy audit failure**: every cycle fails at all four deep Gamma 5 E0086
   conditions (threshold 1e-8; worst residual 2e-4, all negative).  The hold
   steps are dissipative (~1e-4 of plate work per cycle removed), not
   energy-injecting.  This was invisible in v3 (absorbed into EN_PLATE_DISS);
   v4 made it a visible residual (EN_HOLD).  Whether it is fundamental to the
   impulse-step method or reducible by design is unclear.

2. **Post-hold-step overlap tolerance** (`htol`): 1e-3 (v4) or 1e-6 (v5) when
   friction on, vs standard PAIR_PENETRATION_TOL = 2e-8.  No decision record
   for introducing 1e-3 in v4.  Chris said he does not tolerate it.

No jobs are in flight.

## Bulk check results

- E0084 (clusterlifter, friction off, against friction-on baseline):
  - Gamma 3.5, f* 0.3, depth 5: pass (worst 1.10 sd)
  - Gamma 3.5, f* 0.5, depth 5: pass (worst 1.29 sd)
  - Gamma 3.5, f* 0.5, depth 10: pass (worst 0.80 sd)
  - Gamma 3.5, f* 0.3, depth 10: FAIL (every quantity; horizontal energy +36%)

- E0087 (clusterlifter mu=0, against mu=0 baseline):
  - Gamma 3.5, f* 0.3, depth 10: PASS (worst 0.69 sd)
  - Conclusion: the E0084 failure was from comparing different friction settings,
    not from the hold method.

## E0086 deep Gamma 5 results

Collected Nov 23.  Four runs at Gamma 5, friction off, v4 engine (3983f59f),
width 100, N 1000/1500 for depths 10/15.  Artifacts A0090–A0093.

| condition | outcome | cycles | audit failures |
|---|---|---|---|
| f* 0.3, depth 10 | TIMEOUT at 110 cycles | 110 | 109 of 109 (worst 8e-5) |
| f* 0.3, depth 15 | frozen_time at cycle 96 | 95 | 95 of 95 (worst 1.1e-4) |
| f* 0.5, depth 10 | TIMEOUT at 70 cycles | 70 | 70 of 70 (worst 1.5e-4) |
| f* 0.5, depth 15 | completed 120 cycles | 120 | 120 of 120 (worst 2.0e-4) |

Energy audit: all cycles fail in all four runs; no energy gains.  The failures
are from hold-step energy removal, now visible as EN_HOLD residuals in v4.

## Friction overlap investigation (D0055)

Root cause: plate friction in hold steps changes the held sphere's horizontal
velocity, causing drift of ~2.3e-7 per dt_hold into touching neighbours.  Gap
limiter implemented in v5 (D0055); delays overlap failure from cycle 1 to
cycle 10-11 but partial.  Remaining overlaps may involve cluster members or
wall-friction z-components.  Friction defaults to off.

## What's next

Awaiting Chris's direction on the two open design problems above.  No new
experiments should be run until the energy audit failure and the overlap
tolerance are resolved.  Possible directions (see session summary
proposed_directions):

1. Remove the overlap tolerance and redesign the hold step to not create
   overlaps (position correction instead of velocity correction).
2. Per-step energy accounting to identify which contacts remove energy and by
   how much; then judge whether the removal is fundamental or reducible.
3. Consider whether the impulse-step method can pass the energy audit at all,
   or whether the threshold needs revision with explicit justification.
