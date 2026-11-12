Prepare the morning debrief for the sequel research program, and wait for
Chris to discuss it.

Work in ~/Projects/experiments/sequel. Run `uv run --project ~/Projects/experiments/research-programs program check`. Read
DIRECTION.md, PROGRAM.md, the latest session summary in sessions/, and the
checker's review of it in reviews/. Then write the debrief for a scientist
who didn't watch the night and hasn't read the session files or transcripts.

Organize it around lines of research, not around the order of the night or
the files you read. A line of research is one thread of work: a method being
developed, a comparison, a baseline, a question from PROGRAM.md. Everything
about a line goes in its own section, in one place.

1. Opening: one or two sentences. How many decisions are waiting, and the
   single most important finding (the checker's, if it changes what the
   session concluded).
2. Terms: a line each for the terms the debrief depends on (methods,
   conditions, checks). Define anything else where it is first used. Never
   use a name, label or id that the debrief hasn't introduced.
3. One section per line of research that was active, each in this order:
   - what it is and why it is being done;
   - what was built or run (which conditions, how many starts, how long);
   - what the agent concluded;
   - what the checker found: whether each claim holds, is doubtful or is
     broken, and why. A challenged claim is not a headline result;
   - what stands, and what is still open.
   Give numbers with what they mean.
4. How the session ran: the checker's verdict and the facts behind it,
   anything `program check` reported (failures, approvals in the last day),
   the budget, and discrepancies in the records.
5. Decisions for Chris: each of the agent's questions in plain
   language, naming the line it belongs to, what happens by default, and
   your recommendation with a one-line reason.
6. A draft of tonight's instruction.

Report only what the files say, and mark any inference of your own as
yours. Then discuss. When Chris agrees on
tonight's instruction (under about 250 words, written for the agent), save
it as instructions/YYYY-MM-DD.md dated today and commit it on `main`.
