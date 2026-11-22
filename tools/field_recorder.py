"""Run the referee's long_contact.py unchanged and record the layer's height
field at every frame the referee records (32 per cycle), to OUTDIR/fields.npz.

It does what lc_counters.py does (counters.json, SEQUEL_MU) and adds the
recorder.  The recorder only reads: it wraps the referee's
bulk.frame_quantities, which is handed the positions of every recorded frame,
and passes the call through.  Nothing in the engine, the referee or the run
is changed (checked in E0053: final checkpoints identical with and without).

Height field: mean particle height above the plate in bins of side 2 D (2D,
along x) or 2.5 D (3D, square), minus its mean; empty bins take the mean.
The same bins as pattern_id.py.

fields.npz:
  time[F]        absolute time of the frame (cycles * T + t_local)
  frame[F]       frame index within the cycle, 0..31
  var[F]         variance of the field (D^2)
  spec[F, K]     2D: variance carried by Fourier mode k = 1..K of the box
                 (a sine of amplitude a in mode k gives a^2 / 2), K = L / 8,
                 so wavelengths from L down to 8 D;
                 3D: the same summed over rings of |k| = 1..nb/2 (width one)
  field_time[G], field[G, nb] or field[G, nb, nb]
                 the field itself (float32) at the frames listed in
                 SEQUEL_FIELD_FRAMES (default 0,8,16,24: four per cycle)
  L, dim, nb, T  box width, dimension, bins per side, drive period

Resume: when the referee resumes from a checkpoint, frames later than the
checkpoint are dropped from an existing fields.npz, as the referee does with
its own series.  fields.npz is written whenever a checkpoint is, and at the
end of the run however it ends.

usage: field_recorder.py <long_contact.py arguments>"""
import importlib.util
import json
import os
import sys
from pathlib import Path

import numpy as np

REFEREE = Path(__file__).resolve().parent.parent / "referee/long_contact.py"
FRAMES_PER_CYCLE = 32


def height_field(x, y, z, L, dim):
    """Mean height per bin minus its mean; empty bins take the mean."""
    if dim == 2:
        nb = int(L // 2)
        ix = np.minimum((x / L * nb).astype(int), nb - 1)
        tot = np.bincount(ix, weights=z, minlength=nb)
        cnt = np.bincount(ix, minlength=nb)
    else:
        nb = int(L // 2.5)
        ix = np.minimum((x / L * nb).astype(int), nb - 1)
        iy = np.minimum((y / L * nb).astype(int), nb - 1)
        tot = np.bincount(ix * nb + iy, weights=z, minlength=nb * nb).reshape(nb, nb)
        cnt = np.bincount(ix * nb + iy, minlength=nb * nb).reshape(nb, nb)
    h = np.where(cnt > 0, tot / np.maximum(cnt, 1), np.nan)
    h = np.where(np.isnan(h), np.nanmean(h), h)
    return h - h.mean()


def spectrum(h, kmax=None):
    """Variance carried by each mode (2D) or ring (3D), k = 1..kmax."""
    nb = h.shape[0]
    if h.ndim == 1:
        P = 2.0 * np.abs(np.fft.rfft(h)) ** 2 / nb ** 2
        if nb % 2 == 0:
            P[-1] *= 0.5                      # Nyquist mode is its own conjugate
        kmax = kmax or nb // 2
        return P[1:kmax + 1]
    P = np.abs(np.fft.fft2(h)) ** 2 / nb ** 4
    f = np.fft.fftfreq(nb) * nb
    kx, ky = np.meshgrid(f, f, indexing="ij")
    ring = np.rint(np.hypot(kx, ky)).astype(int)
    kmax = kmax or nb // 2
    return np.bincount(ring.ravel(), weights=P.ravel(), minlength=kmax + 1)[1:kmax + 1]


def main(argv):
    engine = Path(argv[argv.index("--engine") + 1]).expanduser().resolve()
    outdir = Path(argv[argv.index("--outdir") + 1]).expanduser().resolve()
    sys.path.insert(0, str(engine))
    from granular import edmd as K
    from granular import sim as simmod

    ff = os.environ.get("SEQUEL_FIELD_FRAMES", "none")
    keep = [] if ff.lower() in ("", "none") else sorted(int(s) for s in ff.split(","))
    mu_override = os.environ.get("SEQUEL_MU")
    made = []
    rec = dict(time=[], frame=[], var=[], spec=[], field_time=[], field=[])
    state = dict(calls=0)
    _init = simmod.Simulation.__init__
    _save = simmod.Simulation.save_checkpoint
    _load = simmod.Simulation.load_checkpoint

    def write():
        if not made or not rec["time"]:
            return
        sim = made[-1]
        nb = int(sim.L // (2 if sim.dim == 2 else 2.5))
        tmp = outdir / "fields.tmp.npz"
        np.savez_compressed(
            tmp, time=np.array(rec["time"]), frame=np.array(rec["frame"], dtype=np.int8),
            var=np.array(rec["var"], dtype=np.float32),
            spec=np.array(rec["spec"], dtype=np.float32),
            field_time=np.array(rec["field_time"]),
            field=np.array(rec["field"], dtype=np.float32),
            L=sim.L, dim=sim.dim, nb=nb, T=sim.T, kept_frames=np.array(keep))
        os.replace(tmp, outdir / "fields.npz")

    def init(self, *a, **k):
        if mu_override is not None:
            k.setdefault("mu", float(mu_override))
        _init(self, *a, **k)
        made.append(self)

    def save_checkpoint(self, path):
        _save(self, path)
        write()

    def load_checkpoint(self, path):
        _load(self, path)
        p = outdir / "fields.npz"
        if p.exists():
            d = np.load(p)
            limit = self.cycle * self.T * (1 + 1e-9)
            n = int(np.count_nonzero(d["time"] <= limit))
            g = int(np.count_nonzero(d["field_time"] <= limit))
            rec["time"], rec["frame"] = list(d["time"][:n]), list(d["frame"][:n])
            rec["var"], rec["spec"] = list(d["var"][:n]), list(d["spec"][:n])
            rec["field_time"], rec["field"] = list(d["field_time"][:g]), list(d["field"][:g])

    simmod.Simulation.__init__ = init
    simmod.Simulation.save_checkpoint = save_checkpoint
    simmod.Simulation.load_checkpoint = load_checkpoint

    spec_ = importlib.util.spec_from_file_location("long_contact", REFEREE)
    lc = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(lc)
    _load_bulk = lc.load_bulk

    def load_bulk():
        bulk = _load_bulk()
        fq = bulk.frame_quantities

        def frame_quantities(r, v, diam, plate_z):
            sim = made[-1]
            state["calls"] += 1
            p = r[0]
            h = height_field(p[:, 0], p[:, 1], p[:, 2] - float(plate_z[0]), sim.L, sim.dim)
            nb = h.shape[0]
            frame = int(round(sim.t_local / sim.T * FRAMES_PER_CYCLE)) % FRAMES_PER_CYCLE
            t = sim.cycle * sim.T + sim.t_local
            rec["time"].append(t)
            rec["frame"].append(frame)
            rec["var"].append(float(h.var()))
            rec["spec"].append(spectrum(h, int(sim.L // 8) if sim.dim == 2 else nb // 2))
            if frame in keep:
                rec["field_time"].append(t)
                rec["field"].append(h.astype(np.float32))
            return fq(r, v, diam, plate_z)

        bulk.frame_quantities = frame_quantities
        return bulk

    lc.load_bulk = load_bulk
    try:
        lc.main(argv)
    finally:
        if made:
            sim = made[-1]
            write()
            names = {v: n for n, v in vars(K).items() if n.startswith("C_") and isinstance(v, int)}
            ennames = {v: n for n, v in vars(K).items() if n.startswith("EN_") and isinstance(v, int)}
            out = dict(cycle=int(sim.cycle), event_time=float(sim.ev_t[sim.tree[1]]),
                       counters={names.get(k, "c%d" % k): int(x) for k, x in enumerate(sim.cnt)},
                       energy_terms={ennames.get(k, "en%d" % k): float(x) for k, x in enumerate(sim.en)},
                       mu=float(sim.P[K.P_MU]), mu_override=mu_override,
                       field_recorder=dict(frames_recorded=len(rec["time"]),
                                           fields_kept=len(rec["field_time"]),
                                           recorder_calls=state["calls"], kept_frames=keep))
            (outdir / "counters.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main(sys.argv[1:])
