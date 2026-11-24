# L0019: Option four, analytical motion

## Question

A different option 4 which doesn't do this lifting thing but directly uses
the analytical solution of the ball's motion. (Chris, Nov 19 debrief.)

Parent: L0009 (option four, clusterlifter / held contact).

## Design

The clusterlifter (L0009, `method/held-contact`) handles lasting contacts by
periodic impulses: every dt_hold = 5e-4 time units, a projected
Gauss-Seidel solver pushes held pairs apart just enough to keep their normal
gap non-negative. This works (no stalls on the 2D grid, clean audit) but
introduces a time step (dt_hold), an iterative solver, and many small
impulse events per contact per cycle.

The analytical-motion method replaces all of that with closed-form
trajectories. A sphere in lasting contact with the plate follows
z(t) = A sin(omega t) + r, vz(t) = A omega cos(omega t) exactly, with no
impulse stream. It releases at the closed-form phase where the plate's
acceleration drops to minus g: sin(omega t) = 1/Gamma, computed once at
capture. For sphere-on-sphere contacts, the riding sphere is locked to a
fixed displacement from its supporter, so the whole cluster moves as a rigid
body with the plate and every sphere's trajectory is sinusoidal plus an
offset.

This is a direct extension of the plate-stick method (option 2,
`method/plate-stick`) to sphere-on-sphere contacts. Plate-stick failed
because it had no sphere-on-sphere handling: a free sphere pressed on a stuck
one would chatter indefinitely. The analytical method adds sphere capture.

### States

Each sphere is FREE (0), RIDING_PLATE (1), RIDING_SPHERE (2), or
RECENTLY_RELEASED (3).

A riding sphere has:
- Supporter: PLATE or a sphere index
- Offset: the 3D displacement from the supporter's center to this sphere's
  center, fixed at capture time (rigid-body coupling)
- Release time: the scheduled EV_RELEASE event time

### Capture

**On the plate** (at EV_PLATE): same conditions as plate-stick. Relative
approach speed below v_capture and the plate can support (a_plate > minus g).
Perfectly inelastic in z: vz set to v_plate, z snapped to z_plate + r.
Horizontal velocity and spin preserved.

**On a riding sphere** (at EV_PP): a collision with a RIDING sphere at
closing speed below v_capture, where the free sphere is approaching. The
capture is rigid: the free sphere's velocity is set to match the supporter's
velocity plus any tangential component along the contact surface that the
rigid offset allows. For v1, the simplest version: all three velocity
components matched to the supporter's (fully inelastic). The 3D offset from
supporter center to rider center is recorded and fixed.

Energy removed at capture is booked in EN_CAPTURE (always a loss).

### Analytical motion

- RIDING_PLATE: z(t) = A sin(omega t) + r, vz = A omega cos(omega t).
  Horizontal position and velocity evolve ballistically. Spin preserved.
- RIDING_SPHERE: position = supporter_position(t) + offset. The supporter
  chain resolves to the plate, so every riding sphere has a sinusoidal
  vertical trajectory plus a constant offset. Horizontal position is also
  locked to the supporter (rigid body).

Cell crossings for riding spheres are computed from the sinusoidal trajectory
(sin_cross, as in plate-stick).

### Release

**From plate**: at the closed-form time where sin(omega t) = 1/Gamma on an
upward crossing (a_plate drops to minus g). Scheduled as EV_RELEASE.

**From sphere**: same phase. In a rigid cluster on the plate, every sphere's
vertical constraint comes through the chain to the plate, and the contact
force on each pair has a vertical component proportional to (g + a_plate).
All contacts release at the same instant.

**Cascade**: on release, every sphere in the cluster becomes FREE with its
current velocity (which is the cluster's velocity at that moment). The
recently-released state (SK=3) and a post-release exclusion window (from
the jerk, as in plate-stick) prevent immediate recapture.

### Pair prediction for riding spheres

Pairs involving a riding sphere use a conservative stepping integrator
(like plate-stick's stuck_pair_root) because the trajectory is sinusoidal,
not quadratic. The relative horizontal motion within a rigid cluster is zero,
so pairs within the cluster are skipped.

### Differences from clusterlifter

| Aspect | Clusterlifter | Analytical ride |
| --- | --- | --- |
| Contact mechanism | Impulse every dt_hold (5e-4) | Exact trajectory, no impulse stream |
| Solver | PGS per cluster per step | None; positions are closed-form |
| Release detection | Impulse goes to zero | Scheduled at closed-form time |
| Accuracy | Approximate (dt_hold discretisation) | Exact (analytical) |
| Event types | EV_HOLD (periodic) | EV_RELEASE (one per capture) |
| Cluster coupling | Normal-only constraint, tangential free | Rigid body (v1) |
| Energy accounting | EN_HOLD residual per step | EN_CAPTURE at capture only |

### Implementation plan

- v1: plate ride only (rewrite of plate-stick with clean energy accounting).
  Tests: frozen referee tests pass, capture/ride/release on a single sphere,
  energy audit.
- v2: add sphere-on-sphere ride (rigid-body clusters). The pressed-pair
  stall case. Tests: v1 tests plus cluster capture/release, the 2D grid.
- v3 (if needed): sliding instead of rigid coupling, for cases where
  tangential motion matters.

### Parameters

- v_capture: closing speed threshold for capture. Same role as v_hold in the
  clusterlifter and v_stick in plate-stick. Default: 0.01 (same as
  clusterlifter's v_hold).
- No dt_hold, no PGS iterations, no gap constant, no over-relaxation. Fewer
  knobs than the clusterlifter.

## Branch

`method/ride`, worktree at `sequel-data/worktrees/ride`.

On Nov 23 the program ran on a Linux container where the Mac's branches
don't exist and the git remote is unreachable. The branch was recreated
from main (whose engine hasn't changed since the branch was cut), with v1's
`granular/` copied from the engine checkout in the Hatteras run folder of
A0098 (`program fetch A0098:engine/granular`).

Commits on this machine's `method/ride`:
- 4d6c4e0: ride v1, recovered (same files as the Mac's 0600773)
- 3380eb3: ride v2, sphere-on-sphere capture (D0059), capture booking (D0060)
- 06be1f7: root-search iteration limit re-predicts (D0061), counter C_ROOTLIM
- 7ae3349: plate captures booked once (3380eb3/06be1f7 booked them twice,
  D0063 corrects D0060); after_unstick capture snap booked in EN_SNAP.
  Motion identical to 06be1f7 (E0096).

The Mac's af09367/0600773 may still exist there; if both machines' branches
meet, this one descends from main 11e1590, not from af09367.

## How to test locally

The worktree can't `uv run` on its own (its research-programs path is
relative). Run frozen tests from inside the worktree with main's env:
`cd worktrees/ride && uv run --project ~/Projects/experiments/sequel python -c
"import sys; sys.path.insert(0,'.'); import pytest; sys.exit(pytest.main(['-q','referee/tests']))"`.
PYTHONPATH does not override the editable install. The referee's summary
doesn't report ride counters; read `sim.cnt` (C_CAPTURE, C_SCAPTURE,
C_RELEASE, C_CASCADE, C_ROOTLIM) from a direct `Simulation` run.
Hatteras commands must use `--outdir $ROBOROBO_OUT/run`.

## Status (Nov 24, all E0098 jobs collected)

E0098 (ride v2 7ae3349, 120 cycles, seed 1, 2 CPU-h cap, Hatteras) is
finished and its outcome written (supported; D0067 says how a cap stop is
read). Evidence: `evidence/E0098-results.json` (per-cycle counters of the
capped runs and of A0115 inside).

- Completed 120 cycles, audit clean every cycle, no slow episodes: all six
  Gamma 3.5 conditions, G5 f0.3 d15 (A0115), G5 f0.5 d5 (A0116). The
  unmodified engine does not complete G3.5 f0.3 d15 (time freezes in cycle 1)
  or G5 f0.3 d15. At G3.5 f0.5 d15 it DOES complete, slowly (2.9 CPU-h vs
  ride's 188 CPU-s); don't call that one a stall (checker, Nov 23 run 3).
- Stopped at the CPU cap (audit clean in every completed cycle):
  G5 f0.3 d5 after 52 (A0127), G5 f0.3 d10 after 48 (A0128), G5 f0.5 d10
  after 14 (A0129), G5 f0.5 d15 after 12 (A0130). E0094 twins identical.
- Why: the unfinished last cycle of each holds 74-99% of all the run's
  C_ROOTLIM hits (6.4-8.7 million, each 10000 iterations of
  `stuck_pair_root`), plus thousands to 259000 captures (churn: captured,
  knocked off, recaptured). Events per CPU-s 1700-11000 vs 72000-490000 in
  completed runs; root calls per event unchanged (~1.8), so each call got
  far more expensive. Tiny plate collisions zero everywhere. G5 f0.3 d5's
  stuck cycle sits at phase 0.940-0.943 (unmodified engine overlapped there
  in cycle 49) and does have tiny pair collisions (up to 25714 per episode).
  Not yet shown: how many steps non-limit root calls take (no counter), and
  which pairs (rider-rider, rider-free) hit the limit.
- Cumulative counters exist per cycle in each artifact's
  `out/run/counters_by_cycle.jsonl` (fetch it: `program fetch A0129:out/run/counters_by_cycle.jsonl`);
  checkpoints every 10 cycles in `out/run/checkpoint.npz`.
- Hatteras and this machine don't follow the same trajectory (unexplained);
  reproduce a Hatteras slow-down from its checkpoint (`--input`), not by
  rerunning.

## Next

1. Wait for Chris (questions in `sessions/2026-11-24-L0019.json`): root
   search first, or bulk check at the eight completed conditions first.
2. Root search: add counters (total iterations, limit hits by pair kind:
   riding-riding, riding-free) on method/ride, check the frozen tests and
   that motion is unchanged, then run cycle 11 of G5 f0.5 d10 from A0129's
   checkpoint on Hatteras (`--input A0129:out/run/checkpoint.npz`, copy into
   the outdir, `--resume`). Likely fix: replace the fixed-safe-step search
   with a bracketing step on the sinusoid, or stop predicting pairs inside
   one rigid riding cluster (design says these should be skipped; check
   they are).
3. Bulk check (not asked yet) where the unmodified engine runs.
4. Run `program check` before every commit (D0065).

## Jobs in flight

None. All E0094 and E0098 jobs collected (A0115-A0130).
