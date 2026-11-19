# Scheduled runs

<!-- Rendered from RoboRobo's template by `program sync`; don't edit here. -->

sequel runs one line of investigation at a time. At 23:00
(America/New_York) `program run-night` reads the night's instruction and, for
each line it has a section for (and each line with open challenges from
the checker), runs the agent on that line, then the checker on that run.
It starts no new line after 05:00.

| What | When | Prompt |
| --- | --- | --- |
| Night runner | 23:00, launchd job | `run-night.plist` |
| One line's run | started by the runner, up to about an hour each | `line.md` |
| Checker, after each line | started by the runner, up to 45 minutes | `line-checker.md` |
| Debrief | 07:00, Code tab scheduled task | `debrief.md` |

## Installing the night runner

Once, on the Mac that runs the program:

```bash
cp ~/Projects/experiments/sequel/scheduled/run-night.plist ~/Library/LaunchAgents/org.renci.roborobo.sequel.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/org.renci.roborobo.sequel.plist
```

After `program sync` changes the plist, copy it again and run
`launchctl bootout gui/$(id -u)/org.renci.roborobo.sequel` before the
bootstrap. The Mac must be awake at 23:00 (a wake schedule in
System Settings, or `pmset repeat`); once started, the runner keeps it
awake.

To see what tonight would run: `program run-night --dry-run`. To run one
line now: `program run-night --line L0013`.

## Where to look

- `~/Projects/experiments/sequel-data/logs/YYYY-MM-DD/night.md`: what ran, for how long, and
  what went wrong. The debrief reads it.
- `~/Projects/experiments/sequel-data/logs/YYYY-MM-DD/L0013-worker.log` and `-checker.log`: each
  run's output.
- `~/Projects/experiments/sequel-data/logs/run-night.log`: the runner's own output, every night,
  including errors that stopped it from starting.

The worker and checker run as `claude -p` unless `program.toml` sets
`[runs] agent`. A run that fails, times out or leaves no summary is
reported, not retried. A run that leaves uncommitted changes or a failing
`program check` stops the night.
