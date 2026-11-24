# L0020 Grapenuts evaluation: progress

Question (Chris, Nov 19 debrief): "Evaluation of the code in
~/Projects/experiments/grapenuts which is another solution to this problem.
Evaluation means both having the checker look at it, but also building a
phase diagram, comparing energies to baseline, etc."

Asked (Nov 22): "Let grapenuts run." and unpaused (Nov 21).

## State (Nov 24, run 3 of the Nov 22 instruction)

- The clone is here: `~/Projects/experiments/sequel-data/grapenuts`, HEAD
  486d8eb on `main`. B0007 resolved. My work is on its branch `sequel-eval`
  (23a3676: `scripts/sequel_long_contact.py`); the engine is untouched.
- **Code description for the checker**: `lines/L0020/grapenuts.md`, from
  the code at 486d8eb (diffed against sequel 6eae1cb, its stated source).
- **Why not the referee script directly (D0066)**: `referee/long_contact.py`
  builds `Simulation` with default arguments, which in grapenuts is the hard
  engine, and its audit has no spring-dissipation term (so every spring
  cycle "fails" at 1e-2). `sequel_long_contact.py` is a step-for-step copy
  of the referee loop with contact settings as arguments, both residuals
  recorded, spring counters per cycle, and `quantities.npz` from the
  referee's own `bulk.frame_quantities`.
- **E0099** (Hatteras, jobs 165011-165028): tc, k = 1e7, 20 kicks per t_c,
  walton; the 12 2D grid conditions (L 100, seed 1) and 3D Gamma 5 f* 0.44
  N 2400 L 20, 120 cycles; plus 5 hard controls (mode never) at the
  conditions sequel's engine completes. See "Jobs" and
  `evidence/E0099-results.json` (`python3 tools/grapenuts_collect.py`
  rebuilds it from the mirror).
- **E0100** (Hatteras, jobs 165029-165033): 1020-cycle referee baselines
  with sequel's unmodified engine (main 7539836) at the 5 shallow 2D
  conditions, for `bulk.py judge` against E0099. The earlier friction-on
  baselines (E0020, E0031) are on the Mac, not on this container.

## Next

1. `program jobs`; rerun `python3 tools/grapenuts_collect.py`; write the
   E0099 outcome if not yet written.
2. E0100: for each finished baseline, `program fetch <artifact>:run/quantities.npz`,
   `bulk.py baseline --from-cycle 20 --cycles 100 --blocks 10`; fetch E0099's
   `run/quantities.npz` at the same condition, `bulk.py measure --from-cycle 20
   --cycles 100`; `bulk.py judge`. Write `evidence/E0100-results.json` and
   the outcome.
3. Stiffness sensitivity (k = 1e6 and 1e8 at a few conditions) before any
   claim: k is a constant the method adds.
4. Phase diagram: the fast pass of L0016/L0018 (ten frequencies, Gamma up
   and down, same box and ramp) with grapenuts; cost per cycle from E0099
   (2D L 100: 0.2 to 23 s per cycle; check the width the passes use).
   Needs a ramp driver in the grapenuts script; read L0016's pass code first.

## Jobs

See the bottom of this file, rewritten at the end of each run.
