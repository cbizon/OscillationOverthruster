# Ledger

Append-only JSONL. Never rewrite a line; to change something, append a new
record that names the one it supersedes (`supersedes`). Schemas are in
`~/Projects/experiments/research-programs/schemas`; `program check` validates every line and fails if an
earlier line was changed.

- `experiments.jsonl`: one line per registration and one per outcome.
- `claims.jsonl`: claims and each status change.
- `decisions.jsonl`: method decisions and who made them.
- `blockers.jsonl`: blockers and how each was resolved or carried.
- `lines.jsonl`: lines of investigation: when each was opened and by whom,
  where it stands, and a note per night. `program map` builds the
  scientist's page from it.
- `terms.jsonl`: the names the records use, with definitions.
