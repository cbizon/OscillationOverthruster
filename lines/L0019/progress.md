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

## Status (Nov 23, run 3, jobs collected)

- E0098 (7ae3349, fixed audit, Hatteras), 8 of 12 ended (A0115-A0122):
  all completed 120 cycles, every cycle's audit clean (worst 2.8e-13, no
  gains, no slow episodes): Gamma 3.5 all six; Gamma 5 f* 0.3 d15; Gamma 5
  f* 0.5 d5. Evidence: `evidence/E0098-interim.json`.
- Still running, all past the unmodified stall cycle, clean so far:
  G5 f0.3 d5 (164950) at cycle 52, in slow episodes near phase 0.94, each
  50000-event chunk about 45 CPU-s; G5 f0.3 d10 (164951) at cycle 40;
  G5 f0.5 d10 (164954) and d15 (164955) at cycle 10. The last three record
  nothing between cycles unless a slow episode is open, so "no new cycle
  for 20-50 min" means either crawling just above the slow threshold or
  hung inside one `run_to` call. The referee checks the CPU cap only when
  `run_to` returns: a cap stop (outcome cpu_budget) means crawling; a Slurm
  TIMEOUT at 4 h with no cap stop means a hang.
- Every E0098 job matches its E0094 twin (06be1f7) cycle for cycle on
  Hatteras (energy change and events per particle), all 12 conditions. The
  E0094 twins started 40 min earlier and sit at the same cycles, so they
  show first how the four end (E0094 164936 was at 5550 of 7200 CPU-s at
  22:23 UTC).
- Scheduled releases: 0 in all eight finished runs (captures up to 1106 plate,
  47 sphere). The checker sampled 40 phases per cycle and found riders are
  knocked off quickly, not held through free flight.
- Hatteras and this machine don't follow the same trajectory (G5 f0.5 d10
  cycle 1: 298 vs 291 events per particle, same settings except run length
  and cap). Not explained. A Hatteras crawl can't be reproduced locally by
  rerunning; use a checkpoint (`--input`) instead.
- Earlier (run 2): audit fix verified (E0096), sphere capture fires at all
  six deep conditions (E0097), E0094's audit invalid, survival valid.

## Next

1. Collect the four E0098 jobs and the four E0094 twins. Write E0098's
   outcome (registration: falsified if v2 fails earlier than the unmodified
   engine where that engine completes 120 cycles (it didn't, at all 5), or any
   audit failure (none so far)). State how each cap stop or timeout is read.
2. If they crawl or hang at Gamma 5: diagnose on Hatteras from the cycle-50 /
   cycle-10 / cycle-40 checkpoint (`checkpoint.npz` in the run folder,
   `--input` of the ended artifact). C_ROOTLIM is large at Gamma 5 (326548
   at f* 0.3 d15): suspect the root-search re-predict path (D0061).
3. If E0098 is clean: bulk-physics check where the unmodified engine runs
   (not asked yet).
4. Run `program check` before every commit (checker, D0065).

## Jobs in flight

E0098 on Hatteras (ride v2 7ae3349, 120 cycles, seed 1, 2 CPU-h cap,
Slurm 4 h): 164950 (G5 f0.3 d5), 164951 (G5 f0.3 d10), 164954 (G5 f0.5
d10), 164955 (G5 f0.5 d15). Collected: 164952, 164953, 164957-164962.

E0094 still running (same motion, survival only): 164936 (G5 f0.3 d5),
164937 (G5 f0.3 d10), 164940 (G5 f0.5 d10), 164941 (G5 f0.5 d15).
