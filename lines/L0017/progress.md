# L0017: Slow loops

## What this line does

Near the transition, go back and go up and down much slower to look for
hysteresis just at those points. The question is whether the gap between the
way up and the way down at f* 0.44 is real (it stays when we slow down) or a
ramp-rate artifact (it closes when we give the system more time at each step).

## Done

- **E0064** (100 cycles per step, f* 0.44, Gamma 1.9 to 2.6 and back,
  no friction, one seed): largest gap 0.200 D. Falsified on (ii).
- **E0069** (400 cycles per step, same loop): largest gap 0.103 D at Gamma
  2.2; edge steps still drifting. Falsified on (iii).
- **E0090** (settle-then-step loop, stopping rule D0056; Hatteras job
  164664, artifact A0173; collected Nov 24): all 29 steps settled, 200 to
  400 cycles each (14 at 200, 9 at 250, 4 at 300, 2 at 400), 48.14
  CPU-hours, no slow stretch, clean audit.
  - Registered measure (A over the whole step): largest gap 0.111 D at 2.25,
    0.108 at 2.2. Falsified on (iii) as registered.
  - Settled window (last 100 cycles): gap 0.021 at 2.2, 0.048 at 2.25,
    largest 0.057 at 2.5 where both branches wander by about 0.05 D.
  - The whole-step measure is dominated by relaxation: the 2.2 way-down step
    falls 0.37 to 0.15 D over 300 cycles, then is flat.
  - Stopping rule is lenient (1-df error): 2.55 up passed while falling
    0.62 to 0.54 D in its last 100 cycles.
  - Evidence: `evidence/E0090-results.json` (has the 25-cycle amplitude
    series of every step), from `tools/settle_loop_gap.py LOOPDIR E0090 OUT`
    run on `program fetch --max-mb 300 A0173:out/loop`.
  - The old `loop_analysis.py` / `rates_table.py` that made E0064/E0069
    evidence are not in the repository; settle_loop_gap.py reimplements the
    amplitude (same formula as settle_ramp.py) and reads the fixed-rate gaps
    from `evidence/E0069-results.json`.

## Jobs in flight

None.

## Next

Waiting for Chris (questions in `sessions/2026-11-24-L0017.json`):
- two more seeds of the settle-then-step loop at f* 0.44 (about 50
  CPU-hours each on Hatteras, run in parallel, ~2 days), possibly with a
  stricter stopping rule; needed for a physical-result claim (3 seeds);
- or a second f* (0.38 or 0.33);
- or stop. Default if unanswered: nothing runs on this line.
