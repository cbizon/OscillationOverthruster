"""Run the 1998 C code in its 2D mode as the baseline for bulk-quantity checks.

The source is the corrected C tree the Figure 1 benchmark reference was made
from: the modern port of the 1998 code with the moving-plate spin-sign fix,
the fresh-run vertical velocity fix, and the instrumentation that writes
field times and plate velocities.  The patches are read from the benchmark
repository (``balls_56_independent/original``) and are not changed here.
Only compile-time parameters differ from the benchmark: the 2D mode
(``DIMENSION 2``, spheres confined to a plane), the box width and height,
the drive, the particle count and the seed.

The C code handles a sphere resting on the plate by snapping it onto the
plate surface after a plate hit; this is the baseline's contact handling.
It aborts when its plate root finder can't bracket a root.  An abort is
recorded, not hidden: the run's metadata says how many cycles completed and
the frames written before the abort are kept.  With several ``--seeds`` the
next seed is tried after an abort; every attempt is kept in its own
``seed-<n>`` folder and listed in ``summary.json``.

Output, in sequel units (lengths in D, time in sqrt(D/g)):

- ``trajectory.npz`` with the keys of ``granular/export.py``: ``time``,
  ``drive_phase``, ``positions``, ``velocities``, ``angular_velocities``,
  ``diameters``, ``plate_z``, ``plate_vz``.  In 2D the C code moves
  particles in its y-z plane and writes only (y, z) positions and velocities
  and the spin about x.  They are mapped to sequel's ``dim=2`` frame, where x
  is horizontal and y is frozen: sequel x = C y, sequel z = C z, sequel y =
  0, and, keeping the axes right-handed, sequel's spin about y = minus C's
  spin about x.
- ``run.json``: parameters, seed, source hashes, compiler, return code,
  completed cycles, elapsed time.

Usage::

    uv run python referee/c_baseline.py --gamma 3.5 --fstar 0.5 --depth 5 \\
        --width 100 --cycles 30 --seeds 16532 1 2 \\
        --outdir ~/Projects/experiments/sequel-data/c-baseline/g3.5-f0.5-d5
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import resource
import shutil
import stat
import subprocess
import time
from pathlib import Path

import numpy as np

BENCHMARK = Path.home() / "Projects/experiments/balls_56_independent/original"
PATCHES = (
    "physics-fixes/0001-fix-bottom-spin-normal.patch",
    "physics-fixes/0002-fix-random-initial-velocity.patch",
    "instrumentation/0001-write-field-time-and-plate-velocity.patch",
)
SOURCE_FILES = ("clist.c", "fel.c", "plist.c", "collide.c", "detect.c",
                "stat.c", "cell.cc", "files.c", "xmain.c")
C_DIAMETER = 0.95          # the C code's mean diameter; its cells are 1.0
PHASES_PER_CYCLE = 32
RUN_NAME = "base"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha256(directory: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in directory.rglob("*") if p.is_file()):
        digest.update(str(path.relative_to(directory)).encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def materialize_source(destination: Path) -> dict[str, str]:
    port = BENCHMARK / "modern-port"
    shutil.copytree(port, destination)
    for path in destination.rglob("*"):
        if path.is_file():
            path.chmod(path.stat().st_mode | stat.S_IWUSR)
    hashes = {"modern_port": tree_sha256(port)}
    for name in PATCHES:
        patch = BENCHMARK / name
        subprocess.run(["patch", "-p1", "-i", str(patch)], cwd=destination,
                       check=True, capture_output=True)
        hashes[name] = sha256(patch)
    return hashes


def _replace_define(text: str, name: str, value: str) -> str:
    pattern = re.compile(rf"^(?://)?#define[ \t]+{re.escape(name)}[ \t]+\S+(.*)$",
                         re.MULTILINE)
    text, count = pattern.subn(lambda m: f"#define {name} {value}{m.group(1)}",
                               text, count=1)
    if count != 1:
        raise ValueError(f"could not uniquely configure {name}")
    return text


def box_height_cells(gamma: float, f_star: float, depth: float) -> int:
    """Box height in C cells: room for the plate's full swing, the layer and
    its flight above the plate, with margin."""
    frequency = f_star / math.sqrt(depth * C_DIAMETER)       # C units
    amplitude = gamma / (2.0 * math.pi * frequency) ** 2      # C units
    return max(50, math.ceil(2.0 * amplitude + 4.0 * depth + 20.0))


def configure(source: Path, *, gamma: float, f_star: float, depth: float,
              n_particles: int, width_cells: int, height_cells: int,
              cycles: float, seed: int) -> float:
    max_particles = 1 << math.ceil(math.log2(n_particles + 16))
    values = {
        "RUN": json.dumps(RUN_NAME),
        "RANDOM": str(seed),
        "FREQUENCY": f"({f_star:.17g}/sqrt({depth:.17g}*0.95))",
        "NMOV": str(n_particles),
        "DIMENSION": "2",
        "START": "0",
        "OLDRUN": json.dumps("unused"),
        "STATS": str(PHASES_PER_CYCLE),
        "FIELDS": str(PHASES_PER_CYCLE),
        "QFLOATS": "0",
        "PDIAM": ".95",
        "PDISP": "0.01",
        "BSIZE": str(width_cells),
        "YBSIZE": str(width_cells),
        "ZBSIZE": str(height_cells),
        "G": "1.0",
        "GRAV": "1",
        "THERMAL": "0",
        "THERMAL2": "0",
        "THERMAL3": "0",
        "THERMAL4": "0",
        "WALLREST": "0.7",
        "BALLREST": "0.7",
        "ROTATIONS": "1",
        "BETA0BALL": ".35",
        "BETA0WALL": ".35",
        "BALLMU": "0.5",
        "WALLMU": "0.5",
        "GAMMASWEEP": "0",
        "GAMMA": f"{gamma:.17g}",
        "TFINAL": f"{cycles:.17g}",
        "PLATEMOVE": "1",
        "PERIODIC": "0",
        "PRESSURE": "0",
        "NP": str(max_particles),
        "NLEVELS": str(int(math.log2(max_particles)) - 1),
    }
    header = source / "main.h"
    text = header.read_text()
    for name, value in values.items():
        text = _replace_define(text, name, value)
    text, count = re.subn(r"^(?://)?#define[ \t]+GRAVDIM(?:[ \t]+.*)?$",
                          "//#define GRAVDIM 2", text, count=1,
                          flags=re.MULTILINE)
    if count != 1:
        raise ValueError("could not uniquely disable GRAVDIM")
    # DENSIFY's 2D packing puts the first row at z = 0.5, inside the plate's
    # swing, and 0.1 from the side wall; it was written for a container at
    # rest.  Without it, rows start above the plate's highest point, as in
    # 3D.  It is tested with #ifdef, so it has to be removed, not set to 0.
    text, count = re.subn(r"^#define[ \t]+DENSIFY\b.*$", "//#define DENSIFY 1",
                          text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise ValueError("could not uniquely disable DENSIFY")
    header.write_text(text)
    return f_star / math.sqrt(depth * C_DIAMETER)


def compile_source(source: Path) -> tuple[Path, str]:
    executable = source / "grains"
    built = subprocess.run(["g++", "-w", "-O2", "-std=gnu++17", *SOURCE_FILES,
                            "-lm", "-o", str(executable)],
                           cwd=source, text=True, capture_output=True)
    if built.returncode != 0:
        raise RuntimeError(f"C compile failed:\n{built.stdout}{built.stderr}")
    compiler = subprocess.run(["g++", "--version"], check=True,
                              capture_output=True, text=True).stdout.splitlines()[0]
    return executable, compiler


def _no_core_dumps() -> None:
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def run(executable: Path, run_dir: Path, timeout_seconds: float) -> tuple[int, float]:
    started = time.monotonic()
    with (run_dir / "run.log").open("w") as log:
        process = subprocess.Popen([str(executable)], cwd=run_dir, stdout=log,
                                   stderr=subprocess.STDOUT,
                                   preexec_fn=_no_core_dumps)
        try:
            return_code = process.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            raise
    return return_code, time.monotonic() - started


def read_frames(run_dir: Path, n_particles: int) -> dict[str, np.ndarray]:
    def output(suffix: str) -> Path:
        return run_dir / f"{RUN_NAME}.{suffix}"

    def per_particle(suffix: str, components: int) -> np.ndarray:
        values = np.fromfile(output(suffix), dtype="<f4")
        record = n_particles * components
        complete = values.size // record          # an abort can cut the last one
        return values[:complete * record].reshape(complete, n_particles, components)

    frames = {
        "positions": per_particle("pos", 2),           # (y, z)
        "velocities": per_particle("vel", 2),          # (vy, vz)
        "angular_velocities": per_particle("ome", 1),  # spin about x
        "plate_z": np.fromfile(output("plate"), dtype="<f4"),
        "plate_vz": np.fromfile(output("platevel"), dtype="<f8"),
        "raw_time": np.fromfile(output("fieldtime"), dtype="<f8"),
    }
    count = min(len(value) for value in frames.values())
    frames = {key: value[:count] for key, value in frames.items()}
    frames["diameters"] = np.fromfile(output("balls"), dtype="<f8")
    if frames["diameters"].size != n_particles:
        raise ValueError(f"{output('balls')} has {frames['diameters'].size} "
                         f"diameters, expected {n_particles}")
    return frames


def to_sequel_units(frames: dict[str, np.ndarray], frequency: float) -> dict[str, np.ndarray]:
    length = C_DIAMETER
    time_unit = math.sqrt(C_DIAMETER)          # g = 1 in both codes
    speed = math.sqrt(C_DIAMETER)
    phase = np.mod(frames["raw_time"] * frequency, 1.0)
    phase[np.isclose(phase, 1.0, atol=1e-7)] = 0.0

    def planar(values: np.ndarray, scale: float) -> np.ndarray:
        out = np.zeros((*values.shape[:2], 3), dtype=np.float32)
        out[:, :, 0] = values[:, :, 0] * scale      # C y -> sequel x
        out[:, :, 2] = values[:, :, 1] * scale      # C z -> sequel z
        return out

    spin = np.zeros((*frames["angular_velocities"].shape[:2], 3), dtype=np.float32)
    spin[:, :, 1] = -frames["angular_velocities"][:, :, 0] * time_unit
    return {
        "time": frames["raw_time"] / time_unit,
        "drive_phase": phase,
        "positions": planar(frames["positions"], 1.0 / length),
        "velocities": planar(frames["velocities"], 1.0 / speed),
        "angular_velocities": spin,
        "diameters": frames["diameters"] / length,
        "plate_z": (frames["plate_z"] / length).astype(np.float32),
        "plate_vz": (frames["plate_vz"] / speed).astype(np.float32),
    }


def run_point(args: argparse.Namespace, seed: int, outdir: Path) -> dict[str, object]:
    """Build, run and export one seed; returns the run's metadata."""
    outdir.mkdir(parents=True, exist_ok=False)
    width_cells = round(args.width * C_DIAMETER)
    n_particles = round(args.depth * args.width)
    height_cells = box_height_cells(args.gamma, args.fstar, args.depth)

    source = outdir / "src"
    hashes = materialize_source(source)
    frequency = configure(source, gamma=args.gamma, f_star=args.fstar,
                          depth=args.depth, n_particles=n_particles,
                          width_cells=width_cells, height_cells=height_cells,
                          cycles=args.cycles, seed=seed)
    executable, compiler = compile_source(source)
    run_dir = outdir / "run"
    run_dir.mkdir()
    return_code, elapsed = run(executable, run_dir, args.timeout_hours * 3600)

    frames = read_frames(run_dir, n_particles)
    trajectory = to_sequel_units(frames, frequency)
    np.savez(outdir / "trajectory.npz", **trajectory)
    completed_cycles = (float(frames["raw_time"][-1] * frequency)
                        if frames["raw_time"].size else 0.0)
    log_tail = (run_dir / "run.log").read_text(errors="replace").splitlines()[-5:]
    meta = dict(
        model="1998 C code, 2D mode (spheres confined to a plane), snap contact",
        gamma=args.gamma, f_star=args.fstar, depth=args.depth,
        width=args.width, particle_count=n_particles,
        box_height=height_cells / C_DIAMETER, cycles_requested=args.cycles,
        seed=seed, return_code=return_code,
        completed=bool(return_code == 0
                       and completed_cycles >= args.cycles - 1e-6),
        completed_cycles=completed_cycles, frames=int(frames["raw_time"].size),
        elapsed_seconds=elapsed, compiler=compiler, source_hashes=hashes,
        log_tail=log_tail,
        trajectory_sha256=sha256(outdir / "trajectory.npz"),
    )
    (outdir / "run.json").write_text(json.dumps(meta, indent=1) + "\n")
    # The raw C outputs are large and fully represented in trajectory.npz.
    for suffix in ("pos", "vel", "ome", "restart"):
        (run_dir / f"{RUN_NAME}.{suffix}").unlink(missing_ok=True)
    return meta


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--gamma", type=float, required=True)
    ap.add_argument("--fstar", type=float, required=True)
    ap.add_argument("--depth", type=float, required=True,
                    help="particle layers, N D / width")
    ap.add_argument("--width", type=float, default=100.0, help="box width in D")
    ap.add_argument("--cycles", type=float, required=True)
    ap.add_argument("--seeds", type=int, nargs="+", default=[16532],
                    help="tried in order until one completes; aborted "
                         "attempts are kept and recorded")
    ap.add_argument("--outdir", type=Path, required=True)
    ap.add_argument("--timeout-hours", type=float, default=12.0)
    args = ap.parse_args(argv)

    width_cells = round(args.width * C_DIAMETER)
    if not math.isclose(width_cells / C_DIAMETER, args.width, rel_tol=1e-9):
        raise ValueError(f"width {args.width} D is not a whole number of C cells "
                         f"({args.width * C_DIAMETER:g}); use a multiple of 20 D")
    outdir = args.outdir.expanduser().resolve()
    outdir.mkdir(parents=True, exist_ok=False)
    attempts = []
    for seed in args.seeds:
        meta = run_point(args, seed, outdir / f"seed-{seed}")
        attempts.append({key: meta[key] for key in
                         ("seed", "completed", "completed_cycles", "return_code",
                          "elapsed_seconds")})
        status = ("completed" if meta["completed"]
                  else f"aborted (code {meta['return_code']})")
        print(f"seed {seed}: {status}, {meta['completed_cycles']:.2f} of "
              f"{args.cycles:g} cycles in {meta['elapsed_seconds']:.0f} s",
              flush=True)
        if meta["completed"]:
            break
    selected = next((a["seed"] for a in attempts if a["completed"]), None)
    summary = dict(gamma=args.gamma, f_star=args.fstar, depth=args.depth,
                   width=args.width, cycles=args.cycles,
                   selected_seed=selected, attempts=attempts)
    (outdir / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    if selected is None:
        print(f"no seed completed {args.cycles:g} cycles -> {outdir}")


if __name__ == "__main__":
    main()
