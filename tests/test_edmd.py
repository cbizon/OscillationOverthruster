"""Unit tests of the collision operators, event predictions and the
event-driven engine."""

import math

import numpy as np
import pytest

from granular import edmd as K
from granular.sim import Simulation, drive_parameters


def params(eps=0.7, mu=0.5, beta0=0.35, alpha=0.75, v0=1.0):
    P = np.zeros(K.NP_FLOAT)
    P[K.P_EPS] = eps
    P[K.P_ALPHA] = alpha
    P[K.P_V0] = v0
    P[K.P_B] = (1 - eps) * v0 ** (-alpha)
    P[K.P_MU] = mu
    P[K.P_BETA0] = beta0
    P[K.P_K] = 0.4
    P[K.P_G] = 1.0
    return P


def make_S(r, v, rad):
    S = np.zeros((len(rad) + 1, 8))
    S[:len(rad), 0:3] = r
    S[:len(rad), 3:6] = v
    S[:len(rad), 7] = rad
    return S


def random_pair(rng):
    d = rng.uniform(0.99, 1.01, 2)
    rad = d / 2
    mass = d ** 3
    n = rng.normal(size=3)
    n /= np.linalg.norm(n)
    r = np.zeros((2, 3))
    r[1] = r[0] + n * (rad[0] + rad[1])
    v = rng.normal(size=(2, 3))
    # make them approach
    if np.dot(v[1] - v[0], n) > 0:
        v[1] -= 2 * np.dot(v[1] - v[0], n) * n
    w = rng.normal(size=(2, 3)) * 2
    return r, v, w, rad, mass, n


def surface_velocity(r, v, w, rad, n):
    vab = v[1] - v[0]
    vn = np.dot(vab, n)
    vt = vab - vn * n
    vs = vt + rad[0] * np.cross(n, w[0]) + rad[1] * np.cross(n, w[1])
    return vn, vs


def test_restitution_function():
    eps, alpha, v0 = 0.7, 0.75, 1.0
    B = (1 - eps) * v0 ** (-alpha)
    assert K.restitution(0.0, eps, alpha, v0, B) == 1.0
    assert K.restitution(2.0, eps, alpha, v0, B) == eps
    assert abs(K.restitution(1.0, eps, alpha, v0, B) - eps) < 1e-15
    vn = 0.3
    assert abs(K.restitution(vn, eps, alpha, v0, B) - (1 - B * vn ** alpha)) < 1e-15


@pytest.mark.parametrize("seed", range(20))
def test_pp_collision_conservation(seed):
    rng = np.random.default_rng(seed)
    r, v, w, rad, mass, n = random_pair(rng)
    P = params()
    cnt = np.zeros(K.NCOUNT, dtype=np.int64)
    I = 0.1 * mass * (2 * rad) ** 2           # K m sigma^2 / 4
    p0 = (mass[:, None] * v).sum(0)
    # angular momentum about the origin
    L0 = sum(mass[k] * np.cross(r[k], v[k]) + I[k] * w[k] for k in range(2))
    E0 = 0.5 * np.sum(mass[:, None] * v ** 2) + 0.5 * np.sum(I[:, None] * w ** 2)
    vn0, vs0 = surface_velocity(r, v, w, rad, n)
    S = make_S(r, v, rad)
    w1 = w.copy()
    assert K.collide_pp(0, 1, S, w1, mass, P, cnt)
    v1 = S[:2, 3:6].copy()
    p1 = (mass[:, None] * v1).sum(0)
    L1 = sum(mass[k] * np.cross(r[k], v1[k]) + I[k] * w1[k] for k in range(2))
    E1 = 0.5 * np.sum(mass[:, None] * v1 ** 2) + 0.5 * np.sum(I[:, None] * w1 ** 2)
    np.testing.assert_allclose(p1, p0, atol=1e-12)
    np.testing.assert_allclose(L1, L0, atol=1e-12)
    assert E1 <= E0 + 1e-12
    vn1, vs1 = surface_velocity(r, v1, w1, rad, n)
    e = K.restitution(-vn0, 0.7, 0.75, 1.0, 0.3)
    assert abs(vn1 + e * vn0) < 1e-12
    # tangential: vs' = -beta vs with beta = min(beta*, beta0)
    onepb = min(0.5 * (1 + e) * 3.5 * abs(vn0) / np.linalg.norm(vs0), 1.35)
    np.testing.assert_allclose(vs1, -(onepb - 1) * vs0, atol=1e-12)
    # tangential impulse never exceeds mu * normal impulse
    Jn = abs(mass[0] * np.dot(v1[0] - v[0], n))
    Jt = np.linalg.norm(mass[0] * ((v1[0] - v[0]) - np.dot(v1[0] - v[0], n) * n))
    assert Jt <= 0.5 * Jn * (1 + 1e-12)


def test_rough_elastic_conserves_energy():
    rng = np.random.default_rng(5)
    P = params(eps=1.0, mu=1e9, beta0=1.0)
    cnt = np.zeros(K.NCOUNT, dtype=np.int64)
    for _ in range(10):
        r, v, w, rad, mass, n = random_pair(rng)
        I = 0.1 * mass * (2 * rad) ** 2
        E0 = 0.5 * np.sum(mass[:, None] * v ** 2) + 0.5 * np.sum(I[:, None] * w ** 2)
        S = make_S(r, v, rad)
        K.collide_pp(0, 1, S, w, mass, P, cnt)
        v = S[:2, 3:6]
        E1 = 0.5 * np.sum(mass[:, None] * v ** 2) + 0.5 * np.sum(I[:, None] * w ** 2)
        assert abs(E1 - E0) < 1e-10 * E0


def test_equal_sphere_formulas_walton():
    """Equal spheres: compare with Walton Eqs. 25.25-25.27 directly."""
    rng = np.random.default_rng(11)
    P = params()
    cnt = np.zeros(K.NCOUNT, dtype=np.int64)
    for _ in range(10):
        r, v, w, rad, mass, n = random_pair(rng)
        rad[:] = 0.5
        mass[:] = 1.0
        r[1] = r[0] + n
        vn, vs = surface_velocity(r, v, w, rad, n)
        e = K.restitution(-vn, 0.7, 0.75, 1.0, 0.3)
        Kk = 0.4
        b1 = (0.5 * (1 + e) * (1 + 1 / Kk) * abs(vn) / np.linalg.norm(vs))
        b1 = min(b1, 1.35)          # 1 + beta
        dva = 0.5 * (1 + e) * vn * n + Kk * b1 / (2 * (Kk + 1)) * vs
        dwa = b1 / (1.0 * (Kk + 1)) * np.cross(n, vs)
        S = make_S(r, v, rad)
        w1 = w.copy()
        K.collide_pp(0, 1, S, w1, mass, P, cnt)
        v1 = S[:2, 3:6].copy()
        np.testing.assert_allclose(v1[0] - v[0], dva, atol=1e-12)
        np.testing.assert_allclose(v1[1] - v[1], -dva, atol=1e-12)
        np.testing.assert_allclose(w1[0] - w[0], dwa, atol=1e-12)
        np.testing.assert_allclose(w1[1] - w[1], dwa, atol=1e-12)


@pytest.mark.parametrize("seed", range(10))
def test_wall_collision(seed):
    rng = np.random.default_rng(100 + seed)
    P = params()
    cnt = np.zeros(K.NCOUNT, dtype=np.int64)
    n = np.array([0.0, 0.0, -1.0])
    rad = np.array([0.5 * rng.uniform(0.99, 1.01)])
    v = rng.normal(size=(1, 3))
    vw = np.array([0.0, 0.0, rng.normal()])
    v[0, 2] = vw[2] - abs(rng.normal()) - 0.01       # approaching the plate
    w = rng.normal(size=(1, 3))
    vab = vw - v[0]
    vn = np.dot(vab, n)
    vs = vab - vn * n + rad[0] * np.cross(n, w[0])
    S = make_S(np.zeros((1, 3)), v, rad)
    w1 = w.copy()
    sep = K.collide_wall(0, n[0], n[1], n[2], vw[0], vw[1], vw[2], S, w1, P)
    v1 = S[:1, 3:6].copy()
    vab1 = vw - v1[0]
    vn1 = np.dot(vab1, n)
    vs1 = vab1 - vn1 * n + rad[0] * np.cross(n, w1[0])
    e = K.restitution(-vn, 0.7, 0.75, 1.0, 0.3)
    assert abs(vn1 + e * vn) < 1e-12
    assert abs(sep - e * (-vn)) < 1e-12
    onepb = min(0.5 * (1 + e) * 3.5 * abs(vn) / np.linalg.norm(vs), 1.35)
    np.testing.assert_allclose(vs1, -(onepb - 1) * vs, atol=1e-12)
    # angular momentum about the contact point is conserved (wall impulse
    # acts at the contact point): m (c->r) x v + I w
    m = 1.0
    I = 0.1 * (2 * rad[0]) ** 2
    arm = -rad[0] * n                  # from contact point to centre
    L0 = m * np.cross(arm, v[0]) + I * w[0]
    L1 = m * np.cross(arm, v1[0]) + I * w1[0]
    np.testing.assert_allclose(L1, L0, atol=1e-12)


def brute_plate_root(zi, vzi, ri, t, tmax, A, om, g=1.0, n=200001):
    tau = np.linspace(0, tmax, n)
    h = zi + vzi * tau - 0.5 * g * tau ** 2 - ri - A * np.sin(om * (t + tau))
    k = np.nonzero(h <= 0)[0]
    if len(k) == 0:
        return np.inf
    k = k[0]
    if k == 0:
        return 0.0
    # refine by bisection
    a, b = tau[k - 1], tau[k]
    f = lambda s: zi + vzi * s - 0.5 * g * s ** 2 - ri - A * math.sin(om * (t + s))
    for _ in range(80):
        m = 0.5 * (a + b)
        if f(m) > 0:
            a = m
        else:
            b = m
    return 0.5 * (a + b)


@pytest.mark.parametrize("seed", range(30))
def test_plate_root(seed):
    rng = np.random.default_rng(200 + seed)
    gamma = rng.uniform(2, 7)
    f, om, A, T = drive_parameters(gamma, rng.uniform(0.2, 0.9), 5.42)
    t = rng.uniform(0, T)
    ri = 0.5
    zp = A * math.sin(om * t)
    zi = zp + ri + rng.exponential(1.0)
    vzi = A * om * math.cos(om * t) + rng.normal() * 2
    tmax = 3 * T
    tau, flag = K.plate_root(zi, vzi, ri, t, tmax, A, om, 1.0, 1e-12, 10000)
    tb = brute_plate_root(zi, vzi, ri, t, tmax, A, om)
    if np.isinf(tb):
        assert flag == 0
    else:
        assert flag == 1
        assert abs(tau - tb) < 1e-6 * max(1.0, tb), (tau, tb)


def test_plate_root_just_after_bounce():
    f, om, A, T = drive_parameters(3.0, 0.44, 5.42)
    for t in np.linspace(0, T, 37):
        zp = A * math.sin(om * t)
        vp = A * om * math.cos(om * t)
        for vrel in [1e-6, 1e-3, 0.1, 1.0]:
            tau, flag = K.plate_root(zp + 0.5, vp + vrel, 0.5, t, 3 * T, A, om,
                                     1.0, 1e-12, 100000)
            tb = brute_plate_root(zp + 0.5 + 1e-13, vp + vrel, 0.5, t, 3 * T, A, om,
                                  n=2000001)
            assert flag == 1
            assert tau > 0
            if tb > 1e-3:
                assert abs(tau - tb) < 1e-5 * max(1, tb), (t, vrel, tau, tb)


def energy(sim):
    r, v, w = sim.snapshot()
    I = 0.1 * sim.mass * sim.diam ** 2
    return (0.5 * np.sum(sim.mass[:, None] * v ** 2) + np.sum(sim.mass * r[:, 2])
            + 0.5 * np.sum(I[:, None] * w ** 2))


def test_engine_energy_conservation_elastic_static_plate():
    """Elastic, perfectly rough spheres in a box with a static floor: total
    energy (kinetic + rotational + potential) must be conserved."""
    sim = Simulation(600, 10.0, 3.0, 0.44, 5.42, 7, v_init=1.0)
    sim.P[K.P_A] = 0.0         # static plate at z = 0
    sim.P[K.P_EPS] = 1.0
    sim.P[K.P_B] = 0.0
    sim.P[K.P_MU] = 1e9
    sim.P[K.P_BETA0] = 1.0
    sim.W[:] = np.random.default_rng(1).normal(size=sim.W.shape)
    sim.rebuild()
    E0 = energy(sim)
    for k in range(1, 11):
        sim.run_to(0.5 * k)
        g, i, j, bad = sim.overlap_check()
        assert g > -1e-9
        assert bad == 0
    E1 = energy(sim)
    assert sim.cnt[K.C_PP] > 10000
    assert abs(E1 - E0) < 1e-8 * abs(E0), (E0, E1)


def test_engine_momentum_free_fall():
    """Far above the plate, with smooth spheres (mu = 0), neither pair nor
    side-wall collisions change the total vertical momentum: it must follow
    -g M t exactly."""
    sim = Simulation(600, 10.0, 3.0, 0.44, 5.42, 3, v_init=1.0)
    sim.P[K.P_MU] = 0.0
    sim.S[:sim.N, 2] += 40.0
    sim.rebuild()
    r0, v0, w0 = sim.snapshot()
    pz0 = np.sum(sim.mass * v0[:, 2])
    sim.run_to(2.0)
    r1, v1, w1 = sim.snapshot()
    pz1 = np.sum(sim.mass * v1[:, 2])
    assert sim.cnt[K.C_PP] > 1000 and sim.cnt[K.C_WALL] > 10
    assert abs(pz1 - (pz0 - 2.0 * np.sum(sim.mass))) < 1e-9 * np.sum(sim.mass)
    g, i, j, bad = sim.overlap_check()
    assert g > -1e-9 and bad == 0
