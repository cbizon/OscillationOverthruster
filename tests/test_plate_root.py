"""Plate-root solver checks ported from the codex-gpt-6-astra-low trial, plus
the drive regimes the generalized solver must also handle (static plate and
plate acceleration below g)."""

import math

import numpy as np
import pytest

from granular import edmd as K
from granular.sim import Simulation


def gap(tau, z, vz, r, t, A, om, g=1.0):
    return z + vz * tau - 0.5 * g * tau * tau - r - A * math.sin(om * (t + tau))


def reference_root(z, vz, r, t, horizon, A, om, g=1.0, n=10001):
    """First sign change of the gap on a fine grid, refined by bisection."""
    grid = np.linspace(0.0, horizon, n)
    h = z + vz * grid - 0.5 * g * grid ** 2 - r - A * np.sin(om * (t + grid))
    below = np.flatnonzero(h < 0.0)
    if len(below) == 0:
        return math.inf
    k = below[0]
    lo, hi = grid[k - 1], grid[k]
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if gap(mid, z, vz, r, t, A, om, g) > 0.0:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-14:
            break
    return 0.5 * (lo + hi)


def test_plate_roots_match_reference():
    rng = np.random.default_rng(17)
    A, om = 3.0, 1.0
    for _ in range(200):
        t = rng.uniform(0, 30)
        z = A * math.sin(t) + 0.5 + rng.uniform(0.001, 8)
        vz = rng.uniform(-5, 8)
        predicted = K.plate_root(z, vz, 0.5, t, 12.0, A, om, 1.0)
        expected = reference_root(z, vz, 0.5, t, 12.0, A, om)
        if math.isinf(expected):
            assert math.isinf(predicted)
        else:
            assert predicted == pytest.approx(expected, abs=2e-11)


def test_static_plate_root_is_free_fall():
    for z, vz in [(3.0, 0.0), (0.6, -2.0), (2.0, 4.0)]:
        expected = vz + math.sqrt(vz * vz + 2.0 * (z - 0.5))
        assert K.plate_root(z, vz, 0.5, 1.3, 50.0, 0.0, 1.0, 1.0) == pytest.approx(
            expected, abs=1e-12)


def test_plate_roots_when_plate_never_outaccelerates_gravity():
    rng = np.random.default_rng(5)
    A, om = 0.5, 1.2                      # Gamma = A om^2 / g = 0.72
    for _ in range(100):
        t = rng.uniform(0, 20)
        z = A * math.sin(om * t) + 0.5 + rng.uniform(0.001, 3)
        vz = rng.uniform(-3, 3)
        predicted = K.plate_root(z, vz, 0.5, t, 10.0, A, om, 1.0)
        expected = reference_root(z, vz, 0.5, t, 10.0, A, om)
        if math.isinf(expected):
            assert math.isinf(predicted)
        else:
            assert predicted == pytest.approx(expected, abs=2e-11)


def test_penetrating_sphere_raises():
    with pytest.raises(ValueError):
        K.plate_root(0.5 - 1e-6, 0.0, 0.5, 0.0, 5.0, 1.0, 1.0, 1.0)


def single_sphere(z, vz, t, A, om):
    """A one-particle simulation with the drive replaced by A sin(om t)."""
    sim = Simulation(1, 10.0, 3.0, 0.44, 5.42, 1)
    sim.A = A
    sim.om = om
    sim.P[K.P_A] = A
    sim.P[K.P_OM] = om
    sim.S[0, K.SX] = 5.0
    sim.S[0, K.SY] = 5.0
    sim.S[0, K.SZ] = z
    sim.S[0, K.SVX:K.SVZ] = 0.0
    sim.S[0, K.SVZ] = vz
    sim.S[0, K.ST] = t
    sim.S[0, K.SR] = 0.5
    sim.W[:] = 0.0
    sim.t_local = t
    sim.rebuild(sort=False)
    return sim


def test_plate_contact_near_zero_coordinate():
    """The sphere starts touching the plate where the plate surface sits at
    z = 0.5 (centre at z = 0) and approaches it at 1e-8: the collision must
    be found despite the near-zero coordinates."""
    A, om = 3.0, 1.0
    t = 200 * math.pi - math.asin(1 / 6)
    phase = t % (2 * math.pi)
    sim = single_sphere(0.5 + A * math.sin(phase), A * math.cos(phase) - 1e-8,
                        t, A, om)
    sim.run_to(t + 1e-6)
    assert sim.cnt[K.C_PLATE] > 0
