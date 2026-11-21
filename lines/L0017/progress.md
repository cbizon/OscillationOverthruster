# L0017: Slow loops

## What this line does

Near the transition, go back and go up and down much slower to look for
hysteresis just at those points. The question is whether the gap between the
way up and the way down at f* 0.44 is real (it stays when we slow down) or a
ramp-rate artifact (it closes when we give the system more time at each step).

## Done

- **E0064** (100 cycles per step, f* 0.44, Gamma 1.9 to 2.6 and back,
  no friction, one seed): complete, 29 steps, 10.78 CPU-hours. The gap
  narrowed from 25 to 100 cycles (0.242 to 0.200 D) but did not close;
  edge steps still drifted by up to 0.11 D. Falsified on (ii).
- **E0069** (400 cycles per step, same loop): complete, 29 steps,
  34.44 CPU-hours, 361 MB. No slow stretch, no audit failure.
  - Largest gap: 0.103 D at Gamma 2.2 (range 2.2 to 2.25), down from
    0.200 D (range 2.2 to 2.3) at 100 cycles.
  - Within-step drift: larger at 400 than at 100 at Gamma 2.25 going up
    (0.113 vs 0.070 D) and 2.2 going down (0.150 vs 0.095 D); smaller
    at 2.3 up and 2.15 down. Falsified on (iii).
  - Pattern: the gap has moved inward and shrunk, but the edge steps are
    still drifting, so the loop has not converged.

## Jobs in flight

None.

## Next

- The 1600-cycle loop is the next rate. It costs about 138 CPU-hours (5.8
  days on one core) and would show whether the gap continues to shrink or
  has stabilised. Waiting for Chris.
