"""The referee's long-contact runner on small conditions."""

import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("long_contact", ROOT / "referee" / "long_contact.py")
long_contact = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(long_contact)

ARGS = ["--engine", str(ROOT), "--dim", "2", "--gamma", "3.5", "--fstar", "0.5",
        "--N", "200", "--L", "40"]


def test_short_run_is_clean(tmp_path):
    out = tmp_path / "run"
    long_contact.main(ARGS + ["--cycles", "6", "--outdir", str(out)])
    summary = json.loads((out / "summary.json").read_text())
    assert summary["outcome"] == "completed" and summary["cycles_completed"] == 6
    assert summary["slow_episodes"] == []
    assert summary["audit_failures"] == [] and summary["energy_gains"] == 0
    assert summary["worst_energy_residual"] < 1e-10
    audit = json.loads((out / "audit.json").read_text())
    assert [row["cycle"] for row in audit] == list(range(1, 7))
    assert all(row["plate_work"] > 0 for row in audit)
    q = np.load(out / "quantities.npz")
    assert q["time"].size == 6 * 32 + 1
    assert int(q["particle_count"]) == 200


def test_resume_matches_uninterrupted_run(tmp_path):
    whole, split = tmp_path / "whole", tmp_path / "split"
    long_contact.main(ARGS + ["--cycles", "8", "--checkpoint-every", "4",
                              "--outdir", str(whole)])
    long_contact.main(ARGS + ["--cycles", "4", "--checkpoint-every", "4",
                              "--outdir", str(split)])
    long_contact.main(ARGS + ["--cycles", "8", "--checkpoint-every", "4",
                              "--outdir", str(split), "--resume"])
    a, b = np.load(whole / "quantities.npz"), np.load(split / "quantities.npz")
    for key in a.files:
        np.testing.assert_array_equal(a[key], b[key])
    audit_a = json.loads((whole / "audit.json").read_text())
    audit_b = json.loads((split / "audit.json").read_text())
    assert audit_a == audit_b


def test_physical_failure_is_recorded_then_raised(tmp_path, monkeypatch):
    """Two spheres placed deeply overlapping: the engine raises, and the
    summary records the failure before the error propagates."""
    import granular.sim as sim_module
    original = sim_module.Simulation.__init__

    def overlapping(self, *a, **kw):
        original(self, *a, **kw)
        self.S[1, :3] = self.S[0, :3]
        self.S[1, 0] += 0.5                 # centres half a diameter apart
        self.rebuild(sort=False)

    monkeypatch.setattr(sim_module.Simulation, "__init__", overlapping)
    out = tmp_path / "bad"
    with pytest.raises(RuntimeError, match="non-physical"):
        long_contact.main(ARGS + ["--cycles", "2", "--outdir", str(out)])
    summary = json.loads((out / "summary.json").read_text())
    assert summary["outcome"] == "physical_failure"
    assert "overlap" in summary["error"]


def test_cpu_budget_stops_the_run(tmp_path):
    out = tmp_path / "budget"
    long_contact.main(ARGS + ["--cycles", "50", "--max-cpu-hours", "1e-7",
                              "--outdir", str(out)])
    summary = json.loads((out / "summary.json").read_text())
    assert summary["outcome"] == "cpu_budget"
    assert summary["cycles_completed"] < 50
