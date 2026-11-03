"""Event-driven hard-sphere kernel for the vertically oscillated granular layer
of Bizon et al., PRL 80, 57 (1998).

Model (all quantities in units of the mean diameter D, gravity g, and the mass
of a sphere of diameter D):

* particles are inelastic, frictional hard spheres that interact only through
  instantaneous binary collisions and move under gravity between collisions;
* normal restitution  e(vn) = 1 - B vn^alpha  for vn < v0,  e = eps  otherwise,
  B = (1 - eps) v0^-alpha;
* tangential impulse from Walton's frictional hard-sphere collision operator
  (Walton 1993, Eqs. 25.15-25.27): sliding with Coulomb friction mu, cut off at
  the rolling limit where the tangential surface-velocity ratio is -beta0;
* stationary side walls at x = 0, L and y = 0, L, and a bottom plate at
  z_p(t) = A sin(omega t); ball-wall collisions use the same eps, mu, beta0;
* delayed-states event-driven algorithm (Lubachevsky 1991, Fig. 6.1; Marin,
  Risso & Cordero 1993): every particle keeps its own state time and only the
  particles taking part in an event are updated; one scheduled event per
  particle, a complete binary tree over the particle event times, and a cell
  grid whose boundary crossings are (virtual-wall) events.

Particle state is stored as an array of structures S[i] = (x, y, z, vx, vy,
vz, t_state, radius) so that the neighbour loop touches one cache line per
particle; angular velocities W[i] and masses are only needed in collisions.
"""

import numpy as np
from numba import njit

# event types
EV_PP = 1      # particle-particle collision, partner = particle index
EV_WALL = 2    # side-wall collision, partner = 0:x-, 1:x+, 2:y-, 3:y+
EV_PLATE = 3   # collision with the oscillating bottom plate
EV_CELL = 4    # cell-boundary crossing, partner = face 0:x- 1:x+ 2:y- 3:y+ 4:z- 5:z+
EV_ADV = 5     # advancement: bring state to event time and re-predict

# state columns
SX, SY, SZ, SVX, SVY, SVZ, ST, SR = range(8)

# float parameter vector layout
P_L, P_HX, P_HZ, P_Z0, P_A, P_OM, P_G, P_EPS, P_ALPHA, P_V0, P_B, P_MU, \
    P_BETA0, P_K, P_BTOL, P_RMAX = range(16)
NP_FLOAT = 16
# int parameter vector layout
I_NX, I_NY, I_NZ, I_N, I_M = range(5)
NP_INT = 5

# counters
C_PP, C_WALL, C_PLATE, C_CELL, C_ADV, C_EVENTS, C_PPSKIP, C_PLSKIP, \
    C_TINYPP, C_TINYPL, C_PREDICT, C_PAIRS, C_ROOTCALL = range(13)
NCOUNT = 20

INF = np.inf

# fail-fast tolerances: geometric errors larger than these mean a missed or
# mispredicted event, not round-off
PLATE_PENETRATION_TOL = 2e-8    # sphere below the plate surface at prediction
PLATE_CONTACT_TOL = 2e-8        # |gap| at a plate collision
PAIR_PENETRATION_TOL = 2e-8     # pair overlap depth at prediction
PLATE_MAX_SEGMENTS = 1000       # monotone-curvature segments per plate search


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------

@njit(cache=True, inline='always')
def restitution(vn_abs, eps, alpha, v0, B):
    if vn_abs >= v0:
        return eps
    return 1.0 - B * vn_abs ** alpha


@njit(cache=True, inline='always')
def advance(i, t, S, g):
    dt = t - S[i, ST]
    if dt != 0.0:
        S[i, SX] += S[i, SVX] * dt
        S[i, SY] += S[i, SVY] * dt
        S[i, SZ] += (S[i, SVZ] - 0.5 * g * dt) * dt
        S[i, SVZ] -= g * dt
        S[i, ST] = t


@njit(cache=True, inline='always')
def cbt_update(i, tree, ev_t, M):
    k = (M + i) >> 1
    while k >= 1:
        a = tree[2 * k]
        b = tree[2 * k + 1]
        if ev_t[a] <= ev_t[b]:
            tree[k] = a
        else:
            tree[k] = b
        k >>= 1


@njit(cache=True)
def cbt_build(tree, ev_t, N, M):
    for k in range(M):
        if k < N:
            tree[M + k] = k
        else:
            tree[M + k] = N      # sentinel, ev_t[N] = +inf
    for k in range(M - 1, 0, -1):
        a = tree[2 * k]
        b = tree[2 * k + 1]
        if ev_t[a] <= ev_t[b]:
            tree[k] = a
        else:
            tree[k] = b


@njit(cache=True, inline='always')
def cell_remove(i, cellof, head, nxt, prv):
    c = cellof[i]
    p = prv[i]
    n = nxt[i]
    if p >= 0:
        nxt[p] = n
    else:
        head[c] = n
    if n >= 0:
        prv[n] = p


@njit(cache=True, inline='always')
def cell_insert(i, c, cellof, head, nxt, prv):
    h = head[c]
    nxt[i] = h
    prv[i] = -1
    if h >= 0:
        prv[h] = i
    head[c] = i
    cellof[i] = c


@njit(cache=True)
def cell_of_position(x, y, z, P, IP):
    nx = IP[I_NX]
    ny = IP[I_NY]
    nz = IP[I_NZ]
    hx = P[P_HX]
    hz = P[P_HZ]
    z0 = P[P_Z0]
    ix = int(x / hx)
    iy = int(y / hx)
    iz = int((z - z0) / hz)
    if ix < 0:
        ix = 0
    if ix > nx - 1:
        ix = nx - 1
    if iy < 0:
        iy = 0
    if iy > ny - 1:
        iy = ny - 1
    if iz < 1:
        iz = 1
    if iz > nz - 1:
        iz = nz - 1
    return ix + nx * (iy + ny * iz)


@njit(cache=True)
def build_cells(S, cellof, head, nxt, prv, P, IP):
    N = IP[I_N]
    for c in range(head.shape[0]):
        head[c] = -1
    for i in range(N - 1, -1, -1):
        cell_insert(i, cell_of_position(S[i, SX], S[i, SY], S[i, SZ], P, IP),
                    cellof, head, nxt, prv)


# ----------------------------------------------------------------------------
# collision operators (Walton 1993, section 25.5)
# ----------------------------------------------------------------------------

@njit(cache=True)
def collide_pp(i, j, S, W, mass, P, cnt):
    """Binary collision of spheres i (=a) and j (=b), states at the same time."""
    eps = P[P_EPS]
    K = P[P_K]
    mu = P[P_MU]
    beta0 = P[P_BETA0]
    dx = S[j, SX] - S[i, SX]
    dy = S[j, SY] - S[i, SY]
    dz = S[j, SZ] - S[i, SZ]
    dist = np.sqrt(dx * dx + dy * dy + dz * dz)
    nx_ = dx / dist
    ny_ = dy / dist
    nz_ = dz / dist
    # relative velocity v_ab = v_b - v_a
    vax = S[j, SVX] - S[i, SVX]
    vay = S[j, SVY] - S[i, SVY]
    vaz = S[j, SVZ] - S[i, SVZ]
    vn = vax * nx_ + vay * ny_ + vaz * nz_
    if vn >= 0.0:
        cnt[C_PPSKIP] += 1
        return False
    ri = S[i, SR]
    rj = S[j, SR]
    # tangential relative velocity and relative surface velocity
    vtx = vax - vn * nx_
    vty = vay - vn * ny_
    vtz = vaz - vn * nz_
    wsx = ri * W[i, 0] + rj * W[j, 0]
    wsy = ri * W[i, 1] + rj * W[j, 1]
    wsz = ri * W[i, 2] + rj * W[j, 2]
    # v_s = v_t + n x (r_a w_a + r_b w_b)
    vsx = vtx + (ny_ * wsz - nz_ * wsy)
    vsy = vty + (nz_ * wsx - nx_ * wsz)
    vsz = vtz + (nx_ * wsy - ny_ * wsx)
    e = restitution(-vn, eps, P[P_ALPHA], P[P_V0], P[P_B])
    if -vn < 1e-10:
        cnt[C_TINYPP] += 1
    mi = mass[i]
    mj = mass[j]
    meff = mi * mj / (mi + mj)
    vs2 = vsx * vsx + vsy * vsy + vsz * vsz
    onepb = 0.0
    if vs2 > 0.0:
        # sliding solution (Walton Eq. 25.23), capped by the rolling limit beta0
        onepb = mu * (1.0 + e) * (1.0 + 1.0 / K) * (-vn) / np.sqrt(vs2)
        if onepb > 1.0 + beta0:
            onepb = 1.0 + beta0
    pn = meff * (1.0 + e) * vn             # normal impulse on a (along n)
    ft = meff * K * onepb / (K + 1.0)       # tangential impulse on a = ft * vs
    ptx = ft * vsx
    pty = ft * vsy
    ptz = ft * vsz
    px = pn * nx_ + ptx
    py = pn * ny_ + pty
    pz = pn * nz_ + ptz
    S[i, SVX] += px / mi
    S[i, SVY] += py / mi
    S[i, SVZ] += pz / mi
    S[j, SVX] -= px / mj
    S[j, SVY] -= py / mj
    S[j, SVZ] -= pz / mj
    # n x P_t
    cx = ny_ * ptz - nz_ * pty
    cy = nz_ * ptx - nx_ * ptz
    cz = nx_ * pty - ny_ * ptx
    fi = 1.0 / (K * mi * ri)     # 2/(K m sigma) with sigma = 2 r
    fj = 1.0 / (K * mj * rj)
    W[i, 0] += fi * cx
    W[i, 1] += fi * cy
    W[i, 2] += fi * cz
    W[j, 0] += fj * cx
    W[j, 1] += fj * cy
    W[j, 2] += fj * cz
    return True


@njit(cache=True)
def collide_wall(i, nx_, ny_, nz_, wvx, wvy, wvz, S, W, P):
    """Collision of sphere i with an infinitely massive flat wall.

    (nx_, ny_, nz_) is the unit normal pointing from the sphere into the wall,
    (wvx, wvy, wvz) the wall velocity.  Returns the post-collision normal
    separation speed, or -1 if the sphere was not approaching.
    """
    eps = P[P_EPS]
    K = P[P_K]
    mu = P[P_MU]
    beta0 = P[P_BETA0]
    vax = wvx - S[i, SVX]
    vay = wvy - S[i, SVY]
    vaz = wvz - S[i, SVZ]
    vn = vax * nx_ + vay * ny_ + vaz * nz_
    if vn >= 0.0:
        return -1.0
    ri = S[i, SR]
    vtx = vax - vn * nx_
    vty = vay - vn * ny_
    vtz = vaz - vn * nz_
    wsx = ri * W[i, 0]
    wsy = ri * W[i, 1]
    wsz = ri * W[i, 2]
    vsx = vtx + (ny_ * wsz - nz_ * wsy)
    vsy = vty + (nz_ * wsx - nx_ * wsz)
    vsz = vtz + (nx_ * wsy - ny_ * wsx)
    e = restitution(-vn, eps, P[P_ALPHA], P[P_V0], P[P_B])
    vs2 = vsx * vsx + vsy * vsy + vsz * vsz
    onepb = 0.0
    if vs2 > 0.0:
        onepb = mu * (1.0 + e) * (1.0 + 1.0 / K) * (-vn) / np.sqrt(vs2)
        if onepb > 1.0 + beta0:
            onepb = 1.0 + beta0
    # impulse per unit mass on the sphere (m_eff = m for an immovable wall)
    pn = (1.0 + e) * vn
    ft = K * onepb / (K + 1.0)
    ptx = ft * vsx
    pty = ft * vsy
    ptz = ft * vsz
    S[i, SVX] += pn * nx_ + ptx
    S[i, SVY] += pn * ny_ + pty
    S[i, SVZ] += pn * nz_ + ptz
    cx = ny_ * ptz - nz_ * pty
    cy = nz_ * ptx - nx_ * ptz
    cz = nx_ * pty - ny_ * ptx
    fi = 1.0 / (K * ri)
    W[i, 0] += fi * cx
    W[i, 1] += fi * cy
    W[i, 2] += fi * cz
    return -e * vn


# ----------------------------------------------------------------------------
# event prediction
# ----------------------------------------------------------------------------

@njit(cache=True, inline='always')
def plate_gap(tau, gap0, vz, phase, A, om, g):
    """Gap between sphere bottom and plate at t + tau, given the gap gap0 at t.

    The plate displacement A sin(phase + om tau) - A sin(phase) is written as
    2 A cos(phase + om tau / 2) sin(om tau / 2), which avoids cancellation
    when tau is small.
    """
    return (gap0 + vz * tau - 0.5 * g * tau * tau
            - 2.0 * A * np.cos(phase + 0.5 * om * tau) * np.sin(0.5 * om * tau))


@njit(cache=True, inline='always')
def plate_gap_rate(tau, vz, phase, A, om, g):
    return vz - g * tau - A * om * np.cos(phase + om * tau)


@njit(cache=True)
def plate_gap_root(lower, upper, gap0, vz, phase, A, om, g):
    """Root of the gap in [lower, upper] with gap(lower) > 0 >= gap(upper):
    Newton steps safeguarded by bisection."""
    trial = upper
    for _ in range(100):
        value = plate_gap(trial, gap0, vz, phase, A, om, g)
        if value > 0.0:
            lower = trial
        else:
            upper = trial
        rate = plate_gap_rate(trial, vz, phase, A, om, g)
        if rate != 0.0 and abs(value / rate) < 1e-14 * max(1.0, trial):
            return trial
        if upper - lower < 2e-14 * max(1.0, upper):
            return 0.5 * (lower + upper)
        if rate != 0.0:
            candidate = trial - value / rate
        else:
            candidate = lower
        if candidate <= lower or candidate >= upper:
            candidate = 0.5 * (lower + upper)
        trial = candidate
    return 0.5 * (lower + upper)


@njit(cache=True)
def plate_root(zi, vzi, ri, t, horizon, A, om, g):
    """First time tau in [0, horizon] at which the sphere (state at time t)
    touches the plate z_p = A sin(om t') while approaching it, or INF.

    The gap h(tau) = zi + vzi tau - g tau^2/2 - ri - A sin(om (t + tau)) has
    curvature -g + A om^2 sin(om (t + tau)), which changes sign only where
    sin(om (t + tau)) = g / (A om^2).  Between those points h is convex or
    concave, so it has at most one extremum; that extremum is located from the
    sign of h', and the first sign change of h is then bracketed and solved.
    Raises if the sphere starts inside the plate.
    """
    phase = (om * t) % (2.0 * np.pi)
    gap0 = zi - ri - A * np.sin(phase)
    if gap0 < -PLATE_PENETRATION_TOL:
        raise ValueError("sphere penetrates the bottom plate")
    if gap0 < 0.0:
        gap0 = 0.0
    curv_max = g + A * om * om
    # lower bound of h on [0, horizon] from h'(0) >= vzi - A om, |h''| <= curv_max
    if gap0 + min(0.0, vzi - A * om) * horizon - 0.5 * curv_max * horizon * horizon > 1e-12:
        return INF
    if gap0 == 0.0 and plate_gap_rate(0.0, vzi, phase, A, om, g) < 0.0:
        return 0.0
    # the sphere bottom stays above the highest plate position
    if min(zi, zi + vzi * horizon - 0.5 * g * horizon * horizon) - ri > A:
        return INF
    split = A * om * om > g
    turn = 0.0
    if split:
        turn = np.arcsin(g / (A * om * om))
    two_pi = 2.0 * np.pi
    lower = 0.0
    for _ in range(PLATE_MAX_SEGMENTS):
        upper = horizon
        if split:
            psi = phase + om * lower
            turn1 = turn + two_pi * (np.floor((psi - turn) / two_pi) + 1.0)
            turn2 = np.pi - turn + two_pi * (np.floor((psi - np.pi + turn) / two_pi) + 1.0)
            upper = min(horizon, (min(turn1, turn2) - phase) / om)
            if upper <= lower + 1e-14:
                upper = min(horizon, lower + 1e-12)
        rate_lower = plate_gap_rate(lower, vzi, phase, A, om, g)
        rate_upper = plate_gap_rate(upper, vzi, phase, A, om, g)
        middle = upper
        if rate_lower * rate_upper < 0.0:
            # isolate the extremum of h in this segment
            left = lower
            right = upper
            middle = 0.5 * (left + right)
            for _ in range(100):
                rate_middle = plate_gap_rate(middle, vzi, phase, A, om, g)
                if rate_middle * rate_lower > 0.0:
                    left = middle
                else:
                    right = middle
                curvature = -g + A * om * om * np.sin(phase + om * middle)
                if curvature != 0.0 and abs(rate_middle / curvature) < 1e-14:
                    break
                if right - left < 2e-14:
                    middle = 0.5 * (left + right)
                    break
                if curvature != 0.0:
                    candidate = middle - rate_middle / curvature
                else:
                    candidate = left
                if candidate <= left or candidate >= right:
                    candidate = 0.5 * (left + right)
                middle = candidate
        if plate_gap(middle, gap0, vzi, phase, A, om, g) < 0.0:
            return plate_gap_root(lower, middle, gap0, vzi, phase, A, om, g)
        if plate_gap(upper, gap0, vzi, phase, A, om, g) < 0.0:
            return plate_gap_root(middle, upper, gap0, vzi, phase, A, om, g)
        if upper >= horizon:
            return INF
        lower = upper
    raise RuntimeError("plate root isolation exceeded the segment limit")


@njit(cache=True)
def predict(i, t, S, cellof, head, nxt, ev_t, P, IP, cnt):
    """Earliest event of particle i (state at time t) given the current
    states of its neighbours.  Pair events are only accepted if they occur
    before the partner's own scheduled event (Lubachevsky invariant)."""
    L = P[P_L]
    hx = P[P_HX]
    hz = P[P_HZ]
    z0 = P[P_Z0]
    g = P[P_G]
    btol = P[P_BTOL]
    nx = IP[I_NX]
    ny = IP[I_NY]
    nz = IP[I_NZ]
    xi = S[i, SX]
    yi = S[i, SY]
    zi = S[i, SZ]
    vxi = S[i, SVX]
    vyi = S[i, SVY]
    vzi = S[i, SVZ]
    ri = S[i, SR]
    c = cellof[i]
    ix = c % nx
    tmp = c // nx
    iy = tmp % ny
    iz = tmp // ny

    best = INF
    btype = EV_ADV
    bp = -1
    # --- x: cell faces / side walls
    if vxi > 0.0:
        if ix < nx - 1:
            d = (ix + 1) * hx - xi
            if d < 0.0:
                d = 0.0
            tt = d / vxi
            if tt < best:
                best = tt
                btype = EV_CELL
                bp = 1
        else:
            d = L - ri - xi
            if d < 0.0:
                d = 0.0
            tt = d / vxi
            if tt < best:
                best = tt
                btype = EV_WALL
                bp = 1
    elif vxi < 0.0:
        if ix > 0:
            d = xi - ix * hx
            if d < 0.0:
                d = 0.0
            tt = d / (-vxi)
            if tt < best:
                best = tt
                btype = EV_CELL
                bp = 0
        else:
            d = xi - ri
            if d < 0.0:
                d = 0.0
            tt = d / (-vxi)
            if tt < best:
                best = tt
                btype = EV_WALL
                bp = 0
    # --- y
    if vyi > 0.0:
        if iy < ny - 1:
            d = (iy + 1) * hx - yi
            if d < 0.0:
                d = 0.0
            tt = d / vyi
            if tt < best:
                best = tt
                btype = EV_CELL
                bp = 3
        else:
            d = L - ri - yi
            if d < 0.0:
                d = 0.0
            tt = d / vyi
            if tt < best:
                best = tt
                btype = EV_WALL
                bp = 3
    elif vyi < 0.0:
        if iy > 0:
            d = yi - iy * hx
            if d < 0.0:
                d = 0.0
            tt = d / (-vyi)
            if tt < best:
                best = tt
                btype = EV_CELL
                bp = 2
        else:
            d = yi - ri
            if d < 0.0:
                d = 0.0
            tt = d / (-vyi)
            if tt < best:
                best = tt
                btype = EV_WALL
                bp = 2
    # --- z faces (parabolic motion)
    if iz < nz - 1 and vzi > 0.0:
        d = z0 + (iz + 1) * hz - zi
        if d < 0.0:
            d = 0.0
        disc = vzi * vzi - 2.0 * g * d
        if disc >= 0.0:
            tt = 2.0 * d / (vzi + np.sqrt(disc))
            if tt < best:
                best = tt
                btype = EV_CELL
                bp = 5
    if iz > 0:
        d = zi - (z0 + iz * hz)
        if d < 0.0:
            d = 0.0
        S_ = np.sqrt(vzi * vzi + 2.0 * g * d)
        if vzi > 0.0:
            tt = (vzi + S_) / g
        else:
            den = S_ - vzi
            if den > 0.0:
                tt = 2.0 * d / den
            else:
                tt = 0.0
        if tt < best:
            best = tt
            btype = EV_CELL
            bp = 4

    # --- particle pairs in the 27 neighbouring cells
    npair = 0
    for jz in range(iz - 1, iz + 2):
        if jz < 0 or jz >= nz:
            continue
        for jy in range(iy - 1, iy + 2):
            if jy < 0 or jy >= ny:
                continue
            base = nx * (jy + ny * jz)
            for jx in range(ix - 1, ix + 2):
                if jx < 0 or jx >= nx:
                    continue
                j = head[base + jx]
                while j >= 0:
                    npair += 1
                    if j != i:
                        dtj = t - S[j, ST]
                        dvz = S[j, SVZ] - g * dtj - vzi
                        ddx = S[j, SX] + S[j, SVX] * dtj - xi
                        ddy = S[j, SY] + S[j, SVY] * dtj - yi
                        ddz = S[j, SZ] + (S[j, SVZ] - 0.5 * g * dtj) * dtj - zi
                        dvx = S[j, SVX] - vxi
                        dvy = S[j, SVY] - vyi
                        b = ddx * dvx + ddy * dvy + ddz * dvz
                        if b < 0.0:
                            sig = ri + S[j, SR]
                            cc = ddx * ddx + ddy * ddy + ddz * ddz - sig * sig
                            a = dvx * dvx + dvy * dvy + dvz * dvz
                            if cc <= 0.0:
                                # touching / overlapping by round-off
                                if cc < -2.0 * sig * PAIR_PENETRATION_TOL:
                                    raise ValueError("sphere pair overlaps")
                                if b < -btol * np.sqrt(a):
                                    tt = 0.0
                                else:
                                    tt = INF
                            else:
                                disc = b * b - a * cc
                                if disc > 0.0:
                                    tt = cc / (np.sqrt(disc) - b)
                                else:
                                    tt = INF
                            if tt < best and t + tt < ev_t[j]:
                                best = tt
                                btype = EV_PP
                                bp = j
                    j = nxt[j]

    cnt[C_PAIRS] += npair
    cnt[C_PREDICT] += 1
    # --- bottom plate (only reachable from low cells)
    A = P[P_A]
    if z0 + iz * hz - ri <= A:
        if best == INF:
            raise RuntimeError("plate search without a finite horizon")
        tpl = plate_root(zi, vzi, ri, t, best, A, P[P_OM], g)
        cnt[C_ROOTCALL] += 1
        if tpl < best:
            best = tpl
            btype = EV_PLATE
            bp = 0
    if best == INF:
        best = 1.0
        btype = EV_ADV
        bp = -1
    return t + best, btype, bp


@njit(cache=True)
def schedule(i, t, S, cellof, head, nxt, ev_t, ev_type, ev_p, tree, P, IP,
             cnt):
    tb, typ, p = predict(i, t, S, cellof, head, nxt, ev_t, P, IP, cnt)
    M = IP[I_M]
    if typ == EV_PP:
        j = p
        if ev_type[j] == EV_PP:
            m = ev_p[j]
            if m != i:
                ev_type[m] = EV_ADV     # preempted: m re-predicts at its time
        ev_t[j] = tb
        ev_type[j] = EV_PP
        ev_p[j] = i
        cbt_update(j, tree, ev_t, M)
    ev_t[i] = tb
    ev_type[i] = typ
    ev_p[i] = p
    cbt_update(i, tree, ev_t, M)


# ----------------------------------------------------------------------------
# main loop
# ----------------------------------------------------------------------------

@njit(cache=True)
def run_events(S, W, mass, cellof, head, nxt, prv, ev_t, ev_type, ev_p, tree,
               P, IP, t_stop, max_events, cnt):
    """Process all events with time < t_stop (or until max_events).
    Returns 0 if t_stop was reached, 1 if max_events was hit."""
    g = P[P_G]
    A = P[P_A]
    om = P[P_OM]
    nx = IP[I_NX]
    ny = IP[I_NY]
    nev = 0
    while True:
        i = tree[1]
        t = ev_t[i]
        if t >= t_stop:
            return 0
        if nev >= max_events:
            return 1
        nev += 1
        cnt[C_EVENTS] += 1
        typ = ev_type[i]
        if typ == EV_PP:
            j = ev_p[i]
            advance(i, t, S, g)
            advance(j, t, S, g)
            if collide_pp(i, j, S, W, mass, P, cnt):
                cnt[C_PP] += 1
            ev_type[j] = EV_ADV
            ev_t[j] = t
            schedule(i, t, S, cellof, head, nxt, ev_t, ev_type, ev_p, tree, P,
                     IP, cnt)
            schedule(j, t, S, cellof, head, nxt, ev_t, ev_type, ev_p, tree, P,
                     IP, cnt)
        elif typ == EV_CELL:
            advance(i, t, S, g)
            f = ev_p[i]
            c = cellof[i]
            if f == 0:
                cn = c - 1
            elif f == 1:
                cn = c + 1
            elif f == 2:
                cn = c - nx
            elif f == 3:
                cn = c + nx
            elif f == 4:
                cn = c - nx * ny
            else:
                cn = c + nx * ny
            cell_remove(i, cellof, head, nxt, prv)
            cell_insert(i, cn, cellof, head, nxt, prv)
            cnt[C_CELL] += 1
            schedule(i, t, S, cellof, head, nxt, ev_t, ev_type, ev_p, tree, P,
                     IP, cnt)
        elif typ == EV_PLATE:
            advance(i, t, S, g)
            if abs(S[i, SZ] - S[i, SR] - A * np.sin(om * t)) > PLATE_CONTACT_TOL:
                raise ValueError("plate collision off the plate surface")
            vp = A * om * np.cos(om * t)
            vsep = collide_wall(i, 0.0, 0.0, -1.0, 0.0, 0.0, vp, S, W, P)
            if vsep >= 0.0:
                cnt[C_PLATE] += 1
                if vsep < 1e-10:
                    cnt[C_TINYPL] += 1
            else:
                cnt[C_PLSKIP] += 1
            schedule(i, t, S, cellof, head, nxt, ev_t, ev_type, ev_p, tree, P,
                     IP, cnt)
        elif typ == EV_WALL:
            advance(i, t, S, g)
            f = ev_p[i]
            if f == 0:
                vs = collide_wall(i, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, S, W, P)
            elif f == 1:
                vs = collide_wall(i, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, S, W, P)
            elif f == 2:
                vs = collide_wall(i, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, S, W, P)
            else:
                vs = collide_wall(i, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, S, W, P)
            if vs >= 0.0:
                cnt[C_WALL] += 1
            schedule(i, t, S, cellof, head, nxt, ev_t, ev_type, ev_p, tree, P,
                     IP, cnt)
        else:   # EV_ADV
            advance(i, t, S, g)
            cnt[C_ADV] += 1
            schedule(i, t, S, cellof, head, nxt, ev_t, ev_type, ev_p, tree, P,
                     IP, cnt)


@njit(cache=True)
def init_events(ev_t, ev_type, ev_p, tree, IP, t0):
    """All particles must have state time t0.  Every particle gets an
    advancement event at t0; the main loop then predicts them one by one."""
    N = IP[I_N]
    for i in range(N):
        ev_t[i] = t0
        ev_type[i] = EV_ADV
        ev_p[i] = -1
    ev_t[N] = INF
    cbt_build(tree, ev_t, N, IP[I_M])


@njit(cache=True)
def project(t, S, g, out_r, out_v):
    N = out_r.shape[0]
    for i in range(N):
        dt = t - S[i, ST]
        out_r[i, 0] = S[i, SX] + S[i, SVX] * dt
        out_r[i, 1] = S[i, SY] + S[i, SVY] * dt
        out_r[i, 2] = S[i, SZ] + (S[i, SVZ] - 0.5 * g * dt) * dt
        out_v[i, 0] = S[i, SVX]
        out_v[i, 1] = S[i, SVY]
        out_v[i, 2] = S[i, SVZ] - g * dt


@njit(cache=True)
def synchronize(t, S, g, N):
    for i in range(N):
        advance(i, t, S, g)


@njit(cache=True)
def rebase(T, S, ev_t, N):
    for i in range(N):
        S[i, ST] -= T
        if ev_t[i] < INF:
            ev_t[i] -= T


@njit(cache=True)
def min_gap(r, rad, cellof, head, nxt, P, IP):
    """Minimum surface gap between neighbouring pairs for synchronized
    positions r.  Returns (min gap, i, j)."""
    nx = IP[I_NX]
    ny = IP[I_NY]
    nz = IP[I_NZ]
    N = IP[I_N]
    best = INF
    bi = -1
    bj = -1
    for i in range(N):
        c = cellof[i]
        ix = c % nx
        tmp = c // nx
        iy = tmp % ny
        iz = tmp // ny
        for jz in range(iz - 1, iz + 2):
            if jz < 0 or jz >= nz:
                continue
            for jy in range(iy - 1, iy + 2):
                if jy < 0 or jy >= ny:
                    continue
                for jx in range(ix - 1, ix + 2):
                    if jx < 0 or jx >= nx:
                        continue
                    j = head[jx + nx * (jy + ny * jz)]
                    while j >= 0:
                        if j > i:
                            dx = r[j, 0] - r[i, 0]
                            dy = r[j, 1] - r[i, 1]
                            dz = r[j, 2] - r[i, 2]
                            gap = np.sqrt(dx * dx + dy * dy + dz * dz) - rad[i] - rad[j]
                            if gap < best:
                                best = gap
                                bi = i
                                bj = j
                        j = nxt[j]
    return best, bi, bj


@njit(cache=True)
def check_cells(r, cellof, P, IP):
    """Number of particles whose centre is outside its assigned cell by more
    than 1e-9 (positions r synchronized)."""
    nx = IP[I_NX]
    ny = IP[I_NY]
    nz = IP[I_NZ]
    hx = P[P_HX]
    hz = P[P_HZ]
    z0 = P[P_Z0]
    bad = 0
    for i in range(r.shape[0]):
        c = cellof[i]
        ix = c % nx
        tmp = c // nx
        iy = tmp % ny
        iz = tmp // ny
        tol = 1e-9
        if r[i, 0] < ix * hx - tol or r[i, 0] > (ix + 1) * hx + tol:
            bad += 1
        elif r[i, 1] < iy * hx - tol or r[i, 1] > (iy + 1) * hx + tol:
            bad += 1
        elif r[i, 2] < z0 + iz * hz - tol:
            bad += 1
        elif iz < nz - 1 and r[i, 2] > z0 + (iz + 1) * hz + tol:
            bad += 1
    return bad


@njit(cache=True)
def check_events(S, ev_t, ev_type, ev_p, N, t_now):
    """Consistency of the event queue: returns number of violations."""
    bad = 0
    for i in range(N):
        if ev_t[i] < t_now:
            bad += 1
        if S[i, ST] > t_now:
            bad += 1
        if ev_type[i] == EV_PP:
            j = ev_p[i]
            if ev_type[j] != EV_PP or ev_p[j] != i or ev_t[j] != ev_t[i]:
                bad += 1
    return bad
