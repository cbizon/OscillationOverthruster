# L0009 Option four (clusterlifter) — progress

## Current state (after Nov 21 session)

Branch `method/held-contact` commit 8f8f999 (v5): gap-limited friction added.
The gap limiter (`_friction_gap_limit`) scans all particles before each plate
or wall friction impulse and scales the impulse to prevent drift into touching
neighbours over one dt_hold.  Post-step re-prediction tolerance narrowed from
1e-3 to 1e-6.  Friction defaults to off: the limiter delays overlap failures
from cycle 1 to cycle 10-11 but does not fully resolve them (remaining overlaps
may involve cluster members or wall-friction z components).

Branch `method/held-contact-mu0` (ee877c7): clusterlifter with MU=0 for
diagnostics.  Pinned.

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

## Energy comparison (E0086-energy-comparison.json)

Per-cycle comparison of clusterlifter (E0081) versus unmodified engine (E0031)
at six Gamma 5 conditions, over the cycles both ran.  Hold energy always a
loss (hold fraction of plate work: -2.6e-6 to -9.5e-5).

## Friction overlap investigation (D0055)

Root cause: plate friction in hold steps changes the held sphere's horizontal
velocity, causing drift of about 2.3e-7 per dt_hold into touching neighbours.
Gap limiter implemented but partial.  Next: extend to cluster members and wall
friction z-components.

## Jobs in flight

E0086 on Hatteras: four clusterlifter runs at Gamma 5 deep layers (depths 10
and 15, f* 0.3 and 0.5), width 100, seed 1, 120 cycles, no CPU cap.  Jobs
164638 to 164641, submitted 2026-11-22 04:09.  Estimated finish: 2 to 10 hours.

## What's next

1. Collect E0086 from Hatteras: per-cycle audit data with hold energy visible.
2. Complete the friction gap limiter (extend to cluster members and wall z).
3. With friction working, rerun the E0084 bulk check with friction on.
