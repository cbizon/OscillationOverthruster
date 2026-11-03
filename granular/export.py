"""Continue a run from a checkpoint for a number of forcing cycles and write
the normalized trajectory archive required by the submission contract.

Frames are recorded at 32 equal phase intervals per cycle, including the
initial frame (at the checkpoint, a complete-cycle boundary) and the final
endpoint.  Lengths are in units of the mean diameter D, time in sqrt(D/g),
velocities in sqrt(gD), angular velocities in sqrt(g/D); z points up and
z = 0 is the mean plate position (plate_z = A sin(omega t)).
"""

import argparse
import json
import os
import time

import numpy as np

from .runner import add_common, make_sim
from . import edmd as K

PHASES = 32


def main(argv=None):
    ap = argparse.ArgumentParser()
    add_common(ap)
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--export-cycles", type=int, required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)

    t0 = time.time()
    sim = make_sim(args)
    sim.load_checkpoint(args.checkpoint)
    ck = np.load(args.checkpoint)
    wall_before = float(ck["walltime"]) if "walltime" in ck.files else 0.0
    assert sim.t_local == 0.0
    start_cycle = sim.cycle
    ncyc = args.export_cycles
    F = PHASES * ncyc + 1
    N = sim.N
    time_a = np.zeros(F)
    phase_a = np.zeros(F)
    pos = np.zeros((F, N, 3))
    vel = np.zeros((F, N, 3))
    omg = np.zeros((F, N, 3))
    pz = np.zeros(F)
    pvz = np.zeros(F)
    coll = np.zeros((F - 1, 3), dtype=np.int64)

    def record(f, t_abs, t_loc, ph):
        r, v, w = sim.snapshot(original_order=True)
        pos[f] = r
        vel[f] = v
        omg[f] = w
        time_a[f] = t_abs
        phase_a[f] = ph
        z, vz = sim.plate(t_loc)
        pz[f] = z
        pvz[f] = vz

    record(0, start_cycle * sim.T, 0.0, 0.0)
    prev = sim.cnt.copy()
    f = 0
    for c in range(ncyc):
        for k in range(1, PHASES + 1):
            t_loc = sim.T * k / PHASES
            sim.run_to(t_loc)
            f += 1
            d = sim.cnt - prev
            prev = sim.cnt.copy()
            coll[f - 1] = (d[K.C_PP], d[K.C_WALL], d[K.C_PLATE])
            cyc_abs = sim.cycle + (1 if k == PHASES else 0)
            if k == PHASES:
                t_abs = cyc_abs * sim.T
                record(f, t_abs, t_loc, 0.0)
            else:
                t_abs = sim.cycle * sim.T + t_loc
                record(f, t_abs, t_loc, k / PHASES)
        sim.end_cycle()
        # same cycle-boundary procedure as the production run
        sim.rebuild(sort=True)
        print("exported cycle %d (%d/%d)  %.0fs" % (sim.cycle, c + 1, ncyc,
                                                   time.time() - t0), flush=True)
    wall_export = time.time() - t0
    diam = sim.diameters_original()
    tmp = args.out + ".tmp.npz"
    np.savez(tmp, time=time_a, drive_phase=phase_a, positions=pos,
             velocities=vel, angular_velocities=omg, diameters=diam,
             plate_z=pz, plate_vz=pvz, collision_counts=coll)
    os.replace(tmp, args.out)
    meta = dict(case=args.case, gamma=args.gamma, f_star=args.fstar,
                particle_count=N, box_width=args.L, box_height=args.box_height,
                seed=args.seed, start_cycle=start_cycle,
                simulation_cycle=sim.cycle, export_cycles=ncyc,
                walltime_seconds=wall_before + wall_export,
                walltime_before_export=wall_before, walltime_export=wall_export,
                A=sim.A, T=sim.T, omega=sim.om, frequency=sim.f,
                counters={n: int(sim.cnt[getattr(K, n)]) for n in
                          ("C_PP", "C_WALL", "C_PLATE", "C_CELL", "C_ADV",
                           "C_EVENTS", "C_TINYPP",
                           "C_TINYPL", "C_PPSKIP", "C_PLSKIP")})
    with open(args.out.replace(".npz", ".json"), "w") as fh:
        json.dump(meta, fh, indent=1)
    print("wrote", args.out, "simulation_cycle", sim.cycle)


if __name__ == "__main__":
    main()
