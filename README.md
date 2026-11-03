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
