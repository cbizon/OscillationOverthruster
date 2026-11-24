# L0020 Grapenuts evaluation: progress

Question (Chris, Nov 19 debrief): "Evaluation of the code in
~/Projects/experiments/grapenuts which is another solution to this problem.
Evaluation means both having the checker look at it, but also building a
phase diagram, comparing energies to baseline, etc."

Asked (Nov 22): "Let grapenuts run." and unpaused (Nov 21).

## State (Nov 24 05:04Z run, started by the service for jobs 165019, 165022, 165023; summary sessions/2026-11-24-L0020.json)

- The clone: `~/Projects/experiments/sequel-data/grapenuts`, detached at
  486d8eb. My branches in it: `sequel-eval` (23a3676:
  `scripts/sequel_long_contact.py`, the referee loop copied with contact
  settings as arguments, D0066) and `contact-energy` (8030406, on top of
  sequel-eval: per-contact work diagnostic, bookkeeping only).
- Worktree: `sequel-data/worktrees/grapenuts-ce` (contact-energy; same
  dynamics as sequel-eval). Use it for local runs; `uv run python scripts/sequel_long_contact.py --bulk
  <sequel>/referee/bulk.py ...` (about 1 min for 30 cycles at depth 5).
- Code description for the checker: `lines/L0020/grapenuts.md`.
- **All experiments collected; nothing running.**
  - E0099 (falsified on energy): all 13 spring runs at k = 1e7 completed 120
    cycles (12 2D grid + 3D); 1 to 16 gaining cycles at six conditions.
    Hard controls: 3 of 5 completed.
  - E0100: sequel baselines on Hatteras at 3 of 5 shallow conditions; k 1e7
    fails plate contact at Gamma 3.5 f* 0.5 depth 10.
  - E0101: bulk passes at k 1e8 only (3 conditions); k 1e8 gains on net at
    Gamma 3.5 f* 0.5 depth 5.
  - E0102 (falsified on the tangential criterion): per contact, 0.2 to 2.7
    percent of contacts gain overall (summed gain 0.2 to 0.3 of the run's
    net residual); the tangential force alone gains in 1.5 to 6.6 percent.
    Summed contact work minus booked dissipation equals the residual
    exactly, so the diagnostic is sound.
- Checker's review of run 3 (2026-11-23-L0020-3) answered: hidden friction
  gain (E0102), E0099 falsified (outcome written), "on the Mac these ran"
  withdrawn (Mac seeds fail too, E0031), B0007 resolution corrected,
  per-cycle cost max is 26.1 s (not 24).
- D0068: E0102's registration is stamped 05:36Z by mistake; actually
  written about 05:08Z, before its runs.

## Next

1. Waiting on Chris: overlap acceptable? energy tolerance for a
   time-stepped spring? (questions in sessions/2026-11-23-L0020-3.json)
2. Bulk judge where sequel's engine fails (Gamma 3.5 f* 0.3 depth 10,
   Gamma 5 f* 0.5 depth 5, and the deep layers): use the 1998 C code
   (`referee/c_baseline.py`) as baseline, as BRIEF.md says; extra seeds of
   sequel's engine fail on the Mac too (E0031).
3. k = 1e8 over the full grid, three seeds (survival, energy sign, bulk).
4. Where the tangential gain comes from: the Walton collision-phase
   impulse is precomputed and delivered even if the slip has reversed;
   the sustained phase rotates xi keeping its length. Split E0102's
   counter by phase to tell which.
5. Phase diagram: fast pass of L0016/L0018 with grapenuts; needs a ramp
   driver; read L0016's pass code first.

## Notes

- `uv run` in the sequel worktree rewrites `uv.lock`; `git checkout
  uv.lock` before `program submit` or commits.
- Grapenuts' own test suite hangs or is very slow at test 90 of ~139 on
  this container; it passed on Hatteras for Chris.
- No `caffeinate`, `uptime`, `pmset`, `free` on this Linux container.

## Jobs

None running. All E0099, E0100, E0101 Hatteras jobs collected; E0102 ran
locally and finished.
