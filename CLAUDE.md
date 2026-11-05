# How to work in this program

You are running one session of a long research program on this simulation
engine. Nobody is watching the session; Chris reads your summary in the
morning and replies with the next instruction. Your memory between sessions
is this repository. Write everything you'd want to know tomorrow into it.

The program runs locally on Chris's Mac. Whether that works well enough is
itself under test (RQ0 in `PROGRAM.md`), so you record how each session ran
(see "Run conditions" below).

## At the start

1. Note the time you started; you need it for the run conditions.
2. Read `DIRECTION.md` (the question, bounds, claim rules, autonomy,
   budgets) and `budgets.yaml`. You never edit them, `referee/`, or
   `approvals.json`.
3. Read `PROGRAM.md`, then the instruction for today in `instructions/`
   (`YYYY-MM-DD.md`, dated by the evening the session starts). If there is
   none, follow `instructions/fallback.md`.
4. Read the last session summary in `sessions/`, the checker's latest review
   in `reviews/`, and any open records in `ledger/blockers.jsonl` and
   `ledger/claims.jsonl`. Answer every open challenge this session: produce
   the evidence that resolves it, narrow the claim, or withdraw it.
5. Check on simulations left running by earlier sessions (see "Long
   simulations"). Collect finished ones before starting new work.
6. Run the frozen tests: `uv run pytest referee/tests`. If they fail on the
   program branch, fixing that comes before anything else.

## Where work goes

- The program's records (this file's siblings: `PROGRAM.md`, `ledger/`,
  `sessions/`, `evidence/`) live on the `program` branch. Commit them there.
- Each contact-handling method is developed on its own branch,
  `method/<short-name>`, in a worktree under
  `~/Projects/experiments/sequel-data/worktrees/`. Never merge a method into
  `program` or `main`; that needs Chris.
- Large outputs (trajectories, movies, checkpoints) go under
  `~/Projects/experiments/sequel-data/runs/<experiment-id>/`, never in git.
  The disk is nearly full: check free space before any run that writes more
  than a gigabyte, keep only what a claim needs, and record the size of what
  you keep in the evidence file.

## While working

- **Pre-register.** Before running an experiment, append to
  `ledger/experiments.jsonl` with status `registered`: the hypothesis, the
  method, how the result will be judged, what would falsify it, and the
  estimated cost in CPU-hours and disk. Don't edit a registration once
  results exist; supersede it with a new record.
- **Pilot first.** Before a long run, run a short one to confirm that what
  you'll measure actually changes across the conditions you're comparing,
  and to measure events per second so the cost estimate is real.
- **Record decisions.** Any method choice a reasonable physicist could make
  differently (a tolerance, a release condition, how long to equilibrate,
  how to define an oscillon) goes in `ledger/decisions.jsonl` with your
  reasoning. Choices `DIRECTION.md` reserves for Chris are recorded as
  `proposed` and asked about.
- **Record blockers** in `ledger/blockers.jsonl`; they stay open until
  resolved or carried forward.
- **Write evidence to `evidence/`**, named after the experiment id
  (`E0007-energy-audit.json`). Every number you report later must appear in
  one of these files exactly. For outputs in `sequel-data`, the evidence
  file records the path, size and SHA-256.
- **Use the referee for judgments.** The referee is in `referee/`: the
  frozen tests, the Figure 1 comparison and the long-contact test, each with
  its own instructions there. Propose claims in `ledger/claims.jsonl`; the
  referee's results and the claim's evidence class in `DIRECTION.md` decide
  their status, not your own reading of the output.
- **Compare against the baseline the same way.** Any change in tolerance,
  time step, sampling or comparison window is applied to the baseline
  engine too, or the comparison doesn't count.
- **Be a skeptic about your own results.** Before claiming anything, go
  through "Known ways this goes wrong" in `DIRECTION.md` and check the most
  likely one.
- **Watch the budgets.** Note in your summary when a budget passes 50% and
  80%. At 100%, stop spending and ask.

## Long simulations

Sessions are a few hours; some simulations will take longer. Run them as
background processes that outlive the session:

- Start each with `caffeinate -i nice -n 10 uv run ...` so the Mac doesn't
  sleep under it and Chris's daytime work keeps priority, with output and a
  log under the experiment's `sequel-data/runs/` folder.
- Write checkpoints often enough that a run killed at any moment loses less
  than about 30 minutes of work, and make every run resumable from its
  latest checkpoint.
- Record each background run in `sequel-data/runs/active.jsonl` (experiment
  id, process id, command, start time, expected finish). Remove the entry
  when you collect the run.
- Don't run more than the core limit in `budgets.yaml` at once, counting
  runs started by earlier sessions.

## Run conditions

Measure, don't guess. Record in the session summary's `run_conditions`:

- `scheduled_start` and `actual_start` (the time you noted at the start), and
  `ended` (when you finish writing the summary).
- `interruptions`: gaps where the machine slept or the session stalled. Check
  with `pmset -g log | grep -E " (Sleep|Wake|DarkWake) "` for the session's
  time window, and note anything else that stopped you (a tool that hung, a
  permission prompt nobody answered).
- `cpu_hours`: CPU time used by simulations this session, from the runs' own
  logs or `ps -o time` on the processes, not an estimate.
- `cores_available`: the cores you could actually use, given other load
  (`uptime` load average at the start).
- `unfinished_runs`: runs still going or waiting at the end, and why (needs
  more time, waiting for cores, waiting for disk).
- `disk_free_gb` at the start and end.
- `limits_hit`: places where running locally limited the science (a
  smaller system than you wanted, fewer random seeds, a shorter run), in
  plain words. Say "none" if there were none.

## At the end

Leave at least 20 minutes to write `sessions/YYYY-MM-DD.json`, dated like the
instruction it followed. Schema:
`~/Projects/experiments/research-programs/schemas/session-summary.schema.json`.
Write it for a physicist who didn't watch the session:

- `headline`: two or three sentences on what the session was for and what
  was learned.
- `experiments`: for each one, the question, what you did, what happened,
  and what it means, in plain language. No experiment ids or abbreviations
  in the prose; numbers in words with their meaning ("the layer gained about
  three percent of its energy per cycle, which a correct method can't do").
- `claims_changed`: claims whose status changed, with why.
- `questions`: at most five, each with why it matters and what you'll do by
  default if unanswered. Only ask what the data can't settle.
- `proposed_directions`: two or three, ranked, each with a rationale.
- `budget`: what was spent and what remains.
- `run_conditions`: as above.

Then update `PROGRAM.md` ("Current state" and "Next"), and commit the program
records on the `program` branch, and any method code on its own branch, with
messages describing the session.
