"""Completely inelastic ball on a vibrated plate.

The layer is modelled as a single ball that sticks to the plate on every
impact (e = 0) and separates when the plate's downward acceleration exceeds
g.  Outputs per landing: flight time, impact speed relative to the plate,
and stuck time, as a function of Gamma.

Plate: z_p = -A cos(omega t), A = Gamma g / omega^2.
Separation when a_p < -g, i.e., cos(omega t) < -1/Gamma, so at phase
phi_sep = arccos(-1/Gamma).  After separation the ball is ballistic; landing
is z_ball = z_plate, found by root-finding over the next few periods.

Units: lengths in D (particle diameters), times in sqrt(D/g), speeds in
sqrt(gD).  The drive frequency f* = f sqrt(D/g) = omega/(2 pi sqrt(g/D)),
so omega = 2 pi f*.  At f* = 0.44 the period T = 1/f* = 2.273.  The
Bizon 1998 convention uses f* (dimensionless frequency) and Gamma
(dimensionless acceleration, A omega^2 / g).

Usage: inelastic_ball.py --fstar F [--gamma-min 3.0] [--gamma-max 7.0]
                         [--gamma-step 0.05] [--max-landings 20]
                         [--out evidence/inelastic-ball.json]
"""
import argparse
import json
from pathlib import Path

import numpy as np


def bisect(f, a, b, tol=1e-14, maxiter=100):
    """Simple bisection root finder (avoids scipy dependency)."""
    fa, fb = f(a), f(b)
    for _ in range(maxiter):
        m = 0.5 * (a + b)
        if b - a < tol:
            return m
        fm = f(m)
        if fa * fm <= 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return 0.5 * (a + b)

ap = argparse.ArgumentParser()
ap.add_argument("--fstar", type=float, required=True)
ap.add_argument("--gamma-min", type=float, default=3.0)
ap.add_argument("--gamma-max", type=float, default=7.0)
ap.add_argument("--gamma-step", type=float, default=0.05)
ap.add_argument("--max-landings", type=int, default=20)
ap.add_argument("--out", type=Path, default=None)
a = ap.parse_args()

omega = 2 * np.pi * a.fstar
T = 2 * np.pi / omega  # one drive period


def plate_z(t, Gamma):
    A = Gamma / omega**2  # g = 1 in our units
    return -A * np.cos(omega * t)


def plate_v(t, Gamma):
    A = Gamma / omega**2
    return A * omega * np.sin(omega * t)


def plate_a(t, Gamma):
    return Gamma * np.cos(omega * t)


def separation_phase(Gamma):
    """Phase (in radians) at which the ball separates: cos(phi) = -1/Gamma."""
    if Gamma <= 1.0:
        return None  # never separates
    return np.arccos(-1.0 / Gamma)


def ball_minus_plate(t, t_sep, z_sep, v_sep, Gamma):
    """z_ball - z_plate at time t, after separation at t_sep."""
    dt = t - t_sep
    z_ball = z_sep + v_sep * dt - 0.5 * dt**2  # g = 1
    return z_ball - plate_z(t, Gamma)


def find_landing(t_sep, z_sep, v_sep, Gamma, max_periods=5):
    """Find the next time the ball lands on the plate after t_sep."""
    dt_tiny = 1e-10
    t_lo = t_sep + dt_tiny
    # scan forward in small steps to find a bracket
    dt_scan = T / 200
    t_prev = t_lo
    f_prev = ball_minus_plate(t_prev, t_sep, z_sep, v_sep, Gamma)
    for _ in range(int(max_periods * 200)):
        t_next = t_prev + dt_scan
        f_next = ball_minus_plate(t_next, t_sep, z_sep, v_sep, Gamma)
        if f_next <= 0:
            # bracket found
            return bisect(lambda t: ball_minus_plate(t, t_sep, z_sep, v_sep, Gamma),
                          t_prev, t_next)
        t_prev, f_prev = t_next, f_next
    return None


def simulate(Gamma, max_landings):
    """Return a list of landings: (flight_time, impact_speed, stuck_time)."""
    if Gamma <= 1.0:
        return []

    phi_sep = separation_phase(Gamma)
    landings = []

    # first separation
    t_sep = phi_sep / omega
    z_sep = plate_z(t_sep, Gamma)
    v_sep = plate_v(t_sep, Gamma)

    for _ in range(max_landings):
        t_land = find_landing(t_sep, z_sep, v_sep, Gamma)
        if t_land is None:
            break
        dt_flight = t_land - t_sep
        # ball velocity at landing
        v_ball = v_sep - (t_land - t_sep)  # g = 1
        v_plate = plate_v(t_land, Gamma)
        impact_speed = abs(v_ball - v_plate)

        # stuck: ball rides with plate from landing to next separation
        # find next separation after landing
        phase_land = (omega * t_land) % (2 * np.pi)
        # separation at phase phi_sep or (2*pi - phi_sep)
        # cos(phi) = -1/Gamma; solutions are phi_sep and 2*pi - phi_sep
        # the ball sticks and waits for the next time cos(omega*t) drops below -1/Gamma
        # from the landing time
        # separation happens at two phases per cycle: phi_sep and 2*pi - phi_sep
        # but only the one where the plate is decelerating (going down) matters
        # separation: plate acceleration < -g means cos(omega*t) < -1/Gamma
        # the ball separates at phi_sep (which is in (pi/2, pi)) and stays separated
        # until it lands. It sticks at landing and waits for the next phi_sep.
        # Actually: cos(phi) < -1/Gamma means phi in (phi_sep, 2*pi - phi_sep).
        # So separation begins at phi_sep and ends at 2*pi - phi_sep, then the plate
        # accelerates upward again, pressing the ball.
        # After landing (ball sticks), it waits until the next time phi = phi_sep in a
        # future cycle.
        n_full = int(np.floor(omega * t_land / (2 * np.pi)))
        # find the next phi_sep after t_land
        t_next_sep = (n_full * 2 * np.pi + phi_sep) / omega
        if t_next_sep <= t_land + 1e-12:
            t_next_sep += T
        # but the ball only separates if at t_next_sep it is still on the plate,
        # meaning it must actually be stuck. Check: is the phase at landing before phi_sep?
        # The ball could land during the separation window (plate decelerating), meaning
        # it immediately separates again. That would be an instantaneous stick.
        # Check: at t_land, is cos(omega*t_land) < -1/Gamma? If yes, ball separates immediately.
        if np.cos(omega * t_land) < -1.0 / Gamma + 1e-12:
            # still in the separation window; ball separates immediately
            stuck_time = 0.0
            t_next_sep = t_land
        else:
            stuck_time = t_next_sep - t_land

        landings.append(dict(
            flight_time=dt_flight,
            impact_speed_gw=impact_speed / (1.0 / omega),  # in units of g/omega
            impact_speed=impact_speed,
            stuck_time=stuck_time,
            stuck_fraction=stuck_time / T,
            t_sep=t_sep,
            t_land=t_land,
        ))

        # next flight
        t_sep = t_next_sep
        z_sep = plate_z(t_sep, Gamma)
        v_sep = plate_v(t_sep, Gamma)

    return landings


results = []
gammas = np.arange(a.gamma_min, a.gamma_max + a.gamma_step / 2, a.gamma_step)
for Gamma in gammas:
    Gamma = round(Gamma, 4)
    landings = simulate(Gamma, a.max_landings)
    # check for period-2: do consecutive landings differ?
    flights = [L["flight_time"] for L in landings]
    period2 = False
    if len(flights) >= 4:
        # compare odd and even landings
        even = flights[0::2]
        odd = flights[1::2]
        if len(even) >= 2 and len(odd) >= 2:
            even_std = np.std(even[-min(5, len(even)):])
            odd_std = np.std(odd[-min(5, len(odd)):])
            if min(len(even), len(odd)) >= 2:
                diff = abs(np.mean(even[-5:]) - np.mean(odd[-5:]))
                mean_flight = np.mean(flights[-10:])
                period2 = diff > 0.01 * mean_flight

    results.append(dict(
        gamma=Gamma,
        f_star=a.fstar,
        landings=landings,
        n_landings=len(landings),
        period2=period2,
    ))

# find key transitions
period2_onset = None
both_soft = None  # both landings have impact < 1 g/omega
one_long = None   # one flight > 1.5 T
for r in results:
    if period2_onset is None and r["period2"]:
        period2_onset = r["gamma"]
    if r["period2"] and len(r["landings"]) >= 4:
        impacts = [L["impact_speed_gw"] for L in r["landings"][-4:]]
        if max(impacts) < 1.0 and both_soft is None:
            both_soft = r["gamma"]
        flights = [L["flight_time"] for L in r["landings"][-4:]]
        if max(flights) > 1.5 * T and one_long is None:
            one_long = r["gamma"]

output = dict(
    model="completely_inelastic_ball",
    f_star=a.fstar,
    gamma_range=[a.gamma_min, a.gamma_max],
    gamma_step=a.gamma_step,
    omega=omega,
    T=T,
    period2_onset=period2_onset,
    both_landings_soft_below=both_soft,
    one_long_flight_from=one_long,
    per_gamma=[dict(
        gamma=r["gamma"],
        n_landings=r["n_landings"],
        period2=bool(r["period2"]),
        flight_times=[L["flight_time"] for L in r["landings"][-4:]],
        impact_speeds_gw=[round(L["impact_speed_gw"], 4) for L in r["landings"][-4:]],
        stuck_times=[round(L["stuck_time"], 4) for L in r["landings"][-4:]],
        stuck_fractions=[round(L["stuck_fraction"], 4) for L in r["landings"][-4:]],
    ) for r in results],
)
out_path = a.out or Path("evidence/inelastic-ball.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(output, indent=1) + "\n")

print(f"f* = {a.fstar}, period T = {T:.4f}")
print(f"period-2 onset: Gamma = {period2_onset}")
print(f"both landings soft (< 1 g/omega): Gamma < {both_soft}")
print(f"one long flight (> 1.5 T): Gamma >= {one_long}")
print(f"written to {out_path}")
