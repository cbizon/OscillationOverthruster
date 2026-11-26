# Wider box: how far each loop got in Gamma, width 200 against the paper's width 100

Updated 2026-11-26 from evidence/E0076-results.json, evidence/E0075-results.json and evidence/E0074-interim.json, by tools/l0018_pinned_ranges.py. One seed per box and f*.

Each loop changes Gamma (peak plate acceleration over gravity) in steps of 0.05 and holds 25 cycles a step. The *floor* is the lowest Gamma completed going down, the *top* the highest completed going up; in brackets is why the next step stopped and at what Gamma: a CPU cap (the step ran out of its CPU-time allowance, so the stop measures the budget, not the physics), an overlap (two spheres found overlapping) or a stall (simulated time stopped advancing). Width 200 holds four times as many spheres (240000 against 60000) at the same depth.

## Unmodified engine (E0076 at width 200, E0073 at width 100), Gamma 1.7 to 7.0 and back

Step CPU caps: width 200 four times width 100's, while a matching step costs about 7 to 11 times as much.

| f* | floor, width 200 | floor, width 100 | top, width 200 | top, width 100 |
|---|---|---|---|---|
| 0.84 | broke in first step (overlap) | 2.2 (cpu cap at 2.15) | | 4.2 (overlap at 4.25) |
| 0.74 | 2.25 (cpu cap at 2.2) | 2.15 (cpu cap at 2.1) | 4.0 (overlap at 4.05) | 4.1 (cpu cap at 4.15) |
| 0.65 | 2.4 (overlap at 2.35) | 2.25 (overlap at 2.2) | 3.9 (overlap at 3.95) | 4.1 (overlap at 4.15) |
| 0.57 | 2.35 (cpu cap at 2.3) | 2.2 (cpu cap at 2.15) | 3.8 (stall at 3.85) | 4.0 (overlap at 4.05) |
| 0.50 | 2.35 (cpu cap at 2.3) | 2.4 (cpu cap at 2.35) | 4.0 (overlap at 4.05) | 4.05 (cpu cap at 4.1) |
| 0.44 | 2.4 (cpu cap at 2.35) | 2.3 (cpu cap at 2.25) | 4.0 (overlap at 4.05) | 4.0 (stall at 4.05) |
| 0.38 | 2.45 (cpu cap at 2.4) | 2.35 (overlap at 2.3) | 4.0 (cpu cap at 4.05) | 4.0 (stall at 4.05) |
| 0.33 | broke in first step (overlap) | 2.35 (overlap at 2.3) | | 4.35 (cpu cap at 4.4) |
| 0.30 | broke in first step (overlap) | 2.5 (cpu cap at 2.45) | | 4.25 (overlap at 4.3) |
| 0.27 | broke in first step (overlap) | broke in first step (overlap) | | broke in first step (overlap) |

## Nudge model (E0075 at width 200, E0065 at width 100), Gamma 3.0 down to the floor, then up

Step CPU caps: width 200 2 CPU-hours down and 8 up; width 100 0.5 both ways, and 2 up in the continued loops (E0072). A matching step costs about 9 times as much at width 200 going down and 7 to 10 times going up, so every CPU-cap end below measures the budget.

| f* | floor, width 200 | floor, width 100 | top, width 200 | top, width 100 (0.5 cap) | top, width 100 (2 cap) |
|---|---|---|---|---|---|
| 0.84 | 2.3 (CPU cap at 2.25) | 2.0 (CPU cap at 1.95) | 4.5 (CPU cap at 4.55) | 4.4 (CPU cap at 4.45) | 4.5 (CPU cap at 4.55) |
| 0.74 | 2.3 (CPU cap at 2.25) | 2.05 (CPU cap at 2.0) | 4.45 (CPU cap at 4.5) | 4.4 (CPU cap at 4.45) | 4.45 (CPU cap at 4.5) |
| 0.65 | 2.35 (CPU cap at 2.3) | 2.15 (CPU cap at 2.1) | 4.45 (CPU cap at 4.5) | 4.4 (CPU cap at 4.45) | 4.45 (CPU cap at 4.5) |
| 0.57 | 2.4 (CPU cap at 2.35) | 2.2 (CPU cap at 2.15) | 4.45 (CPU cap at 4.5) | 4.4 (CPU cap at 4.45) | 4.5 (CPU cap at 4.55) |
| 0.50 | 2.45 (CPU cap at 2.4) | 2.2 (CPU cap at 2.15) | 4.4 (CPU cap at 4.45) | 4.4 (CPU cap at 4.45) | 4.45 (CPU cap at 4.5) |
| 0.44 | 2.5 (CPU cap at 2.45) | 2.25 (CPU cap at 2.2) | 4.4 (CPU cap at 4.45) | 4.35 (CPU cap at 4.4) | 4.45 (CPU cap at 4.5) |
| 0.38 | 2.45 (CPU cap at 2.4) | 2.25 (CPU cap at 2.2) | 4.35 (stall at 4.4) | 4.35 (CPU cap at 4.4) | 4.45 (CPU cap at 4.5) |
| 0.33 | 2.45 (CPU cap at 2.4) | 2.35 (CPU cap at 2.3) | 4.35 (CPU cap at 4.4) | 4.45 (CPU cap at 4.5) | 4.5 (CPU cap at 4.55) |
| 0.30 | 2.5 (CPU cap at 2.45) | 2.35 (CPU cap at 2.3) | 4.45 (CPU cap at 4.5) | 4.3 (record ends still climbing) | - |
| 0.27 | first step ran out of its CPU cap (49 of 50 cycles) | same at width 100 | | | |

## Friction off (E0074 at width 200, E0060 at width 100), Gamma 1.7 to 7.0 and back

- f* 0.84: width 200 completed all 213 steps, as width 100 did.
- f* 0.74: width 200 completed all 213 steps, as width 100 did.
- The other eight f* are still running at width 200.

Where the spatial pattern appears (the registered test of these experiments) is not yet measured at either width.
