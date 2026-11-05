"""Production driver for one Figure-1 case.

Runs forcing cycles from the initial condition, re-sorting particles at every
cycle boundary, writing monitoring data (height maps at 8 phases per cycle and
per-phase layer statistics) and checkpoints.  A file STOP in the output
directory makes the run checkpoint and exit at the next cycle boundary.
"""

import argparse
import json
import math
import os
import time

import numpy as np

from .sim import Simulation
from . import edmd as K


def height_map(r, rad, L, nb=100, dim=3):
    """Top-surface height map: highest particle top (z + r) in each column.
    In 2D the map is a single row (a height profile along x)."""
    nby = nb if dim == 3 else 1
    ix = np.clip((r[:, 0] / L * nb).astype(np.int64), 0, nb - 1)
    iy = np.clip((r[:, 1] / L * nby).astype(np.int64), 0, nby - 1)
    hm = np.full((nby, nb), -np.inf)
    np.maximum.at(hm, (iy, ix), r[:, 2] + rad)
    bad = ~np.isfinite(hm)
    if bad.any():
        hm[bad] = np.min(hm[~bad])
    return hm


def layer_stats(r, zp):
    z = r[:, 2]
    q = np.percentile(z, [1, 5, 50, 95, 99])
    return [zp, float(z.mean()), *[float(x) for x in q]]


def make_sim(args):
    if args.depth is None:
        # 3D: the Figure 1 depth; 2D: number of particle layers, N D / L
        args.depth = 5.42 if args.dim == 3 else args.N / args.L
    return Simulation(args.N, args.L, args.gamma, args.fstar, args.depth,
                      args.seed, box_height=args.box_height,
                      mu=args.mu, eps=args.eps, alpha=args.alpha, v0=args.v0,
                      dim=args.dim)


def add_common(ap):
    ap.add_argument("--case", required=True)
    ap.add_argument("--gamma", type=float, required=True)
    ap.add_argument("--fstar", type=float, required=True)
    ap.add_argument("--N", type=int, default=60000)
    ap.add_argument("--L", type=float, default=100.0)
    ap.add_argument("--dim", type=int, choices=(2, 3), default=3)
    ap.add_argument("--depth", type=float, default=None,
                    help="layer depth for f*; default 5.42 in 3D, N/L in 2D")
    ap.add_argument("--seed", type=int, default=16532)
    ap.add_argument("--box-height", type=float, default=100.0)
    ap.add_argument("--mu", type=float, default=0.5)
    ap.add_argument("--eps", type=float, default=0.7)
    ap.add_argument("--alpha", type=float, default=0.75)
    ap.add_argument("--v0", type=float, default=1.0)


def main(argv=None):
    ap = argparse.ArgumentParser()
    add_common(ap)
    ap.add_argument("--cycles", type=int, required=True, help="total cycles")
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--ckpt-every", type=int, default=10)
    ap.add_argument("--keep-every", type=int, default=50)
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args(argv)

    os.makedirs(args.outdir, exist_ok=True)
    mapdir = os.path.join(args.outdir, "maps")
    os.makedirs(mapdir, exist_ok=True)
    log = open(os.path.join(args.outdir, "log.txt"), "a")

    def say(s):
        print(s, flush=True)
        log.write(s + "\n")
        log.flush()

    sim = make_sim(args)
    ck = os.path.join(args.outdir, "checkpoint.npz")
    wall0 = 0.0
    if args.resume and os.path.exists(ck):
        sim.load_checkpoint(ck)
        wall0 = float(np.load(ck)["walltime"]) if "walltime" in np.load(ck) else 0.0
        say("resumed at cycle %d (walltime so far %.0f s)" % (sim.cycle, wall0))
    else:
        with open(os.path.join(args.outdir, "config.json"), "w") as f:
            json.dump(dict(vars(args), A=sim.A, T=sim.T, omega=sim.om, f=sim.f,
                           nx=sim.nx, nz=sim.nz, hx=sim.hx, z0=sim.z0,
                           fill_fraction=sim.fill_fraction), f, indent=1)
    say("case %s %dD N=%d L=%g depth=%g Gamma=%g f*=%g A=%.6f T=%.6f omega=%.6f "
        "grid=%dx%dx%d"
        % (args.case, sim.dim, sim.N, sim.L, sim.depth, sim.gamma, sim.f_star,
           sim.A, sim.T, sim.om, sim.nx, sim.ny, sim.nz))
    t_run = time.time()

    def walltime():
        return wall0 + (time.time() - t_run)

    def checkpoint():
        sim.save_checkpoint(ck)
        # store walltime alongside (re-save small file)
        d = dict(np.load(ck))
        d["walltime"] = walltime()
        tmp = ck + ".tmp.npz"
        np.savez(tmp, **d)
        os.replace(tmp, ck)
        if sim.cycle % args.keep_every == 0:
            np.savez(os.path.join(args.outdir, "ckpt_%06d.npz" % sim.cycle), **d)

    nph = 32          # layer statistics at 32 phases per cycle
    nmap = 8          # height maps at 8 phases per cycle
    prev = sim.cnt.copy()
    while sim.cycle < args.cycles:
        if os.path.exists(os.path.join(args.outdir, "STOP")):
            say("STOP file found at cycle %d" % sim.cycle)
            break
        c0 = time.time()
        maps = []
        stats = []
        for k in range(1, nph + 1):
            sim.run_to(sim.T * k / nph)
            r, v, w = sim.snapshot()
            zp, vp = sim.plate(sim.t_local if k < nph else sim.T)
            stats.append(layer_stats(r, zp))
            if k % (nph // nmap) == 0:
                maps.append(height_map(r, sim.rad, sim.L, dim=sim.dim)
                            .astype(np.float16))
        d = sim.cnt - prev
        prev = sim.cnt.copy()
        diag = sim.diagnostics()
        sim.end_cycle()
        np.savez(os.path.join(mapdir, "c%05d.npz" % sim.cycle),
                 maps=np.array(maps), stats=np.array(stats, dtype=np.float32),
                 counts=d)
        dt = time.time() - c0
        say("cycle %5d ev/N=%5.0f pp=%9d wall=%7d plate=%8d cell=%7d adv=%8d "
            "tinypp=%d zmax=%.1f %.1fs %.2fMev/s wall=%.0fs"
            % (sim.cycle, d[K.C_EVENTS] / sim.N, d[K.C_PP], d[K.C_WALL],
               d[K.C_PLATE], d[K.C_CELL], d[K.C_ADV],
               d[K.C_TINYPP], diag["zmax"], dt,
               d[K.C_EVENTS] / dt / 1e6, walltime()))
        if sim.cycle % args.ckpt_every == 0:
            g, i, j, bad = sim.overlap_check()
            say("   check: min gap %.3e, bad %d, plate gap %.3e, box x[%.4f,%.4f] "
                "y[%.4f,%.4f]" % (g, bad, diag["gap_plate"], diag["xmin"],
                                  diag["xmax"], diag["ymin"], diag["ymax"]))
            checkpoint()
        else:
            sim.rebuild(sort=True)
    checkpoint()
    say("finished at cycle %d, walltime %.0f s" % (sim.cycle, walltime()))


if __name__ == "__main__":
    main()
