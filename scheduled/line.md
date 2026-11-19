# One line's run

<!-- Rendered from RoboRobo's template by `program sync`; don't edit here. -->

`program run-night` starts you for one line of investigation of sequel
and names the line (`L0013` below stands for it) and the night (the evening
it started, `YYYY-MM-DD` below). Follow CLAUDE.md exactly; it says what to
read first and what to write at the end. What is different from a whole
session:

- **Your line only.** Work on this line's question. Read other lines'
  records when you need their results, but don't register experiments in,
  write notes for, or change the state of any other line. Work you think
  another line should do goes in `proposed_directions`.
- **Your part of the instruction** is the `## L0013` section of the
  night's instruction, plus anything above the first line section. Its
  "Asked" items are the ones you answer. If you were started only to
  answer the checker's open challenges, there are no items: answer the
  challenges and stop.
- **Your memory** for this line is `lines/L0013/progress.md`: what's done,
  what's next, jobs in flight with their ids and where they run. Read it
  first; create it if it doesn't exist. Rewrite it at the end so the next
  run of this line can start from it alone.
- **A new line** you think is needed is opened with `status: "proposed"`
  and a `reason`. It doesn't run until Chris makes it active; don't
  register experiments in it.
- **Time.** The runner stops you after its time limit (about an hour).
  Start long work as background jobs (see "Long jobs" in CLAUDE.md), record
  them in `progress.md`, and end the run; a later run collects them. Leave
  ten minutes for the end.
- **Your summary** is `sessions/YYYY-MM-DD-L0013.json`, with `line_id` set.
  `answers` covers this line's "Asked" items. `open_blockers` lists the open
  blockers that affect this line and any that affect no particular line.
- **`PROGRAM.md`**: change only what concerns this line.
- **Commit** your records on `main` before you stop, and leave nothing
  uncommitted: the next line starts from what you leave, and the runner
  stops the night if the repository is dirty or `program check` fails.
- Record `scheduled_start` as the time the runner started you and
  `actual_start` as the time you noted.
- If something outside the program stops you (no network, a tool missing,
  a permission refused), record it as a blocker and in the run conditions,
  write the summary, commit, and stop.
