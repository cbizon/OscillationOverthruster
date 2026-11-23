# L0020 Grapenuts evaluation: progress

Question (Chris, Nov 19 debrief): "Evaluation of the code in
~/Projects/experiments/grapenuts which is another solution to this problem.
Evaluation means both having the checker look at it, but also building a
phase diagram, comparing energies to baseline, etc."

Asked (Nov 22): "Let grapenuts run." and unpaused (Nov 21).

## State (Nov 23, run 3: the first run that started)

- Nothing of grapenuts has been read or run yet. The clone the instructions
  name (`~/Projects/experiments/sequel-data/grapenuts`, commit 486d8eb) is
  not on this machine (Linux container), nor is the original. Blocker B0007.
- E0095 (D0062, job hatteras-164948, A0112): a read-only Hatteras job
  looked for the copy shipped there for Chris's test run. None: the
  workdir's `git/` holds only `sequel.git` and `research-programs.git`, and
  no run folder has a grapenuts checkout. Falsified; B0007 stays open.
- Next run: if `sequel-data/grapenuts` exists, check `git rev-parse
  486d8eb`, then start at step 1 of the plan. If not, nothing to do but
  carry B0007.
- Baseline data to reuse (no new baseline runs needed for a first pass):
  fast-pass baseline with friction E0068/E0073 (L0016), width-200 passes
  E0074/E0075/E0076 (L0018, running), referee bulk baselines used by
  E0084 (L0009) at the 2D shallow conditions.

## What would answer the items

- A code description for the checker: what grapenuts does with lasting
  contacts (springs applied as small kicks between free flights), every
  constant it adds, how it books energy, and how it differs from the
  paper's collision model; written to `lines/L0020/grapenuts.md` from the
  code at 486d8eb.
- Survival and energy audit at the referee conditions: Gamma 5, f* 0.44,
  N 2400, L 20 (3D) and the twelve 2D grid conditions, 120 cycles, with the
  per-cycle energy balance (plate work, collisional loss, spring
  energy, anything added by fiat).
- Bulk physics against the baseline (`referee/bulk.py judge`: 100-cycle
  mean within 3.61 block sd of a 10-block baseline) where the unmodified
  engine runs (2D shallow conditions) or the C code runs (2D Gamma 3.5).
  Grapenuts' output must be converted to the keys `bulk.py measure` reads
  (`granular/export.py` format); that converter is the first code to write.
- Phase diagram: pattern versus Gamma (up and down) at the ten frequencies
  of the fast passes (L0016, L0018), same box and ramp, so it can be laid
  over the baseline, nudge and no-friction diagrams.

## Plan once the code is here

1. Read it; write `grapenuts.md`; run its tests locally (139 passed on
   Hatteras).
2. Register a pilot (Hatteras): survival + energy at the 2D grid and the
   3D Gamma 5 case, 120 cycles, seed 1; measure cost per cycle.
3. Converter to export format; bulk judge at the shallow 2D points.
4. Phase-diagram pass registered from the pilot's costs.

## Jobs

- None running. E0095 (hatteras-164948) collected Nov 23.
