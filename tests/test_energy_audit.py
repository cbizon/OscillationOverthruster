"""Energy and momentum accounting: the books balance to round-off for the
unmodified engine, every collision dissipates in its own frame, and energy
put in outside the accounted channels shows up as a residual."""

import numpy as np
import pytest

from granular import edmd as K
from granular.sim import Simulation


def balance(sim, run):
    """Run, then return (energy residual, energy throughput, momentum
    residual, momentum scale)."""
    e0, p0 = sim.layer_energy()
    en0 = sim.en.copy()
    t0 = sim.time_abs()
    run()
    e1, p1 = sim.layer_energy()
    d = sim.en - en0
    accounted = (d[K.EN_PLATE_WORK] + d[K.EN_PLATE_DISS] + d[K.EN_PP_DISS]
                 + d[K.EN_WALL_DISS])
    throughput = (abs(d[K.EN_PLATE_WORK]) + abs(d[K.EN_PLATE_DISS])
                  + abs(d[K.EN_PP_DISS]) + abs(d[K.EN_WALL_DISS]))
    gravity = sim.P[K.P_G] * sim.mass.sum() * (sim.time_abs() - t0)
    momentum = (p1 - p0) - (d[K.EN_PLATE_JZ] + d[K.EN_WALL_JZ] - gravity)
    return (e1 - e0) - accounted, throughput, momentum, abs(d[K.EN_PLATE_JZ]) + gravity


def run_cycles(sim, cycles):
    def run():
        for _ in range(cycles):
            sim.run_to(sim.T)
            sim.end_cycle()
            sim.rebuild(sort=True)
    return run


@pytest.mark.parametrize("dim, n, width", [(3, 600, 10.0), (2, 300, 60.0)])
def test_books_balance_for_driven_layer(dim, n, width):
    sim = Simulation(n, width, 3.0, 0.44, 5.42 if dim == 3 else n / width, 5, dim=dim)
    residual, throughput, momentum, scale = balance(sim, run_cycles(sim, 4))
    assert throughput > 0
    assert abs(residual) < 1e-9 * throughput, (residual, throughput)
    assert abs(momentum) < 1e-9 * scale, (momentum, scale)
    assert sim.cnt[K.C_EGAIN] == 0
    assert sim.en[K.EN_PP_DISS] < 0
    assert sim.en[K.EN_PLATE_DISS] < 0
    assert sim.en[K.EN_WALL_DISS] <= 0
    assert sim.en[K.EN_PLATE_WORK] > 0       # the plate drives the layer


def test_elastic_rough_collisions_dissipate_nothing():
    """eps = 1 and perfectly rough: every collision conserves energy, so
    the dissipation terms stay at round-off and nothing counts as a gain."""
    sim = Simulation(400, 8.0, 3.0, 0.44, 5.42, 7, v_init=1.0)
    sim.P[K.P_A] = 0.0
    sim.P[K.P_EPS] = 1.0
    sim.P[K.P_B] = 0.0
    sim.P[K.P_MU] = 1e9
    sim.P[K.P_BETA0] = 1.0
    sim.rebuild()
    residual, throughput, _, _ = balance(sim, lambda: sim.run_to(4.0))
    total = abs(sim.layer_energy()[0])
    assert abs(sim.en[K.EN_PP_DISS]) < 1e-9 * total
    assert sim.cnt[K.C_EGAIN] == 0
    assert abs(residual) < 1e-9 * total


@pytest.mark.parametrize("kind", ["velocity", "position"])
def test_unaccounted_injection_shows_as_residual(kind):
    """A fake contact method that bumps a particle's velocity (a floor) or
    lifts it (a snap) outside the accounted channels: the audit's residual
    equals the energy it changed, whichever the sign."""
    sim = Simulation(600, 10.0, 3.0, 0.44, 5.42, 5)
    sim.run_to(0.5 * sim.T)
    sim.rebuild(sort=False)        # synchronize, so the bump is clean

    def run():
        e_before, _ = sim.layer_energy()
        i = 17
        if kind == "velocity":
            sim.S[i, K.SVZ] += 0.3
        else:
            sim.S[i, K.SZ] += 0.05
        sim.rebuild(sort=False)
        injected = sim.layer_energy()[0] - e_before
        run.injected = injected
        sim.run_to(sim.T)

    residual, throughput, momentum, scale = balance(sim, run)
    assert abs(run.injected) > 1e-3       # either sign is unaccounted
    assert residual == pytest.approx(run.injected, rel=1e-6, abs=1e-9 * throughput)
    if kind == "velocity":
        assert momentum == pytest.approx(sim.mass[17] * 0.3, rel=1e-6)


def test_accounting_survives_checkpoint(tmp_path):
    sim = Simulation(200, 8.0, 3.0, 0.44, 5.42, 3)
    sim.run_to(sim.T)
    path = str(tmp_path / "c.npz")
    sim.save_checkpoint(path)
    resumed = Simulation(200, 8.0, 3.0, 0.44, 5.42, 3)
    resumed.load_checkpoint(path)
    np.testing.assert_array_equal(resumed.en, sim.en)
