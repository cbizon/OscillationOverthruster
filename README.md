# sequel

Event-driven hard-sphere simulation of vertically oscillated granular layers,
following Bizon et al., PRL 80, 57 (1998).

## Provenance

The engine was imported from the `claude-opus-5-5-max-r01` trial of the
granular Figure 1 benchmark campaign:

```text
/Users/bizon/Projects/experiments/granular_mean/campaign-results/
  haiku-luna-terra-sol-low-cluster-v1/trials/claude-opus-5-5-max-r01/workspace/
```

Imported files: `granular/{__init__,edmd,sim,runner,export}.py` and
`tests/test_edmd.py`. Benchmark-specific analysis, manifest, and submission
scripts were left behind.

## Setup

```bash
uv sync
uv run pytest
```

## Changes from the imported engine

- The plate separation-speed floor (an energy-injecting Zeno guard) is removed.
- The plate-root solver is the exact curvature-segmented solver from the
  `codex-gpt-6-astra-low-r01` trial, generalized to arbitrary g, static plates,
  and Gamma <= 1.
- The engine raises on plate penetration, off-surface plate contacts, pair
  overlaps deeper than 2e-8, and plate searches that cannot isolate a root.
- Tests ported from astra: plate-root edge cases, an all-pairs reference event
  loop, and checkpoint-restart equivalence.

## Known limitation: resting contact on the plate

With no regularization, the model stalls when a sphere is pressed against the
plate while the plate accelerates upward faster than g. In a Gamma = 5,
f* = 0.44 run (N = 2400, L = 20), cycle 3 reached phase 0.88 (plate
acceleration 3.4 g), and one sphere and its neighbour above it then generated
about 2e6 events per 1e-8 time units. Relative normal speeds were about
1e-11, so e(v) was effectively 1 and the pair rattled at the
floating-point resolution of time. Handling this deliberately (for example a
co-moving "stuck" state while the plate acceleration exceeds g, as in the
original C code) is the next piece of work.
