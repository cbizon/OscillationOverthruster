"""Bulk quantities of a vibrated layer, for checking that a contact method
doesn't change the macroscopic physics.

``measure`` reads a trajectory (``granular/export.py`` format, or
``referee/c_baseline.py`` output, which has the same keys) and, over a
window of whole drive cycles, computes per frame:

- ``zcm``: centre-of-mass height above the plate;
- ``thickness``: standard deviation of particle heights (layer depth);
- ``ke_vertical``, ``ke_horizontal``: kinetic energy per particle in the
  lab frame, vertical and horizontal parts;
- ``temp_vertical``, ``temp_horizontal``: the same about the layer's
  centre-of-mass velocity (granular temperature, energy per particle);
- ``plate_contact``: fraction of particles whose bottom is within
  ``CONTACT_GAP`` of the plate.

Each is averaged by phase over the drive's response period (``--period``
cycles: 2 for patterns at f/2, 4 at f/4), giving a profile of
``32 * period`` phase bins, and its overall mean.  Take-off and landing
phases are where the plate-contact profile crosses ``CONTACT_THRESHOLD``.

Collision rate is deliberately not measured: contact methods model the
resting state differently (long contacts or many small collisions), so the
rate describes the method rather than the physics.

Trend check: the mean of each quantity over each successive response period
in the window, fitted with a straight line.  ``trend`` is the fitted change
across the window, ``trend_se`` its standard error; ``drifting`` is true when
the change differs from zero at 95% (two-sided Student t with periods - 2
degrees of freedom; with 5 periods that is 3.18 standard errors, not 2),
which means the settling time was too short.

``compare`` takes two measurements and, for each quantity, finds the
whole-cycle shift (0 to period - 1) that best aligns the profiles (a period-2
response can be in either phase), then reports the largest difference across
phase and the difference of means.  Masses are taken as d^3 in both codes.

Usage::

    uv run python referee/bulk.py measure TRAJ.npz --from-cycle 20 \\
        --cycles 10 --period 2 --out bulk.json
    uv run python referee/bulk.py compare A.json B.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

PHASES = 32
CONTACT_GAP = 0.02          # D; a particle this close to the plate touches it
CONTACT_THRESHOLD = 0.01    # fraction of particles touching: layer on the plate
# two-sided 95% Student t critical values by degrees of freedom
T95 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365,
       8: 2.306, 9: 2.262, 10: 2.228, 12: 2.179, 15: 2.131, 20: 2.086,
       30: 2.042}
QUANTITIES = ("zcm", "thickness", "ke_vertical", "ke_horizontal",
              "temp_vertical", "temp_horizontal", "plate_contact")


def drive_period(time: np.ndarray, phase: np.ndarray) -> float:
    """The drive period, from frames within a cycle (phase increasing)."""
    dt = np.diff(time)
    dphase = np.diff(phase)
    within = (dphase > 0) & (dt > 0)
    if not within.any():
        raise ValueError("no two frames within one cycle; can't infer the period")
    return float(np.median(dt[within] / dphase[within]))


def frame_quantities(positions, velocities, diameters, plate_z) -> dict[str, np.ndarray]:
    mass = diameters ** 3
    total = mass.sum()
    z = positions[:, :, 2].astype(np.float64)
    v = velocities.astype(np.float64)
    n = positions.shape[1]
    vcm = np.einsum("p,fpk->fk", mass, v) / total
    rel = v - vcm[:, None, :]
    gap = z - 0.5 * diameters[None, :] - plate_z[:, None]
    return {
        "zcm": np.einsum("p,fp->f", mass, z) / total - plate_z,
        "thickness": z.std(axis=1),
        "ke_vertical": 0.5 * np.einsum("p,fp->f", mass, v[:, :, 2] ** 2) / n,
        "ke_horizontal": 0.5 * np.einsum("p,fp->f", mass,
                                         v[:, :, 0] ** 2 + v[:, :, 1] ** 2) / n,
        "temp_vertical": 0.5 * np.einsum("p,fp->f", mass, rel[:, :, 2] ** 2) / n,
        "temp_horizontal": 0.5 * np.einsum("p,fp->f", mass,
                                           rel[:, :, 0] ** 2 + rel[:, :, 1] ** 2) / n,
        "plate_contact": (gap < CONTACT_GAP).mean(axis=1),
    }


def window_frames(time, phase, period_time, from_cycle, cycles) -> tuple[np.ndarray, np.ndarray]:
    """Indices of frames in [from_cycle, from_cycle + cycles), one per phase
    bin, and each frame's bin counted from the window start."""
    position = time / period_time                       # cycles since t = 0
    bins = np.rint(position * PHASES).astype(np.int64)
    if np.abs(position * PHASES - bins).max() > 1e-3:
        raise ValueError("frames are not on the 32-per-cycle phase grid")
    start, stop = from_cycle * PHASES, (from_cycle + cycles) * PHASES
    keep = (bins >= start) & (bins < stop)
    index = np.flatnonzero(keep)
    _, first = np.unique(bins[index], return_index=True)   # drop duplicate frames
    index = index[first]
    if index.size != cycles * PHASES:
        raise ValueError(f"window cycles {from_cycle} to {from_cycle + cycles} has "
                         f"{index.size} frames, expected {cycles * PHASES}; "
                         "the trajectory doesn't cover it")
    return index, bins[index] - start


def t95(dof: int) -> float:
    """Critical value for dof, rounding dof down to the table (conservative)."""
    if dof < 1:
        raise ValueError("no degrees of freedom")
    if dof > 30:
        return 1.96
    return T95[max(k for k in T95 if k <= dof)]


def trend(per_period: np.ndarray) -> tuple[float, float]:
    """Fitted change across the window and its standard error."""
    k = per_period.size
    if k < 3:
        raise ValueError("the trend check needs at least three response periods")
    x = np.arange(k, dtype=np.float64)
    slope, intercept = np.polyfit(x, per_period, 1)
    residual = per_period - (slope * x + intercept)
    se_slope = np.sqrt(residual @ residual / (k - 2) / ((x - x.mean()) @ (x - x.mean())))
    return float(slope * (k - 1)), float(se_slope * (k - 1))


def crossings(profile: np.ndarray, threshold: float) -> dict[str, list[float]]:
    """Phases (in cycles from the window start) where the profile rises above
    (landing) or falls below (take-off) the threshold, cyclically."""
    above = profile >= threshold
    rises = np.flatnonzero(above & ~np.roll(above, 1))
    falls = np.flatnonzero(~above & np.roll(above, 1))
    return {"landing": [float(i / PHASES) for i in rises],
            "takeoff": [float(i / PHASES) for i in falls]}


def measure(path: Path, from_cycle: int, cycles: int, period: int) -> dict[str, object]:
    if cycles % period:
        raise ValueError(f"{cycles} cycles is not a whole number of {period}-cycle periods")
    data = np.load(path)
    time = data["time"]
    period_time = drive_period(time, data["drive_phase"])
    index, rel_bin = window_frames(time, data["drive_phase"], period_time,
                                   from_cycle, cycles)
    values = frame_quantities(data["positions"][index], data["velocities"][index],
                              data["diameters"], data["plate_z"][index].astype(np.float64))
    order = np.argsort(rel_bin)
    bins_per_period = PHASES * period
    result = {}
    for name in QUANTITIES:
        series = values[name][order]
        by_period = series.reshape(cycles // period, bins_per_period)
        change, change_se = trend(by_period.mean(axis=1))
        result[name] = {
            "mean": float(series.mean()),
            "profile": by_period.mean(axis=0).tolist(),
            "trend": change,
            "trend_se": change_se,
            "drifting": bool(abs(change) > t95(cycles // period - 2) * change_se),
        }
    return {
        "trajectory": str(path),
        "from_cycle": from_cycle,
        "cycles": cycles,
        "period": period,
        "drive_period_time": period_time,
        "particle_count": int(data["diameters"].size),
        "quantities": result,
        "plate_contact_phases": crossings(np.array(result["plate_contact"]["profile"]),
                                          CONTACT_THRESHOLD),
    }


def compare(a: dict, b: dict) -> dict[str, dict[str, float]]:
    if a["period"] != b["period"]:
        raise ValueError("measurements use different response periods")
    period = a["period"]
    out = {}
    for name in QUANTITIES:
        pa = np.array(a["quantities"][name]["profile"])
        pb = np.array(b["quantities"][name]["profile"])
        shifts = [np.abs(pa - np.roll(pb, s * PHASES)).max() for s in range(period)]
        best = int(np.argmin(shifts))
        scale = max(np.abs(pa).max(), np.abs(pb).max())
        out[name] = {
            "mean_a": a["quantities"][name]["mean"],
            "mean_b": b["quantities"][name]["mean"],
            "mean_difference": b["quantities"][name]["mean"] - a["quantities"][name]["mean"],
            "max_profile_difference": float(shifts[best]),
            "relative_to_profile_max": float(shifts[best] / scale) if scale else 0.0,
            "cycle_shift": best,
        }
    return out


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="command", required=True)
    m = sub.add_parser("measure", help="bulk quantities of one trajectory")
    m.add_argument("trajectory", type=Path)
    m.add_argument("--from-cycle", type=int, required=True)
    m.add_argument("--cycles", type=int, required=True)
    m.add_argument("--period", type=int, default=2)
    m.add_argument("--out", type=Path, required=True)
    c = sub.add_parser("compare", help="compare two measurements")
    c.add_argument("a", type=Path)
    c.add_argument("b", type=Path)
    args = ap.parse_args(argv)

    if args.command == "measure":
        result = measure(args.trajectory, args.from_cycle, args.cycles, args.period)
        args.out.write_text(json.dumps(result, indent=1) + "\n")
        for name in QUANTITIES:
            q = result["quantities"][name]
            flag = "  DRIFTING" if q["drifting"] else ""
            print(f"{name:16s} mean {q['mean']:10.4f}   change over window "
                  f"{q['trend']:+.4f} +/- {q['trend_se']:.4f}{flag}")
        print("plate contact:", result["plate_contact_phases"])
        return
    a = json.loads(args.a.read_text())
    b = json.loads(args.b.read_text())
    print(f"{'quantity':16s} {'mean A':>10s} {'mean B':>10s} {'B - A':>10s} "
          f"{'max diff':>10s} {'rel':>6s} shift")
    for name, row in compare(a, b).items():
        print(f"{name:16s} {row['mean_a']:10.4f} {row['mean_b']:10.4f} "
              f"{row['mean_difference']:+10.4f} {row['max_profile_difference']:10.4f} "
              f"{row['relative_to_profile_max']:6.3f} {row['cycle_shift']}")


if __name__ == "__main__":
    main()
