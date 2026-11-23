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
- 3380eb3: ride v2, sphere-on-sphere capture (D0059), capture booking in
  audited terms (D0060)
- 06be1f7: root-search iteration limit re-predicts instead of returning
  no-contact (D0061), counter C_ROOTLIM

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

## Status (Nov 23)

v2 built, frozen tests pass. E0093 (local, 20 cycles, 12 conditions):
sphere-on-sphere capture fired 0 times at every condition that ended
(once in the pre-fix build). Plate capture fires at depth 10 (45 at
Gamma 3.5 f* 0.3). Deep stalls remain (Gamma 3.5 f* 0.3 d15 cycle 1,
Gamma 5 f* 0.3 d15 cycle 3); four deep conditions neither ended nor
finished in 600 s. The method does not act where it is needed yet.

E0092 (v1 pilot, six jobs labelled E0091): all failed in 29 s on the
existing output folder. No data. B0006 resolved.

## Next

1. Collect E0094.
2. Find why sphere capture doesn't fire near stalls: log every
   free-on-riding contact (closing speed, normal z, plate acceleration)
   in a stalling run. Candidates: the bottom sphere of a pressed pair is
   not riding (its plate hits stay above 1e-4); closing speeds at
   sphere contacts stay above 1e-4; the contact is with a free sphere
   resting on a free sphere (no rider in the chain).
3. Audit residual 8e-8 at Gamma 5 f* 0.3 d5 cycle 17 (first build): check
   whether the snap term (EN_SNAP, unaudited) or a missed booking causes it.

## Jobs in flight

E0094 on Hatteras (ride v2 06be1f7, 120 cycles, seed 1, 2 CPU-h cap):
- 164936-164941: Gamma 5; f* 0.3 depths 5, 10, 15; f* 0.5 depths 5, 10, 15
- 164942-164947: Gamma 3.5; same order

E0092 jobs 164696-164701 (labelled E0091): failed, recorded, nothing to
collect.
