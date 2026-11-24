# L0020 Grapenuts evaluation: progress

Question (Chris, Nov 19 debrief): "Evaluation of the code in
~/Projects/experiments/grapenuts which is another solution to this problem.
Evaluation means both having the checker look at it, but also building a
phase diagram, comparing energies to baseline, etc."

Asked (Nov 22): "Let grapenuts run." and unpaused (Nov 21).

## State (Nov 24, run 3 of the Nov 22 instruction; summary sessions/2026-11-23-L0020-3.json)

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
   E0099 outcome.
2. Bulk judge (`uv run python tools/grapenuts_judge.py`) needs baselines;
   on Hatteras sequel's engine fails Gamma 3.5 f* 0.3 depth 10 and Gamma 5
   f* 0.5 depth 5 at seed 1, so try seeds 2 and 3 there.
3. k = 1e8 at the full grid with three seeds (survival, energy sign, bulk);
   check the small net gain at high k (finer step at k = 1e8?).
4. Phase diagram: the fast pass of L0016/L0018 (ten frequencies, Gamma up
   and down, same box and ramp) with grapenuts; cost per cycle from E0099
   (2D L 100: 0.2 to 23 s per cycle; check the width the passes use).
   Needs a ramp driver in the grapenuts script; read L0016's pass code first.

## Results so far (Nov 24)

- E0099 (k = 1e7): 10 of 12 2D conditions completed 120 cycles; net energy
  over every run a loss (-4e-5 to -1.8e-3 of throughput); single cycles
  gain up to +9.5e-3 (Gamma 5 f* 0.3 depth 10). Hard controls: 3 of 5
  complete; the other two fail exactly as sequel main does on Hatteras.
- E0100 (outcome written): baselines at 3 of 5 shallow conditions; k = 1e7
  fails Gamma 3.5 f* 0.5 depth 10 on plate contact (3.80 sd).
- E0101 (outcome written): k = 1e6 fails 2 of 3, k = 1e8 passes 3 of 3; at
  k = 1e8 Gamma 3.5 f* 0.5 depth 5 gains energy on net (+8.3e-6).
- Grapenuts' own test suite: hangs or is very slow at test 90 of ~139 on
  this container (two tries, no failures before it); not resolved.
- Note: `uv run` in the sequel worktree rewrites `uv.lock`; `git checkout
  uv.lock` before `program submit` or commits.

## Jobs

Still running at the end of the Nov 24 run (E0099, Hatteras; collect with
`program jobs`, then `python3 tools/grapenuts_collect.py` and write the
E0099 outcome):

- 165019: 2D Gamma 5 f* 0.3 depth 15 (60 of 120 cycles, about 24 s/cycle)
- 165022: 2D Gamma 5 f* 0.5 depth 15 (80 of 120, about 19 s/cycle)
- 165023: 3D Gamma 5 f* 0.44 N 2400 L 20 (100 of 120, about 17 s/cycle)

All other E0099, E0100 and E0101 jobs are collected.
