#!/bin/bash
# settle_loop.sh RAMP_ARGS...
# Run settle_ramp.py on Hatteras (or locally) with the given arguments.
# Output goes to $ROBOROBO_OUT/loop (or the named outdir if no ROBOROBO_OUT).
set -e

outdir="${ROBOROBO_OUT:-/tmp}/loop"
exec uv run python tools/settle_ramp.py "$@" "$outdir"
