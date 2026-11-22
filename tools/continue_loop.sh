#!/bin/bash
# continue_loop.sh INPUT_LOOP_DIR RAMP_ARGS...
# Copy a loop folder from $1 to $ROBOROBO_OUT/loop, clean up any failed
# (non-completed) step at the end, then run ramp.py with the given arguments.
# For use on Hatteras via program submit.
set -e

src="$1"; shift
dst="${ROBOROBO_OUT}/loop"

# Copy the input loop to the output directory
cp -r "$src" "$dst"

# Remove any .cap0.5h leftovers
find "$dst" -name '*.cap0.5h' -exec rm -rf {} + 2>/dev/null || true

# Remove the last step if it was not completed (ramp.py would refuse to continue)
python3 - "$dst" <<'PY'
import json, shutil, sys
from pathlib import Path
out = Path(sys.argv[1])
rj = out / "ramp.jsonl"
if not rj.exists():
    sys.exit(0)
rows = [json.loads(line) for line in rj.read_text().splitlines() if line.strip()]
changed = False
while rows and rows[-1].get("outcome") != "completed":
    s = rows.pop()
    d = out / ("step-%03d-g%s" % (s["step"], s["gamma"]))
    for p in [d, Path(str(d) + ".log")]:
        if p.exists():
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
    changed = True
    print("removed failed step %d (Gamma %s, outcome %s)" % (s["step"], s["gamma"], s.get("outcome")))
if changed:
    rj.write_text("".join(json.dumps(r) + "\n" for r in rows))
PY

# Delete checkpoints from steps that aren't the last completed one,
# except those at Gamma multiples of 0.5 (ramp.py --keep-checkpoints-every 0.5).
# This saves disk on Hatteras.
python3 - "$dst" <<'PY'
import json, sys
from pathlib import Path
out = Path(sys.argv[1])
rj = out / "ramp.jsonl"
if not rj.exists():
    sys.exit(0)
rows = [json.loads(line) for line in rj.read_text().splitlines() if line.strip()]
completed = [r for r in rows if r.get("outcome") == "completed"]
if not completed:
    sys.exit(0)
last_step = completed[-1]["step"]
removed = 0
for r in completed:
    if r["step"] == last_step or r["step"] == 0:
        continue
    g = r["gamma"]
    q = g / 0.5
    if abs(q - round(q)) < 1e-6:
        continue
    ck = out / ("step-%03d-g%s" % (r["step"], g)) / "checkpoint.npz"
    if ck.exists():
        ck.unlink()
        removed += 1
if removed:
    print("pruned %d checkpoints" % removed)
PY

# Run ramp.py with the remaining arguments
exec uv run python tools/ramp.py "$@" "$dst"
