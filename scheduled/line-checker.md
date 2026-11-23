# Checking one line's run

<!-- Rendered from RoboRobo's template by `program sync`; don't edit here. -->

`program run-night` starts you right after one line's run of sequel, and
names the run's summary, `sessions/YYYY-MM-DD-L0013.json` (`L0013` and the
date stand for the line and night you were given). Read CHECKER.md and
follow it for that run:

- The "session" CHECKER.md speaks of is this run: its summary, the part of
  the night's instruction it followed (the `## L0013` section, with
  anything above the first line section), and the records it added.
- Your previous review of this line is the latest
  `reviews/*-L0013.json`; check its open challenges were answered.
- Write `reviews/YYYY-MM-DD-L0013.json` with `line_id` set, or the file
  the prompt names. If that file
  already exists, stop.
- If the summary doesn't exist, write the review anyway, saying so in
  `summary`, with an empty `reviews` list.
- Finish within 45 minutes. Commit only your review, on
  `main`, and leave nothing uncommitted.
