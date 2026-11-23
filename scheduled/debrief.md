Prepare the morning debrief for the sequel research program, and wait for
Chris to discuss it.

Work in ~/Projects/experiments/sequel. First run `git pull`: if the always-on service runs
this program, its runs are on the remote and not here yet. Then run `uv
run --project ~/Projects/experiments/research-programs program check`. Find what ran since the last
debrief: the night's report, `~/Projects/experiments/sequel-data/logs/YYYY-MM-DD/night.md` (dated
by the evening the night started), if the night runner ran; otherwise the
summaries and reviews the service committed since the last debrief (`git
log --since=yesterday -- sessions reviews`). A line's later runs in a day
are numbered (`sessions/YYYY-MM-DD-L0013-2.json`). Then read DIRECTION.md,
PROGRAM.md, the instruction, and for each run its summary
(`sessions/YYYY-MM-DD-L0013.json`) and the checker's review of it
(`reviews/YYYY-MM-DD-L0013.json`). If nothing ran, say so first. Then write
the debrief for a scientist who didn't watch the runs and hasn't read the
session files or transcripts.

The instruction's "Asked" section is what Chris asked for, in
Chris's words. The debrief answers those questions as they were
asked. If the session answered a different question, or built something
other than what was asked, say that; don't adopt the session's framing.

Organize it around lines of research, not around the order of the night or
the files you read. Each line ran on its own, with its own summary and
review; everything about a line goes in its own section, in one place, under
the name it has on the program map.

1. Opening: one or two sentences. How many decisions are waiting, and the
   single most important finding (the checker's, if it changes what the
   session concluded).
2. Terms: a line each for the terms the debrief depends on (methods,
   conditions, checks). Define anything else where it is first used. Never
   use a name, label or id that the debrief hasn't introduced.
3. What you asked: for each line, each item from its section's "Asked",
   word for word, followed by the answer in the same terms: yes, no, a
   number, or "not answered" with why. Add the checker's verdict on whether
   it was answered, and anything the run did differently from what was
   asked. Say which lines ran only to answer challenges, and which were
   instructed but didn't run, and why (from the night's report).
4. One section per line of research that was active, each in this order:
   - what it is and why it is being done;
   - what was built or run (which conditions, how many starts, how long);
   - what the agent concluded;
   - what the checker found: whether each claim holds, is doubtful or is
     broken, and why. A challenged claim is not a headline result;
   - what stands, and what is still open.
   Give numbers with what they mean. Say which item under "What you asked"
   the line serves, or that nobody asked for it.
5. How the night ran: the problems in the night's report, the checker's
   verdicts on how each run went, anything `program check` reported
   (failures, approvals in the last day), the budget, and discrepancies in
   the records.
6. Decisions for Chris: only questions Chris can answer
   from this debrief alone, without reading the ledger. Put each in plain
   language, in the terms Chris has used, with the line it belongs
   to, what happens by default, and your recommendation with a one-line
   reason. If you can't put a question that way, don't ask it: say the
   agent's default applies.
7. Lines the agent proposed (`status: "proposed"`): for each, its question
   and reason, and your recommendation. It runs only if Chris
   approves it.
8. A draft of tonight's instruction, in the format below. Only lines with
   a section run tonight (and lines with open challenges), so ask which
   lines Chris wants run.

Report only what the files say, and mark any inference of your own as
yours.

Then run `uv run --project ~/Projects/experiments/research-programs program map`. It writes the program
map, a page of the lines of investigation against nights, to the path it
prints. Show Chris the page: publish it as an artifact if you can,
updating the one from earlier days instead of making a new one. The lines
in your debrief are the lines on the map, under the same names.

Then discuss. When Chris decides something about a line (opens one,
pauses, drops or closes one, or settles a question in it), append the
record to ledger/lines.jsonl with `by: "human"`: a `note` with `night` set
to today's date (the night the instruction is for) giving the decision in
Chris's words, with `planned: true` if it sets work for tonight, and
an `update` if the status changed. Approving a proposed line is an
`update` with `status: "active"`. Run `program check` and commit it with
the instruction.

## The instruction

The instruction has a section per line to run tonight, headed
`## L0013 <line name>` (see instructions/README.md), each with two parts.
Anything above the first line section applies to every line; keep it to
housekeeping.

- `### Asked`: a numbered list of what Chris asked for this line in
  this conversation, in Chris's own words, quoted and not
  paraphrased. One item per request. Trim, but don't reword, merge or
  reinterpret. A request that spans lines goes in each line it asks
  something of.
- `### Details`: what the agent needs to carry each item out (conditions,
  order, approvals, housekeeping), written for the agent, each point tied
  to an item by number or marked as housekeeping.

Details may add to an item. They may not narrow or defer part of it. If you
think part of a request should wait or be done differently, tell
Chris so before saving, and put the agreed wording under Asked.

When Chris agrees on tonight's instruction (each line's Details
under about 250 words), save it as instructions/YYYY-MM-DD.md dated today,
run `uv run --project ~/Projects/experiments/research-programs program run-night --dry-run` and show
Chris which lines will run and why, then commit it on `main`.
