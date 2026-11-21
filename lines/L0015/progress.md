# L0015: Fast pass, nudge

## What's done

- **E0065 (fast pass, ten frequencies):** Complete. Each loop starts at
  Gamma 3.0, goes down to a floor (Gamma 2.0 to 2.35), up to a wall at
  Gamma 4.35 to 4.50, clean audit. The wall is period-2 bouncing: the
  layer alternates between a high-bounce cycle (airborne, few collisions)
  and a low-bounce cycle (chattering on the plate, many collisions). The
  heavy cycle's collision count grows rapidly with Gamma and drives the
  cost. The spatial pattern (wavenumber 3-4 at f* 0.44) weakens through
  the wall and disappears by Gamma 4.4.

- **E0072 (continuations above the wall):** Each of the eight loops got
  one step past E0065's wall (Gamma 4.50 or 4.55) and hit the 2 CPU-hour
  per step guard. All processes are dead. The continuation is not restarted;
  the instruction said to keep it queued behind the baselines.

- **E0085 (wall analysis):** The period-2 is documented at f* 0.44 and
  0.84. At f* 0.44: even-odd event ratio 4.6 at Gamma 4.0, 11.1 at 4.5;
  CPU per cycle doubles between 4.4 and 4.45 and again between 4.45 and
  4.5. At f* 0.84: event ratio 1.4 at 4.0, 14.5 at 4.5; wall is 0.1
  higher in Gamma.

## What's next

- Decide whether to push the nudge above Gamma 4.5 (costly) or accept
  coverage to 4.4-4.5 and test the clusterlifter there instead.
- The nudge pass data is complete enough for comparison with the no-friction
  pass (E0060) and the baseline pass (E0073, once collected) over the common
  Gamma range below the wall.

## Jobs in flight

None. All E0072 jobs are dead.

## Key evidence files

- `evidence/E0065-results.json` (all ten loops)
- `evidence/E0085-nudge-wall-fields.json` (wall analysis)
- `evidence/E0059-results.json` (pilot)
