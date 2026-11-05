"""2D mode: spheres confined to a plane (the 1998 C code's 2D model)."""

import numpy as np
import pytest

from granular import edmd as K
from granular.sim import KINERTIA, Simulation
from test_reference import all_pairs_reference


def planar(n, L, seed, **kw):
    return Simulation(n, L, 3.0, 0.44, n / L, seed, dim=2, **kw)


def spin_about_y(sim, seed):
    sim.W[:, 1] = np.random.default_rng(seed).normal(size=sim.N)


def assert_planar(sim):
    r, v, w = sim.snapshot()
    np.testing.assert_array_equal(r[:, 1], 0.5 * sim.hx)
    np.testing.assert_array_equal(v[:, 1], 0.0)
    np.testing.assert_array_equal(w[:, [0, 2]], 0.0)


def planar_energy(sim):
    r, v, w = sim.snapshot()
    inertia = 0.25 * KINERTIA * sim.mass * sim.diam ** 2
    return (0.5 * np.sum(sim.mass[:, None] * v ** 2) + np.sum(sim.mass * r[:, 2])
            + 0.5 * np.sum(inertia * w[:, 1] ** 2))


def test_planar_setup():
    sim = planar(300, 30.0, 4)
    assert sim.ny == 1 and sim.IP[K.I_NY] == 1
    assert sim.P[K.P_K] == KINERTIA
    np.testing.assert_array_equal(sim.mass, sim.diam ** 3)
    assert_planar(sim)


def test_driven_spheres_stay_in_plane():
    """Several cycles of driven, dissipative, frictional spheres: every
    position, velocity and spin stays exactly in the plane.  (With
    v_init = 1 this layer hits the resting-contact stall in cycle 0, so
    the test uses the default start.)"""
    sim = planar(400, 40.0, 3)
    spin_about_y(sim, 3)
    sim.rebuild()
    for _ in range(3):
        sim.run_to(sim.T)
        sim.end_cycle()
        sim.rebuild(sort=True)
    assert sim.cnt[K.C_PP] > 10000 and sim.cnt[K.C_PLATE] > 100
    assert sim.cnt[K.C_WALL] > 0
    assert_planar(sim)
    g, i, j, bad = sim.overlap_check()
    assert g > -1e-9 and bad == 0


def test_equal_planar_formulas_walton():
    """Equal spheres colliding in the plane: Walton's operator (K = 2/5)
    gives in-plane impulses and spin changes about y only."""
    rng = np.random.default_rng(17)
    P = np.zeros(K.NP_FLOAT)
    P[K.P_EPS], P[K.P_ALPHA], P[K.P_V0] = 0.7, 0.75, 1.0
    P[K.P_B] = 0.3
    P[K.P_MU], P[K.P_BETA0], P[K.P_K], P[K.P_G] = 0.5, 0.35, KINERTIA, 1.0
    cnt = np.zeros(K.NCOUNT, dtype=np.int64)
    for _ in range(10):
        angle = rng.uniform(0, 2 * np.pi)
        n = np.array([np.cos(angle), 0.0, np.sin(angle)])
        r = np.array([[0.0, 0.5, 0.0], [0.0, 0.5, 0.0]])
        r[1] += n
        v = np.zeros((2, 3))
        v[:, [0, 2]] = rng.normal(size=(2, 2))
        if np.dot(v[1] - v[0], n) > 0:
            v[1] -= 2 * np.dot(v[1] - v[0], n) * n
        w = np.zeros((2, 3))
        w[:, 1] = rng.normal(size=2) * 2
        vab = v[1] - v[0]
        vn = np.dot(vab, n)
        vs = vab - vn * n + 0.5 * np.cross(n, w[0]) + 0.5 * np.cross(n, w[1])
        e = K.restitution(-vn, 0.7, 0.75, 1.0, 0.3)
        Kk = KINERTIA
        b1 = min(0.5 * (1 + e) * (1 + 1 / Kk) * abs(vn) / np.linalg.norm(vs), 1.35)
        dva = 0.5 * (1 + e) * vn * n + Kk * b1 / (2 * (Kk + 1)) * vs
        dwa = b1 / (Kk + 1) * np.cross(n, vs)
        S = np.zeros((3, 8))
        S[:2, 0:3], S[:2, 3:6], S[:2, 7] = r, v, 0.5
        w1 = w.copy()
        K.collide_pp(0, 1, S, w1, np.ones(2), P, cnt)
        np.testing.assert_allclose(S[0, 3:6] - v[0], dva, atol=1e-12)
        np.testing.assert_allclose(S[1, 3:6] - v[1], -dva, atol=1e-12)
        np.testing.assert_allclose(w1 - w, [dwa, dwa], atol=1e-12)
        assert S[0, 4] == 0.0 and S[1, 4] == 0.0
        assert np.all(w1[:, [0, 2]] == 0.0)


def test_planar_energy_conservation_elastic_static_plate():
    """Elastic, perfectly rough spheres in a plane on a static floor conserve
    kinetic, rotational and potential energy."""
    sim = planar(400, 20.0, 7, v_init=1.0)
    sim.P[K.P_A] = 0.0
    sim.P[K.P_EPS] = 1.0
    sim.P[K.P_B] = 0.0
    sim.P[K.P_MU] = 1e9
    sim.P[K.P_BETA0] = 1.0
    spin_about_y(sim, 1)
    sim.rebuild()
    E0 = planar_energy(sim)
    for k in range(1, 11):
        sim.run_to(0.5 * k)
    E1 = planar_energy(sim)
    assert sim.cnt[K.C_PP] > 3000
    assert abs(E1 - E0) < 1e-8 * abs(E0), (E0, E1)
    assert_planar(sim)


@pytest.mark.parametrize("n_particles, t_end", [(20, 6.0), (60, 4.5)])
def test_planar_matches_all_pairs_reference(n_particles, t_end):
    """Both cases stop soon after the layer lands: event counts still match
    at t = 8, but in the landing burst the round-off differences grow from
    about 1e-12 at t = 4 to 1e-7 at t = 8, past the comparison tolerance."""
    sim = planar(n_particles, 6.0, 723, v_init=1.0)
    spin_about_y(sim, 723)
    sim.rebuild()
    S0, W0, mass, P = sim.S.copy(), sim.W.copy(), sim.mass.copy(), sim.P.copy()
    S_ref, W_ref, counts_ref = all_pairs_reference(S0, W0, mass, P, 0.0, t_end)
    sim.run_to(t_end)
    r, v, w = sim.snapshot()
    counts = sim.cnt[[K.C_PP, K.C_WALL, K.C_PLATE]]
    assert counts_ref.min() > 0
    np.testing.assert_array_equal(counts, counts_ref)
    np.testing.assert_allclose(r, S_ref[:sim.N, 0:3], atol=1e-8)
    np.testing.assert_allclose(v, S_ref[:sim.N, 3:6], atol=1e-8)
    np.testing.assert_allclose(w, W_ref, atol=1e-8)


def test_checkpoint_dimension_mismatch_raises(tmp_path):
    path = str(tmp_path / "state.npz")
    planar(100, 10.0, 3).save_checkpoint(path)
    spheres = Simulation(100, 10.0, 3.0, 0.44, 10.0, 3)
    with pytest.raises(ValueError, match="checkpoint is 2D"):
        spheres.load_checkpoint(path)
