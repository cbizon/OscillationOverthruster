# L0001, Nudge: progress

Rewritten 2026-11-24 (run for the Nov 23 23:42 instruction in
`lines/L0001/instruction.md`).

## Where it stands

- The line's question (judge the position nudge on its own against the
  full-physics baseline; the elastic-window half went to L0007, closed) is
  answered as far as the referee can judge today. Summary of the record,
  with sources: `evidence/L0001-closing-review-2026-11-23.json`.
  - Survival: 17 of 18 2D Gamma 5 runs to 1000 cycles (unmodified 0 of 18);
    one overlap at Gamma 5, f* 0.3, depth 10, seed 1. 3D survival case:
    five seeds, 1000 cycles.
  - Energy audit: clean after the accumulator fix (E0044).
  - Bulk check: passes wherever a baseline exists (case g only weakly).
  - Frozen engine tests: never run on method/nudge. Figure 1 comparison:
    not built for any method (referee/README.md section 2).
  - By design (notes/contact-options.md) it can't become the default.
- The phase diagram did not supersede the line; it uses the nudge as an
  engine. That work is L0015's (E0089 loops on Hatteras).

## Waiting for

- Chris: close now (recommended), or close after one frozen-test run on
  16f3334 (the nudge with the accumulator fix, used by the phase-diagram
  loops).
- B0008: method/nudge (b608fef, 16f3334) isn't in the clone on the Linux
  machine these runs now use. Needed for the frozen-test run, and for any
  nudge job submitted from here.

## If asked to run the frozen tests

Get the branch onto this machine (Chris), make a worktree under
`sequel-data/worktrees/nudge` at 16f3334, run `uv run pytest referee/tests`
from main's referee against that engine the way the ride/plate-stick checks
did (see PROGRAM.md, Option 4 / ride sections), record the result as an
evidence file, then close the line.

## Jobs in flight

None for this line.
