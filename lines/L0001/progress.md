# L0001, Nudge: progress

Rewritten 2026-11-24 (run for Chris's Nov 24 00:04 answer in
`lines/L0001/instruction.md`: "Yes run the frozen engine tests").

## Where it stands

- Everything asked is done. Waiting for Chris to close the line.
- Frozen engine tests: 74 of 74 at b608fef (Nov 6 checker, Nov 7 agent,
  `evidence/frozen-tests-2026-11-07.json`) and at 16f3334 (E0103, Hatteras
  job 165153, artifact A0172, `evidence/E0103-results.json`; main control
  74 of 74 in the same job).
- Survival: 17 of 18 2D Gamma 5 runs to 1000 cycles (unmodified 0 of 18);
  one overlap at Gamma 5, f* 0.3, depth 10, seed 1. Completed runs with
  heavy slow stretches: f* 0.3 depth 10 seeds 2, 3 (47%, 13%), f* 0.3
  depth 15 seed 1 (71%). 3D survival case: five seeds, 1000 cycles.
- Energy audit: the two nudge runs rerun after the accumulator fix (176
  failing cycles) were all round-off (E0044); the remaining ~650 failing
  cycles were not rerun ("likely, not shown").
- Bulk check: passes wherever a baseline exists, but all such conditions
  lack lasting contacts; case g only weakly.
- Corrections from the Nov 23 review are in
  `evidence/L0001-closing-review-2026-11-23.json` ("corrections_2026-11-24").
- By design (notes/contact-options.md) the nudge can't become the default.
  The phase diagram uses it as an engine (L0015).

## Code

- `method/nudge` restored in this machine's clone at 16f3334 from the
  bundle in A0172 (`out/method-nudge.bundle`). B0008 resolved; nudge jobs
  can use `--tree engine=method/nudge` again.
- How E0103 got the commit (D0070): Hatteras keeps a bare repo of shipped
  trees at `<workdir>/git/sequel.git`; a job can clone a commit from it.

## Jobs in flight

None for this line.
