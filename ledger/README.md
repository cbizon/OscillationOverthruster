# Ledger

Append-only JSONL. Never rewrite a line; to change something, append a new
record that names the one it supersedes (`supersedes`). Schemas are in
`../../schemas/` (or the shared schemas directory this program points to).

- `experiments.jsonl`: one line per registration and one per outcome.
- `claims.jsonl`: claims and each status change.
- `decisions.jsonl`: method decisions and who made them.
- `blockers.jsonl`: blockers and how each was resolved or carried.
