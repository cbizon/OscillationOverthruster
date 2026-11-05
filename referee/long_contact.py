"""Long-contact test of an engine: survival, energy audit, and bulk quantities.

Runs one condition for a number of drive cycles with the engine in
``--engine`` (a checkout of sequel, usually a method branch's worktree; the
referee script itself always comes from the program branch) and records:

- **Survival.** The run goes on until it completes its cycles; nothing
  stops it for being slow.  It ends early only when:
  - the engine raises on a non-physical state (an overlap, a sphere below
    the plate, a plate contact off the surface, an unbracketed plate root):
    recorded as ``physical_failure`` with the message, then raised;
  - it reaches ``--max-cpu-hours`` (``cpu_budget``);
  - simulated time is frozen: a chunk of ``CHUNK`` events per particle
    advances it by exactly zero (``frozen_time``), so the run can never
    move again.
  Slow stretches are recorded, not stopped: a slow episode starts when a
  chunk advances time by less than ``SLOW_TIME_FRACTION`` of a drive
  period and ends when one advances it by more.  Each episode records
  where it started (cycle and phase), the slowest advance per event, how
  many events and how much CPU it took, and where it ended, or that it was
  still going when the run stopped.  Whether these resting-contact
  episodes clear on their own, and how long they take, is part of what
  the test measures (Chris, Nov 5: see what can be done without a stall
  detector).  The first landing of a deep layer is dense but not slow by
  this measure (about 1e-3 of a period per chunk, against about 1e-7 in a
  resting-contact episode).
- **Energy audit, per cycle.** The layer's change in energy (kinetic,
  rotational, gravitational, from snapshots) must equal the plate's work
  plus the dissipation of every collision, each measured in the frame where
  it can only lose energy (``granular/edmd.py``, ``run_events``).  The
  residual is energy the contact handling added or removed without
  accounting for it.  Also checked: vertical momentum against plate and
  wall impulses and gravity, and that no collision gained energy in its
  own frame.  A cycle passes when the energy residual is below
  ``AUDIT_REL_TOL`` of the cycle's energy throughput (the sum of the
  magnitudes of the accounted terms), the momentum residual below
  ``AUDIT_REL_TOL`` of the plate's impulse plus gravity's, and there is no
  gain.  The unmodified engine balances to about 1e-12.
- **Bulk quantities, every frame** (32 per cycle), saved to
  ``quantities.npz`` for ``referee/bulk.py measure``.

Checkpoints every ``--checkpoint-every`` cycles (skipped while a slow
episode is open); ``--resume`` continues from the latest one.
``summary.json`` is also rewritten every ``PROGRESS_SECONDS`` during a slow
episode, so a long one can be watched.

Usage::

    uv run python referee/long_contact.py --engine ~/Projects/experiments/sequel \\
        --dim 2 --gamma 3.5 --fstar 0.3 --N 500 --L 100 --depth 5 \\
        --cycles 1020 --outdir ~/Projects/experiments/sequel-data/runs/E0001/g3.5-f0.3-d5
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

AUDIT_REL_TOL = 1e-8
CHUNK = 100                     # events per particle between progress checks
SLOW_TIME_FRACTION = 1e-6       # of a drive period per chunk: a slow episode
PROGRESS_SECONDS = 300
PHASES = 32
HERE = Path(__file__).resolve().parent


def load_bulk():
    spec = importlib.util.spec_from_file_location("bulk", HERE / "bulk.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def engine_provenance(engine: Path) -> dict[str, object]:
    def git(*args):
        return subprocess.run(["git", "-C", str(engine), *args], check=True,
                              capture_output=True, text=True).stdout.strip()
    return {"path": str(engine), "commit": git("rev-parse", "HEAD"),
            "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
            "dirty": bool(git("status", "--porcelain", "--", "granular"))}


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--engine", type=Path, required=True,
                    help="sequel checkout whose granular package is tested")
    ap.add_argument("--dim", type=int, choices=(2, 3), required=True)
    ap.add_argument("--gamma", type=float, required=True)
    ap.add_argument("--fstar", type=float, required=True)
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--L", type=float, required=True)
    ap.add_argument("--depth", type=float, default=None,
                    help="default 5.42 in 3D, N/L in 2D")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--cycles", type=int, required=True)
    ap.add_argument("--checkpoint-every", type=int, default=10)
    ap.add_argument("--max-cpu-hours", type=float, default=40.0,
                    help="stop at this much CPU (budgets.yaml per_run_cpu_hours)")
    ap.add_argument("--outdir", type=Path, required=True)
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args(argv)

    engine = args.engine.expanduser().resolve()
    sys.path.insert(0, str(engine))
    from granular import edmd as K
    from granular.sim import Simulation
    import granular
    if Path(granular.__file__).resolve().parent != engine / "granular":
        raise RuntimeError(f"imported granular from {granular.__file__}, not {engine}")
    bulk = load_bulk()

    depth = args.depth if args.depth is not None else (
        5.42 if args.dim == 3 else args.N / args.L)
    outdir = args.outdir.expanduser().resolve()
    checkpoint = outdir / "checkpoint.npz"
    sim = Simulation(args.N, args.L, args.gamma, args.fstar, depth, args.seed,
                     dim=args.dim)
    names = bulk.QUANTITIES
    series = {name: [] for name in names}
    times, phases, audit, episodes = [], [], [], []
    wall_before = cpu_before = 0.0
    if args.resume and checkpoint.exists():
        sim.load_checkpoint(str(checkpoint))
        saved = np.load(outdir / "quantities.npz")
        keep = int(np.count_nonzero(saved["time"] <= sim.cycle * sim.T + 1e-9 * sim.T))
        times, phases = list(saved["time"][:keep]), list(saved["drive_phase"][:keep])
        series = {name: list(saved[name][:keep]) for name in names}
        audit = [row for row in json.loads((outdir / "audit.json").read_text())
                 if row["cycle"] <= sim.cycle]
        previous = json.loads((outdir / "summary.json").read_text())
        wall_before, cpu_before = previous["wall_seconds"], previous["cpu_seconds"]
        episodes = [ep for ep in previous["slow_episodes"]
                    if ep.get("end_cycle") is not None and ep["end_cycle"] < sim.cycle]
    else:
        outdir.mkdir(parents=True, exist_ok=False)

    started = time.time()
    cpu_started = time.process_time()

    def cpu_seconds():
        return cpu_before + time.process_time() - cpu_started

    def now_phase():
        return float((sim.ev_t[sim.tree[1]] / sim.T) % 1.0)

    def record_frame(phase_index):
        r, v, w = sim.snapshot()
        plate_z, _ = sim.plate(sim.t_local)
        values = bulk.frame_quantities(r[None], v[None], sim.diam,
                                       np.array([plate_z]))
        for name in names:
            series[name].append(float(values[name][0]))
        times.append(sim.cycle * sim.T + sim.t_local)
        phases.append(phase_index / PHASES)

    def save(status):
        tmp = outdir / "quantities.tmp.npz"
        np.savez(tmp, time=np.array(times), drive_phase=np.array(phases),
                 particle_count=sim.N,
                 **{name: np.array(series[name]) for name in names})
        os.replace(tmp, outdir / "quantities.npz")
        (outdir / "audit.json").write_text(json.dumps(audit, indent=0) + "\n")
        summary = dict(
            engine=engine_provenance(engine), dim=args.dim, gamma=args.gamma,
            f_star=args.fstar, particle_count=args.N, width=args.L, depth=depth,
            seed=args.seed, cycles_requested=args.cycles,
            chunk_events_per_particle=CHUNK, slow_time_fraction=SLOW_TIME_FRACTION,
            max_cpu_hours=args.max_cpu_hours, audit_rel_tol=AUDIT_REL_TOL,
            **status,
            cycles_completed=sim.cycle,
            slow_episodes=[{k: v for k, v in ep.items() if k != "cnt0"}
                           for ep in episodes],
            audit_failures=[row["cycle"] for row in audit if not row["passes"]],
            worst_energy_residual=max((abs(row["energy_residual_rel"]) for row in audit),
                                      default=0.0),
            worst_momentum_residual=max((abs(row["momentum_residual_rel"]) for row in audit),
                                        default=0.0),
            energy_gains=int(sim.cnt[K.C_EGAIN]),
            events_per_particle_cycle=(float(sim.cnt[K.C_EVENTS]) / sim.N / sim.cycle
                                       if sim.cycle else None),
            wall_seconds=wall_before + time.time() - started,
            cpu_seconds=cpu_seconds(),
        )
        (outdir / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
        return summary

    if not times:
        record_frame(0)
    chunk = CHUNK * sim.N
    episode = None
    last_progress_save = time.time()

    def close_episode():
        nonlocal episode
        d = sim.cnt - episode.pop("cnt0")
        episode["tiny_plate_collisions"] = int(d[K.C_TINYPL])
        episode["tiny_pair_collisions"] = int(d[K.C_TINYPP])
        episode["end_cycle"] = sim.cycle
        episode["end_phase"] = now_phase()
        episode = None

    def advance_to(target):
        """Run to target.  Returns None, or the reason the run must stop.
        A slow chunk opens or extends a slow episode; a normal one closes it."""
        nonlocal episode, last_progress_save
        while True:
            before = sim.ev_t[sim.tree[1]]
            cpu0 = cpu_seconds()
            try:
                hit_limit = sim.run_to(target, max_events=chunk)
            except (ValueError, RuntimeError) as error:
                return {"outcome": "physical_failure", "error": str(error),
                        "error_type": type(error).__name__,
                        "failure_cycle": sim.cycle, "failure_phase": now_phase()}
            if cpu_seconds() > args.max_cpu_hours * 3600:
                return {"outcome": "cpu_budget"}
            if not hit_limit:
                if episode is not None:
                    close_episode()
                return None
            progress = float(sim.ev_t[sim.tree[1]] - before)
            if progress == 0.0:
                return {"outcome": "frozen_time", "frozen_cycle": sim.cycle,
                        "frozen_phase": now_phase()}
            if progress < SLOW_TIME_FRACTION * sim.T:
                if episode is None:
                    episode = {"start_cycle": sim.cycle, "start_phase": now_phase(),
                               "events": 0, "cpu_seconds": 0.0,
                               "slowest_advance_per_event": progress / chunk,
                               "cnt0": sim.cnt.copy()}
                    episodes.append(episode)
                episode["events"] += chunk
                episode["cpu_seconds"] += cpu_seconds() - cpu0
                episode["slowest_advance_per_event"] = min(
                    episode["slowest_advance_per_event"], progress / chunk)
                episode["reached_cycle"] = sim.cycle
                episode["reached_phase"] = now_phase()
                if time.time() - last_progress_save > PROGRESS_SECONDS:
                    save({"outcome": "running"})
                    last_progress_save = time.time()
            elif episode is not None:
                close_episode()

    stop = None
    while sim.cycle < args.cycles:
        energy0, momentum0 = sim.layer_energy()
        en0, cnt0 = sim.en.copy(), sim.cnt.copy()
        for k in range(1, PHASES + 1):
            stop = advance_to(sim.T * k / PHASES)
            if stop is not None:
                break
            if k < PHASES:
                record_frame(k)
        if stop is not None:
            break
        energy1, momentum1 = sim.layer_energy()
        d = sim.en - en0
        terms = [d[K.EN_PLATE_WORK], d[K.EN_PLATE_DISS], d[K.EN_PP_DISS], d[K.EN_WALL_DISS]]
        throughput = sum(abs(x) for x in terms)
        energy_residual = (energy1 - energy0) - sum(terms)
        gravity = sim.P[K.P_G] * sim.mass.sum() * sim.T
        momentum_residual = ((momentum1 - momentum0)
                             - (d[K.EN_PLATE_JZ] + d[K.EN_WALL_JZ] - gravity))
        momentum_scale = abs(d[K.EN_PLATE_JZ]) + gravity
        gains = int(sim.cnt[K.C_EGAIN] - cnt0[K.C_EGAIN])
        row = {
            "cycle": sim.cycle + 1,
            "energy_change": energy1 - energy0,
            "plate_work": d[K.EN_PLATE_WORK],
            "plate_dissipation": d[K.EN_PLATE_DISS],
            "pair_dissipation": d[K.EN_PP_DISS],
            "wall_dissipation": d[K.EN_WALL_DISS],
            "energy_residual_rel": energy_residual / throughput if throughput else 0.0,
            "momentum_residual_rel": momentum_residual / momentum_scale,
            "energy_gains": gains,
            "events_per_particle": float(sim.cnt[K.C_EVENTS] - cnt0[K.C_EVENTS]) / sim.N,
        }
        row["passes"] = bool(abs(row["energy_residual_rel"]) < AUDIT_REL_TOL
                             and abs(row["momentum_residual_rel"]) < AUDIT_REL_TOL
                             and gains == 0)
        audit.append({key: (float(v) if isinstance(v, np.floating) else v)
                      for key, v in row.items()})
        sim.end_cycle()
        record_frame(0)
        if (sim.cycle % args.checkpoint_every == 0 or sim.cycle == args.cycles) \
                and episode is None:
            sim.save_checkpoint(str(checkpoint))       # also re-sorts
            save({"outcome": "running"})
        else:
            sim.rebuild(sort=True)
    if episode is not None:
        episode.pop("cnt0", None)
        episode["end_cycle"] = None                    # still going
    status = stop if stop is not None else {"outcome": "completed"}
    summary = save(status)
    if status["outcome"] == "physical_failure":
        raise RuntimeError(f"non-physical state in cycle {sim.cycle + 1}: {status['error']}")
    outcome = {"completed": f"completed {summary['cycles_completed']} cycles",
               "cpu_budget": "stopped at the CPU budget after "
                             f"{summary['cycles_completed']} cycles",
               "frozen_time": f"time frozen in cycle {sim.cycle + 1}"}[status["outcome"]]
    audit_text = ("energy audit clean" if not summary["audit_failures"]
                  else f"energy audit failed in {len(summary['audit_failures'])} cycles")
    print(f"{outcome}; {len(episodes)} slow episodes; {audit_text} (worst residual "
          f"{summary['worst_energy_residual']:.1e}); "
          f"{summary['wall_seconds']:.0f} s -> {outdir}")


if __name__ == "__main__":
    main()
