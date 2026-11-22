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

## What's next

- **Collect E0089** from Hatteras and test the inelastic ball prediction:
  does the cost peak near 4.6 and drop to the 4.3 level by 5.0?
- Once E0089 completes, overlay measured cost on the ball model.
- Compare nudge and no-friction passes over the common Gamma range.

## Jobs in flight

| Experiment | Host | Job ID | f* | From Gamma | Description |
|---|---|---|---|---|---|
| E0089 | hatteras | 164647 | 0.33 | 4.50 | nudge loop continuation, 48h guard |
| E0089 | hatteras | 164648 | 0.38 | 4.45 | nudge loop continuation, 48h guard |
| E0089 | hatteras | 164649 | 0.44 | 4.45 | nudge loop continuation, 48h guard |
| E0089 | hatteras | 164650 | 0.50 | 4.45 | nudge loop continuation, 48h guard |
| E0089 | hatteras | 164651 | 0.57 | 4.50 | nudge loop continuation, 48h guard |
| E0089 | hatteras | 164652 | 0.65 | 4.45 | nudge loop continuation, 48h guard |
| E0089 | hatteras | 164653 | 0.74 | 4.45 | nudge loop continuation, 48h guard |
| E0089 | hatteras | 164654 | 0.84 | 4.50 | nudge loop continuation, 48h guard |

## Key evidence files

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
