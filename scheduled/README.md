# Scheduled tasks

<!-- Rendered from RoboRobo's template by `program sync`; don't edit here. -->

Prompts for the Claude Code (Code tab) scheduled tasks that run sequel on
Chris's Mac. Create each task in the Code tab with "run only on this
computer", `~/Projects/experiments/sequel` as its folder, and the prompt file's contents.

| Task | When (America/New_York) | Prompt |
| --- | --- | --- |
| Session | 23:00 until 05:00 | `session.md` |
| Checker | 05:30, about 45 minutes | `checker.md` |
| Debrief | 07:00 | `debrief.md` |

The Mac has to be awake with the Claude app open. Long jobs run under
`caffeinate`, so they keep it awake once started; the start of each task is
the fragile part, and each session records how it actually ran.
