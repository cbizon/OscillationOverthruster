"""Write a cycle-0 start for referee/long_contact.py --resume (3D Figure 1
case b, or any condition), from one of two initial states:

  --vup FRAC      the engine's default start (fill 0.30, v_init 0.1) with
                  FRAC x the plate's peak speed (A omega) added to every
                  sphere's vertical velocity, so the first impact is gentler;
  --c-restart P   the 1998 C code's restart file P (reference bundle), with
                  every sphere advanced ballistically to the restart time,
                  converted to sequel units (lengths / 0.95, velocities
                  / sqrt(0.95), spins * sqrt(0.95)) and frame (z minus A minus
                  0.001/0.95: the C plate is z = A(1 + sin) + 0.001 raw).
                  The restart must be at plate phase 0.

usage: caseb_start.py ENGINE OUTDIR --gamma G --fstar F --N N --L L --seed S
                      (--vup FRAC | --c-restart PATH)

Writes checkpoint.npz at cycle 0 plus the empty quantities.npz, audit.json,
summary.json that --resume reads (same layout as soft_start.py).
"""
import argparse, json, math, sys
from pathlib import Path
import numpy as np

SEQ = Path(__file__).resolve().parent.parent

ap = argparse.ArgumentParser()
ap.add_argument("engine", type=Path); ap.add_argument("outdir", type=Path)
ap.add_argument("--gamma", type=float, required=True)
ap.add_argument("--fstar", type=float, required=True)
ap.add_argument("--N", type=int, required=True)
ap.add_argument("--L", type=float, required=True)
ap.add_argument("--depth", type=float, default=5.42)
ap.add_argument("--seed", type=int, required=True)
g = ap.add_mutually_exclusive_group(required=True)
g.add_argument("--vup", type=float)
g.add_argument("--c-restart", type=Path)
a, _unknown = ap.parse_known_args()
engine = a.engine.expanduser().resolve()
sys.path.insert(0, str(engine))
from granular.sim import Simulation
import granular
assert Path(granular.__file__).resolve().parent == engine / "granular"
sys.path.insert(0, str(SEQ / "referee"))
import bulk

sim = Simulation(a.N, a.L, a.gamma, a.fstar, a.depth, a.seed, dim=3)
N = sim.N
info = {}
if a.vup is not None:
    sim.S[:N, 5] += a.vup * sim.A * sim.om
    info = dict(kind="upward", vup_fraction=a.vup, vup=a.vup * sim.A * sim.om)
else:
    raw = a.c_restart.read_bytes()
    h = np.frombuffer(raw[:32], "<f8")
    assert int(h[0]) == N and h[1] == a.gamma, h
    G = float(h[3])
    dt_ = np.dtype([("diam", "<f8"), ("loc", "<f8", 3), ("vel", "<f8", 3), ("cell", "<i4", 3),
                    ("time", "<f8"), ("g", "<f8"), ("ome", "<f8", 3)])
    assert len(raw) == 32 + N * dt_.itemsize + 32
    c = np.frombuffer(raw[32:32 + N * dt_.itemsize], dt_)
    assert np.all(c["g"] == 1.0)
    cyc = G * float(h[2])
    assert abs(cyc - round(cyc)) < 1e-8, cyc          # plate phase 0
    dt = G - c["time"]
    loc = c["loc"] + c["vel"] * dt[:, None]
    vel = c["vel"].copy()
    loc[:, 2] -= 0.5 * dt ** 2; vel[:, 2] -= dt            # raw gravity 1
    s = 1.0 / 0.95; ts = math.sqrt(s)
    diam = c["diam"] * s
    sim.S[:N, 0:3] = loc * s
    sim.S[:N, 2] -= sim.A + 0.001 * s
    sim.S[:N, 3:6] = vel * ts
    sim.S[:N, 6] = 0.0
    sim.S[:N, 7] = 0.5 * diam
    sim.W[:] = c["ome"] / ts
    sim.diam = diam.copy(); sim.mass = diam ** 3; sim.pid = np.arange(N)
    sim.rmax = float(0.5 * diam.max())
    gap = sim.S[:N, 2] - sim.S[:N, 7]
    info = dict(kind="c_restart", path=str(a.c_restart), c_cycle=round(cyc), c_time=G,
                min_gap_to_plate=float(gap.min()), max_advance=float(dt.max()))
out = a.outdir.expanduser().resolve()
out.mkdir(parents=True, exist_ok=False)
sim.save_checkpoint(str(out / "checkpoint.npz"))
np.savez(out / "quantities.npz", time=np.zeros(0), drive_phase=np.zeros(0),
         particle_count=sim.N, **{q: np.zeros(0) for q in bulk.QUANTITIES})
(out / "audit.json").write_text("[]\n")
(out / "summary.json").write_text(json.dumps(dict(
    wall_seconds=0.0, cpu_seconds=0.0, slow_episodes=[], soft_start=info)) + "\n")
print(out, json.dumps(info))
