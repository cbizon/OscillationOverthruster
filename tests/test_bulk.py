"""The referee's bulk-quantity tool on synthetic trajectories with known answers."""

import importlib.util
from pathlib import Path

import numpy as np
import pytest

_spec = importlib.util.spec_from_file_location(
    "bulk", Path(__file__).resolve().parents[1] / "referee" / "bulk.py")
bulk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bulk)

T = 3.7     # drive period, arbitrary


def synthetic(path, cycles=30, n=50, drift=0.0, alternate=0.0, duplicate_last=False):
    """Particles stacked in a column; centre-of-mass height above the plate
    is 3 + sin(2 pi phase) + alternate * (-1)^cycle + drift * cycle."""
    frames = cycles * bulk.PHASES + 1
    k = np.arange(frames)
    time = k * T / bulk.PHASES
    phase = (k % bulk.PHASES) / bulk.PHASES
    cycle = k // bulk.PHASES
    plate = 0.5 * np.sin(2 * np.pi * phase)
    zcm = (3.0 + np.sin(2 * np.pi * phase) + alternate * (-1.0) ** cycle
           + drift * cycle)
    offsets = np.linspace(-2.0, 2.0, n)
    pos = np.zeros((frames, n, 3))
    pos[:, :, 2] = (plate + zcm)[:, None] + offsets[None, :]
    pos[:, :, 0] = np.linspace(1, 9, n)
    vel = np.zeros((frames, n, 3))
    vel[:, :, 2] = 2.0                  # whole layer moving up at 2
    vel[:, :, 0] = np.where(np.arange(n) % 2, 1.0, -1.0)   # +-1 horizontally
    diam = np.ones(n)
    arrays = dict(time=time, drive_phase=phase, positions=pos, velocities=vel,
                  angular_velocities=np.zeros_like(pos), diameters=diam,
                  plate_z=plate, plate_vz=np.zeros(frames))
    if duplicate_last:
        arrays = {key: (np.concatenate([v, v[-1:]]) if key not in ("diameters",) else v)
                  for key, v in arrays.items()}
    np.savez(path, **arrays)
    return path


def test_drive_period_is_inferred(tmp_path):
    data = np.load(synthetic(tmp_path / "t.npz"))
    assert bulk.drive_period(data["time"], data["drive_phase"]) == pytest.approx(T)


def test_known_quantities(tmp_path):
    result = bulk.measure(synthetic(tmp_path / "t.npz"), 20, 10, 2)
    q = result["quantities"]
    assert q["zcm"]["mean"] == pytest.approx(3.0, abs=1e-9)
    profile = np.array(q["zcm"]["profile"])
    expected = 3.0 + np.sin(2 * np.pi * np.arange(64) / 32)
    np.testing.assert_allclose(profile, expected, atol=1e-9)
    assert q["thickness"]["mean"] == pytest.approx(np.linspace(-2, 2, 50).std())
    assert q["ke_vertical"]["mean"] == pytest.approx(2.0)          # m v^2 / 2
    assert q["ke_horizontal"]["mean"] == pytest.approx(0.5)
    assert q["temp_vertical"]["mean"] == pytest.approx(0.0, abs=1e-12)  # moves as a block
    assert q["temp_horizontal"]["mean"] == pytest.approx(0.5)
    assert not any(v["drifting"] for v in q.values())


def test_drift_is_flagged(tmp_path):
    result = bulk.measure(synthetic(tmp_path / "t.npz", drift=0.05), 20, 10, 2)
    zcm = result["quantities"]["zcm"]
    assert zcm["drifting"]
    assert zcm["trend"] == pytest.approx(0.05 * 8, rel=1e-6)   # 5 periods, 8 cycles apart


def test_window_must_be_covered(tmp_path):
    with pytest.raises(ValueError, match="doesn't cover"):
        bulk.measure(synthetic(tmp_path / "t.npz", cycles=25), 20, 10, 2)


def test_duplicate_final_frame_is_ignored(tmp_path):
    a = bulk.measure(synthetic(tmp_path / "a.npz"), 20, 10, 2)
    b = bulk.measure(synthetic(tmp_path / "b.npz", duplicate_last=True), 20, 10, 2)
    assert a["quantities"] == b["quantities"]


def test_compare_aligns_period_two_response(tmp_path):
    """Two runs that alternate in opposite cycles agree after a one-cycle shift."""
    a = bulk.measure(synthetic(tmp_path / "a.npz", alternate=0.3), 20, 10, 2)
    b = bulk.measure(synthetic(tmp_path / "b.npz", cycles=32, alternate=0.3), 21, 10, 2)
    rows = bulk.compare(a, b)
    assert rows["zcm"]["cycle_shift"] == 1
    assert rows["zcm"]["max_profile_difference"] == pytest.approx(0.0, abs=1e-9)


def test_plate_contact_phases():
    profile = np.zeros(64)
    profile[10:20] = 0.5
    profile[40:50] = 0.5
    phases = bulk.crossings(profile, 0.01)
    assert phases["landing"] == [10 / 32, 40 / 32]
    assert phases["takeoff"] == [20 / 32, 50 / 32]


def test_baseline_and_judge(tmp_path):
    """Block means of a noisy baseline give the scatter; a method inside the
    threshold passes and one shifted well outside fails."""
    rng = np.random.default_rng(0)
    path = synthetic(tmp_path / "base.npz", cycles=60)
    data = dict(np.load(path))
    frames = data["time"].size
    # per-cycle noise in height, so block means scatter
    noise = np.repeat(rng.normal(0, 0.2, frames // bulk.PHASES + 1), bulk.PHASES)[:frames]
    data["positions"][:, :, 2] += noise[:, None]
    np.savez(path, **data)
    base = bulk.baseline(path, 20, 10, 4, 2)
    assert base["threshold"] == bulk.rule.threshold(4, len(bulk.QUANTITIES))
    sd = base["quantities"]["zcm"]["sd"]
    assert sd > 0
    inside = bulk.measure(synthetic(tmp_path / "in.npz"), 20, 10, 2)
    rows = bulk.judge(base, inside)
    limit = base["threshold"] * sd
    assert rows["zcm"]["passes"] == (abs(3.0 - base["quantities"]["zcm"]["mean"]) <= limit)
    shifted = synthetic(tmp_path / "out.npz")
    data = dict(np.load(shifted))
    data["positions"][:, :, 2] += 2 * limit + 1.0
    np.savez(shifted, **data)
    assert not bulk.judge(base, bulk.measure(shifted, 20, 10, 2))["zcm"]["passes"]


def test_judge_refuses_mismatched_lengths(tmp_path):
    base = bulk.baseline(synthetic(tmp_path / "b.npz", cycles=60), 20, 10, 4, 2)
    method = bulk.measure(synthetic(tmp_path / "m.npz"), 20, 6, 2)
    with pytest.raises(ValueError, match="same length"):
        bulk.judge(base, method)


def test_baseline_needs_enough_blocks(tmp_path):
    with pytest.raises(ValueError, match="at least 3 baseline blocks"):
        bulk.baseline(synthetic(tmp_path / "b.npz", cycles=60), 20, 10, 2, 2)


def test_thresholds_give_five_percent_false_fails():
    """A method drawn from the same distribution as the baseline blocks fails
    some quantity about 5% of the time (checked for 10 blocks)."""
    rng = np.random.default_rng(7)
    trials, n = 40000, 10
    b = rng.normal(size=(trials, len(bulk.QUANTITIES), n))
    m = rng.normal(size=(trials, len(bulk.QUANTITIES)))
    z = np.abs(m - b.mean(2)) / b.std(2, ddof=1)
    rate = (z > bulk.rule.threshold(n, len(bulk.QUANTITIES))).any(1).mean()
    assert 0.04 < rate < 0.06
