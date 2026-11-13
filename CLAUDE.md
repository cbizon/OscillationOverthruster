# How to work in this program

<!-- Rendered from RoboRobo's template by `program sync`; don't edit here.
     This program's own instructions are in BRIEF.md. -->

You are running one session of sequel, a long research program:
long-lasting contacts in event-driven simulation of vibrated granular layers, and the hysteresis and oscillon experiments they make possible. Nobody is watching the session; Chris reads your summary
in the morning and replies with the next instruction. Your memory between
sessions is this repository. Write everything you'd want to know tomorrow
into it.

Who owns what:

- **Chris's files**, which you never change: `DIRECTION.md`,
  `BRIEF.md`, `budgets.yaml`, `program.toml`, `referee/`, `notes/`, and
  `approvals.json`.
- **RoboRobo's files**, which you never change: this file, `CHECKER.md`,
  `scheduled/`, `.claude/`, and the folder READMEs.
- **Yours**: `PROGRAM.md`, `ledger/`, `sessions/`, `evidence/`, and your
  code on branches.

`program check` fails if any of the first two changed.

## At the start

1. Note the time you started; you need it for the run conditions.
2. Read `DIRECTION.md` (the question, bounds, claim rules, autonomy), then
   `BRIEF.md` (how this program works day to day) and `budgets.yaml`. Read
   the notes in `notes/` that `BRIEF.md` points to before planning: they
   hold Chris's thinking from before the program, and you follow
   them unless an instruction says otherwise.
3. Read `PROGRAM.md`, then the instruction for today in `instructions/`
   (`YYYY-MM-DD.md`, dated by the evening the session starts). If there is
   none, follow `instructions/fallback.md`. The instruction's "Asked"
   section is what Chris wants to know, in Chris's words;
   see "What was asked".
4. Read the last session summary in `sessions/`, the checker's latest review
   in `reviews/`, and any open records in `ledger/blockers.jsonl` and
   `ledger/claims.jsonl`. Answer every open challenge this session: produce
   the evidence that resolves it, narrow the claim, or withdraw it.
5. Check on jobs left running by earlier sessions (see "Long jobs"). Collect
   finished ones before starting new work.
6. Run `uv run --project ~/Projects/experiments/research-programs program check`. If it fails, fixing
   what it reports comes first; if you can't fix it, record a blocker, write
   the summary, and stop.
7. Do any start-of-session checks `BRIEF.md` lists.

## What was asked

The session exists to answer the items under "Asked" in the instruction, as
they are worded. "Details" says how; where the two seem to disagree, "Asked"
wins and you say so in the summary.

- Before planning, write down for each item what result would answer it.
  If your plan can't produce that result, change the plan, not the
  question.
- Don't replace a question with a neighbouring one you find more
  interesting or easier to test. A finding nobody asked for goes in
  `proposed_directions`; it doesn't take the night.
- If an item is unclear, take the reading closest to the words, do that,
  and say which reading you took. Don't build on a reading the words don't
  support.
- When you test a change (a method, a fix, a setting), first show that it
  acted: where its output first differs from the unchanged version, and how
  often the new code path ran. A run identical to the baseline tests
  nothing, and you say so instead of reporting a result.
- A choice the instruction didn't make that changes what is being tested is
  a decision: record it, and list it under that item's `departures`.

## Where work goes, and keeping the machine clean

- Records (`PROGRAM.md`, `ledger/`, `sessions/`, `evidence/`) are committed
  on `main`. Code you try out goes on branches as `BRIEF.md` says; merging
  into `main` needs Chris.
- Large outputs go under `~/Projects/experiments/sequel-data/runs/<experiment-id>/`, never in git.
  Keep only what a claim needs, and record the size of what you keep in the
  evidence file.
- Stay inside `~/Projects/experiments/sequel` and `~/Projects/experiments/sequel-data`. Write nothing anywhere else,
  including temporary files: use `~/Projects/experiments/sequel-data/tmp/` and empty it before the
  session ends.
- Before starting jobs and at the end of the session, check free disk
  (`df -h ~`), the size of `~/Projects/experiments/sequel-data` (`du -sh`), and memory
  (`memory_pressure`), and stay within the limits in `budgets.yaml`. Delete
  intermediate output nobody will use. Never delete evidence a ledger
  record points to.

## While working

- **Pre-register.** Before running an experiment, get an id with
  `uv run --project ~/Projects/experiments/research-programs program next-id E` and append a
  `registration` to `ledger/experiments.jsonl`: the hypothesis, the method,
  how the result will be judged, what would falsify it, and the estimated
  cost in the resources `budgets.yaml` names. Don't change a registration
  once results exist; register a new experiment that supersedes it. The
  ledger is append-only: never edit or delete a line. Schemas are in
  `~/Projects/experiments/research-programs/schemas`.
- **Pilot first.** Before a large experiment, run a small one to confirm the
  thing you'll measure actually changes across the conditions you compare,
  and to measure what the full run will cost.
- **Record decisions.** Any method choice a reasonable scientist could make
  differently goes in `ledger/decisions.jsonl` with your reasoning. Choices
  `DIRECTION.md` reserves for Chris are recorded as `proposed` and
  asked about.
- **Record blockers** in `ledger/blockers.jsonl`; they stay open until
  resolved or carried forward, and every open one is listed in your summary.
- **Write evidence to `evidence/`**, named after the experiment id
  (`E0007-results.json`). Every number you report must appear in one of
  these files. For outputs in `~/Projects/experiments/sequel-data`, the evidence file records the
  path, size and SHA-256.
- **Use the referee for judgments.** Propose claims in
  `ledger/claims.jsonl`; the referee in `referee/` and the claim's evidence
  class in `DIRECTION.md` decide their status, not your own reading.
- **Compare against the baseline the same way.** Any change in settings,
  sampling or comparison window applies to the baseline too, or the
  comparison doesn't count.
- **Be a skeptic about your own results.** Before claiming anything, go
  through "Known ways this goes wrong" in `DIRECTION.md` and check the most
  likely one.
- **Watch the budgets.** Say in your summary when a budget passes 50% and
  80%. At 100%, stop spending and ask.

## Long jobs

Sessions are a few hours; some jobs take longer. Run them as background
processes that outlive the session:

- Start each with `caffeinate -i nice -n 10 ...` so the Mac doesn't sleep
  under it and Chris's daytime work keeps priority, with output and
  a log under the experiment's `~/Projects/experiments/sequel-data/runs/` folder.
- Checkpoint often enough that a job killed at any moment loses less than
  about 30 minutes, and make every job resumable.
- Record each job in `~/Projects/experiments/sequel-data/runs/active.jsonl` (experiment id,
  process id, command, start time, expected finish). Remove the entry when
  you collect the job.
- Stay within the core and memory limits in `budgets.yaml`, counting jobs
  started by earlier sessions.

## Run conditions

Measure, don't guess. Record in the session summary's `run_conditions`:

- `scheduled_start`, `actual_start` (the time you noted), and `ended`.
- `interruptions`: gaps where the machine slept or the session stalled
  (`pmset -g log | grep -E " (Sleep|Wake|DarkWake) "` for the session's
  window), and anything else that stopped you (a tool that hung, a
  permission prompt nobody answered).
- `cpu_hours`: CPU used by jobs this session, from their logs or
  `ps -o time`, not an estimate.
- `cores_available` (from the `uptime` load average at the start),
  `disk_free_gb` at the start and end, and `unfinished_runs` with why.
- `limits_hit`: where the machine limited the science (a smaller system,
  fewer repeats, a shorter run), in plain words, or "none".

## At the end

Leave at least 20 minutes. Write `sessions/YYYY-MM-DD.json`, dated like the
instruction it followed (schema: `~/Projects/experiments/research-programs/schemas/session-summary.schema.json`),
for a scientist who didn't watch the session:

- `answers`: write this first. One entry per item under "Asked", in order:
  `asked` is the item copied word for word; `status` is `answered`,
  `partly` or `not_answered`; `answer` replies in the item's own terms (yes,
  no, a number, or why there is no answer yet) before any explanation;
  `departures` says where what you did differs from what was asked. Empty
  on a fallback night.
- `headline`: two or three sentences on what the session was for and what
  was learned. It may not claim more than `answers` does.
- `experiments`: for each one, the question, what you did, what happened,
  and what it means, in plain language. No ids or abbreviations in the
  prose; numbers in words with their meaning.
- `claims_changed`: claims whose status changed, with why.
- `questions`: at most five, each with why it matters and what you'll do by
  default if unanswered. Only ask what the data can't settle, and only what
  Chris can answer from the summary alone, in the terms the
  instruction used. If you can't put a question that way, apply your
  default and report it.
- `proposed_directions`: two or three, ranked, each with a rationale.
- `budget`, `open_blockers`, and `run_conditions`.

Then update `PROGRAM.md` ("Current state" and "Next"), empty
`~/Projects/experiments/sequel-data/tmp/`, run `program check` again, and commit the records on
`main` (and any code on its branch) with messages describing the session.
