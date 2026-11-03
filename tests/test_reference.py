"""Whole-engine checks ported from the codex-gpt-6-astra-low trial.

The all-pairs reference advances every particle to every event and searches
all pairs, walls and the plate for the next one.  It shares the collision
operators and the plate-root solver with the engine, so agreement tests the
delayed states, cell lists and event scheduling: the parts where a missed or
stale event would otherwise go unnoticed.
"""

import numpy as np
import pytest

from granular import edmd as K
from granular.sim import Simulation


def all_pairs_reference(S, W, mass, P, t0, t_end):
    """Synchronous event loop over all particles; returns final (S, W, counts)."""
    S = S.copy()
    W = W.copy()
    N = len(mass)
    L = P[K.P_L]
    A = P[K.P_A]
    om = P[K.P_OM]
    g = P[K.P_G]
    btol = P[K.P_BTOL]
    cnt = np.zeros(K.NCOUNT, dtype=np.int64)
    counts = np.zeros(3, dtype=np.int64)
    t = t0
    walls = [(-1.0, 0.0), (1.0, 0.0), (0.0, -1.0), (0.0, 1.0)]
    while True:
        soonest = t_end - t
        event = None
        r = S[:N, 0:3]
        v = S[:N, 3:6]
        rad = S[:N, K.SR]
        for i in range(N):
            tp = K.plate_root(r[i, 2], v[i, 2], rad[i], t, soonest, A, om, g)
            if tp < soonest:
                soonest, event = tp, ("plate", i, -1)
            for axis in range(2):
                if v[i, axis] > 0.0:
                    tw = max(L - rad[i] - r[i, axis], 0.0) / v[i, axis]
                    face = 2 * axis + 1
                elif v[i, axis] < 0.0:
                    tw = max(r[i, axis] - rad[i], 0.0) / -v[i, axis]
                    face = 2 * axis
                else:
                    continue
                if tw < soonest:
                    soonest, event = tw, ("wall", i, face)
            dd = r[i + 1:] - r[i]
            dv = v[i + 1:] - v[i]
            b = np.einsum("ij,ij->i", dd, dv)
            a = np.einsum("ij,ij->i", dv, dv)
            sig = rad[i] + rad[i + 1:]
            cc = np.einsum("ij,ij->i", dd, dd) - sig * sig
            for k in np.flatnonzero(b < 0.0):
                if cc[k] <= 0.0:
                    tt = 0.0 if b[k] < -btol * np.sqrt(a[k]) else np.inf
                else:
                    disc = b[k] * b[k] - a[k] * cc[k]
                    tt = cc[k] / (np.sqrt(disc) - b[k]) if disc > 0.0 else np.inf
                if tt < soonest:
                    soonest, event = tt, ("pair", i, i + 1 + k)
        S[:N, 0:3] += S[:N, 3:6] * soonest
        S[:N, 2] -= 0.5 * g * soonest * soonest
        S[:N, 5] -= g * soonest
        t += soonest
        S[:N, K.ST] = t
        if event is None:
            return S, W, counts
        kind, i, j = event
        if kind == "pair":
            if K.collide_pp(i, j, S, W, mass, P, cnt):
                counts[0] += 1
        elif kind == "wall":
            nx, ny = walls[j]
            if K.collide_wall(i, nx, ny, 0.0, 0.0, 0.0, 0.0, S, W, P) >= 0.0:
                counts[1] += 1
        else:
            vp = A * om * np.cos(om * t)
            if K.collide_wall(i, 0.0, 0.0, -1.0, 0.0, 0.0, vp, S, W, P) >= 0.0:
                counts[2] += 1


@pytest.mark.parametrize("n_particles, t_end", [(20, 8.0), (120, 4.5)])
def test_delayed_states_match_all_pairs_reference(n_particles, t_end):
    """The dense case stops before the layer lands on the plate: in the landing
    collision burst, round-off differences grow chaotically (a 1e-13 nudge to
    one particle reaches 1e-2 within a quarter time unit), so trajectories
    can no longer be compared there."""
    sim = Simulation(n_particles, 6.0, 3.0, 0.44, 5.42, 723, v_init=1.0)
    sim.W[:] = np.random.default_rng(723).normal(size=sim.W.shape)
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


def test_checkpoint_restart_matches_continued_run(tmp_path):
    """A run restarted from a mid-cycle checkpoint, after a cycle boundary,
    reproduces the continued run bit for bit."""
    args = (100, 10.0, 3.0, 0.44, 5.42, 89)
    sim = Simulation(*args, v_init=1.0)
    sim.run_to(sim.T)
    sim.end_cycle()
    sim.rebuild(sort=True)
    sim.run_to(0.5 * sim.T)
    path = str(tmp_path / "state.npz")
    sim.save_checkpoint(path)
    sim.run_to(sim.T)
    expected = sim.snapshot(original_order=True)

    resumed = Simulation(*args, v_init=1.0)
    resumed.load_checkpoint(path)
    resumed.run_to(resumed.T)
    np.testing.assert_array_equal(resumed.cnt, sim.cnt)
    for actual, reference in zip(resumed.snapshot(original_order=True), expected):
        np.testing.assert_array_equal(actual, reference)
