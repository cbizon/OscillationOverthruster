# Brief: sequel

Human-only: Chris writes this; the agent reads it after `DIRECTION.md`
every session. It holds what is specific to this program's day-to-day work;
the general rules are in `CLAUDE.md`.

The program runs locally on Chris's Mac. Whether that works well enough is
itself under test (RQ0 in `PROGRAM.md`), which is why the run conditions in
every summary matter here.

## Start-of-session checks

- Run the frozen engine tests: `uv run pytest referee/tests`. If they fail
  on `main`, fixing that comes before anything else.

## Where code goes

- Each contact-handling idea is developed on its own branch,
  `method/<short-name>`, in a worktree under
  `~/Projects/experiments/sequel-data/worktrees/`. Branch from `main`.
- The engine is `granular/`. Ideas change the engine on their branch;
  `referee/` always comes from `main`.

## How to run things

All of the referee's tools are described in `referee/README.md`; read it
before using them. In short:

- `referee/long_contact.py --engine <worktree> ...` runs one condition
  with a method's engine and records survival (with slow episodes), a
  per-cycle energy and momentum audit, and per-frame bulk quantities. A run
  ends on a non-physical state, its CPU budget, frozen time, or completion;
  being slow is recorded, not stopped.
- `referee/bulk.py measure`, `baseline`, `judge`: bulk quantities over a
  window, a 10-block baseline, and the pass rule.
- `referee/c_baseline.py`: the 1998 C code in 2D, the baseline where this
  engine stalls.
- Costs measured so far: a 2D condition takes about 0.01 to 0.1 s per cycle
  with this engine (a 1,020-cycle baseline in about 30 s with the C code);
  the 3D N = 2400 case about 1 s per cycle. 3D at N = 60000 is not measured
  yet.

## Comparisons

- Settle 20 cycles, measure 100; baselines are 10 blocks of 100 cycles
  from one run (`referee/README.md`, pass rule).
- Where this engine runs the condition without a contact method, that is the
  baseline; where it stalls, the C code is; where both stall (2D Gamma = 5,
  depths 10 and 15), compare methods with each other and rely on the energy
  audit and smoothness across neighbouring conditions.
- The 2D grid and 3D conditions are listed in `referee/README.md`.
