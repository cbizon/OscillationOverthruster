# How to work in this program

<!-- Rendered from RoboRobo's template by `program sync`; don't edit here.
     This program's own instructions are in BRIEF.md. -->

You are running one session of sequel, a long research program:
long-lasting contacts in event-driven simulation of vibrated granular layers, and the hysteresis and oscillon experiments they make possible. Each night runs one line of investigation at a time, and a
session is one line's run: `scheduled/line.md` says what that changes, and
"the session" below means your run. Nobody is watching;
Chris reads your summary in the morning and replies with the next
instruction. Your memory between sessions is this repository. Write
everything you'd want to know tomorrow into it.

Who owns what:

- **Chris's files**, which you never change: `DIRECTION.md`,
  `BRIEF.md`, `budgets.yaml`, `program.toml`, `referee/`, `notes/`, and
  `approvals.json`.
- **RoboRobo's files**, which you never change: this file, `CHECKER.md`,
  `scheduled/`, `.claude/`, and the folder READMEs.
- **Yours**: `PROGRAM.md`, `ledger/`, `sessions/`, `evidence/`, `lines/`
  (except its README), and your code on branches.

`program check` fails if any of the first two changed.

## At the start

1. Note the time you started; you need it for the run conditions.
2. Read `DIRECTION.md` (the question, bounds, claim rules, autonomy), then
   `BRIEF.md` (how this program works day to day) and `budgets.yaml`. Read
   the notes in `notes/` that `BRIEF.md` points to before planning: they
   hold Chris's thinking from before the program, and you follow
   them unless an instruction says otherwise.
3. Read `PROGRAM.md`, your line's `lines/L0013/progress.md`, then your
   line's section of the instruction for tonight in `instructions/`
   (`YYYY-MM-DD.md`, dated by the evening the night starts). Its "Asked"
   items are what Chris wants to know, in Chris's words;
   see "What was asked".
4. Read your line's last summary in `sessions/` (`*-L0013.json`; before
   lines ran separately, the last `YYYY-MM-DD.json`), the checker's latest
   review of your line in `reviews/`, and any open records in
   `ledger/blockers.jsonl` and `ledger/claims.jsonl`. Answer every open
   challenge on your line this session: produce the evidence that resolves
   it, narrow the claim, or withdraw it.
5. Check on jobs left running by earlier sessions (see "Long jobs"). Collect
   finished ones before starting new work.
6. Run `uv run --project ~/Projects/experiments/research-programs program check`. If it fails, fixing
   what it reports comes first; if you can't fix it, record a blocker, write
   the summary, and stop.
7. Do any start-of-session checks `BRIEF.md` lists.

## What was asked

The session exists to answer the items under "Asked" in your line's section
of the instruction, as they are worded. "Details" says how; where the two seem to disagree, "Asked"
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

## Lines of investigation

The program's work is organised into lines: one thread each (a method, a
comparison, a baseline, a question). `ledger/lines.jsonl` records them, and
`program map` builds the page Chris reads from it, so what you write
there is what Chris sees. Schema: `~/Projects/experiments/research-programs/schemas/line.schema.json`.

- Every experiment belongs to one line. Its registration carries `line_id`
  and a `title` of a few plain words. If an experiment would serve two
  lines, split it into two.
- Open a line (`record: "open"`, id from `program next-id L`) before the
  first experiment in it: its `name`, the `question` in Chris's
  words where Chris asked it (`question_source` says where), and
  the `parent` it branched from. A line you open yourself also needs a
  `reason`, and starts with `status: "proposed"`: it runs only once
  Chris makes it active. Don't open one to hold work nobody asked
  for while an item under "Asked" is unanswered.
- At the end of the session, append for your line a `note`:
  the `night` (the session's date) and two or three plain sentences on what
  happened, with `waiting: true` if the line can't move without
  Chris. Append an `update` when its `state`, `feeds` or
  `artifacts` changed. `state` is where the line stands now, for someone
  who reads nothing else; it holds to the same standard as a claim.
- You may close a line you opened. Pausing, dropping or closing a line
  Chris opened is Chris's call: propose it in `questions`.
- When a note or summary needs a name for a method, a condition or a
  check, add it to `ledger/terms.jsonl` once (id from `program next-id T`),
  with the `aliases` it goes by, and use that name from then on.

## Where work goes, and keeping the machine clean

- Records (`PROGRAM.md`, `ledger/`, `sessions/`, `evidence/`) are committed
  on `main`. Code you try out goes on branches as `BRIEF.md` says; merging
  into `main` needs Chris.
- Everything in `~/Projects/experiments/sequel-data` is one of four kinds, and `program check`
  fails on anything else:
  - **Data**, what runs produce, in `~/Projects/experiments/sequel-data/runs/<experiment-id>/`
    here or in a job's run folder on a cluster, never in git. Every data
    folder is an artifact in `ledger/artifacts.jsonl`, with a manifest of
    its files. Record a folder here with `program record <folder>` when you
    create it and again when it is finished; `program jobs` records cluster
    outputs itself. Delete data only with `program delete <id> --reason
    ...`, never `rm`; cited data can't be deleted. Cite artifacts by id
    (A0123) in evidence and outcomes.
  - **Scratch** in `~/Projects/experiments/sequel-data/tmp/`, never recorded; empty it before
    the session ends. Data fetched to look at goes in `tmp/fetch/` and is
    removed after every run.
  - **Code**: git repositories, such as method worktrees and clones of
    other code.
  - **Operational state**: `jobs/`, `logs/`, `map/`, `mirror/`, and files
    directly in `runs/` such as `active.jsonl`.
- Stay inside `~/Projects/experiments/sequel` and `~/Projects/experiments/sequel-data`. Write nothing anywhere else.
- Before starting jobs and at the end of the session, check free disk
  (`df -h ~`), the size of `~/Projects/experiments/sequel-data` (`du -sh`), and memory
  (`memory_pressure`), and stay within the limits in `budgets.yaml`. Each
  limit says where it applies (`where`: `local` is this computer, other names
  are hosts in `program.toml`) and whether it is a ceiling (`max`) or a
  floor (`min`); a limit doesn't apply anywhere it doesn't name. Delete
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

A line's run is about an hour; many jobs take longer. Run them as
background processes that outlive the run, and record them in your line's
`progress.md` too:

- Start each with `caffeinate -i nice -n 10 ...` so the Mac doesn't sleep
  under it and Chris's daytime work keeps priority, with output and
  a log under the experiment's `~/Projects/experiments/sequel-data/runs/` folder. Run `program
  record` on that folder when you start the job, and again when you collect
  it.
- Checkpoint often enough that a job killed at any moment loses less than
  about 30 minutes, and make every job resumable.
- Record each job in `~/Projects/experiments/sequel-data/runs/active.jsonl` (experiment id,
  process id, command, start time, expected finish). Remove the entry when
  you collect the job.
- Stay within the `budgets.yaml` limits `where: [local]` (cores,
  memory, disk), counting jobs started by earlier sessions.

### On a cluster

If `program.toml` lists `[hosts]`, jobs can run there instead. Use only
those hosts; asking for another is a decision for Chris.

- Give the experiment's registration a `host` field (`local` or a host in
  `program.toml`) and say why in the method ("hatteras, because 40 seeds ×
  6 h"). `program submit` refuses a job for another host.
- Commit the code, then submit with `program submit --host hatteras
  --experiment E0131 [--time 6:00:00 --mem 16G --cpus 4] -- uv run python
  sim.py`. The job runs that commit from the repository's top folder and
  writes outputs to `$ROBOROBO_OUT`. Arguments are passed as given, so to
  use `$ROBOROBO_OUT` or `$ROBOROBO_IN` in them, or chain commands, wrap
  the command in `bash -c '...'`. Never call `ssh`, `rsync`, `sbatch` or
  `scancel` yourself.
- Code from another branch: `--tree engine=method/nudge` checks it out at
  `../engine`, a real git checkout. Another repository: clone it into
  `~/Projects/experiments/sequel-data` and use `--tree name=<its path>:<revision>`; it lands at
  `../name`, and the job can `cd` there and `uv run` in its own project.
  Sibling repositories named as uv path sources in `pyproject.toml` go along
  by themselves, at their committed state.
- Inputs a job starts from (a checkpoint to continue) are artifacts:
  `--input A0123[:path/in/it]`, or a path inside a recorded folder here;
  repeatable. The job finds a copy in `$ROBOROBO_IN`, so it can't change the
  original. An input on the same cluster is copied there, not through this
  computer.
- Don't wait for the job; record its id in your line's `progress.md` and
  end the run.
- Outputs stay on the cluster. Run `program jobs` at the start of each run:
  it copies only small files (the host's `fetch` patterns, such as
  `*.json`) and the Slurm log into
  `~/Projects/experiments/sequel-data/mirror/<experiment>/<host>-<job>/`, running jobs included,
  so you can follow progress. A job that ended becomes an artifact (its id
  is printed), and gets a job record,
  `evidence/<experiment>/<host>-<job>.json` (commits, command, resources,
  state, `cpu_hours` for the outcome's `cost_actual`). Commit the ledger and
  the record. A failed or vanished job is a problem to record, not to retry
  silently.
- To look at anything else, `program fetch A0123[:path]` copies it into
  `~/Projects/experiments/sequel-data/tmp/fetch/`; it is gone after the run. Look at whatever you
  need. For an analysis over a lot of data (every step of a loop), it's
  quicker to run it as a job next to the data, with the artifact as its
  input, and look at the small result.

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

Leave at least ten minutes. Write `sessions/YYYY-MM-DD-L0013.json`, dated
like the instruction it followed, with `line_id` set (schema:
`~/Projects/experiments/research-programs/schemas/session-summary.schema.json`), for a scientist who didn't watch
the session:

- `answers`: write this first. One entry per item under "Asked", in order:
  `asked` is the item copied word for word; `status` is `answered`,
  `partly` or `not_answered`; `answer` replies in the item's own terms (yes,
  no, a number, or why there is no answer yet) before any explanation;
  `departures` says where what you did differs from what was asked. Empty
  when you were started only to answer challenges.
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

Then append this session's notes and updates to `ledger/lines.jsonl`,
rewrite `lines/L0013/progress.md`, update what concerns your line in
`PROGRAM.md` ("Current state" and "Next"), empty
`~/Projects/experiments/sequel-data/tmp/`, run `program check` again and
`uv run --project ~/Projects/experiments/research-programs program map` to see that the page builds,
and commit the records on `main` (and any code on its branch) with
messages describing the session. Leave nothing uncommitted.
