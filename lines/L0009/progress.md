# L0009 Option four — progress

## Current state (after the Nov 24 run, instruction of Nov 23)

**Clusterlifter (`method/held-contact`, tip 8f8f999) is stopped as built.**
Chris's instruction says: don't extend it, fix it, or run it. Its description
stays in `lines/L0009/clusterlifter.md`.

**The design that replaces it is in `lines/L0009/design.md`** (Nov 24). It is on paper only: no code and no runs.
- It follows González, Risso and Soto (arXiv 1012.4844), which was read tonight in its ar5iv version.
- It opens with a table: clusterlifter kept one of the paper's seven elements fully (wake on a fast hit), two partly, and four not at all.
- The design has three states:
  - **free**: the base model;
  - **riding**: a lasting contact whose approach speed is held at zero while the sphere slides or rolls along the surface. On the plate the motion is in closed form; on a still sphere it is integrated until the contact force reaches zero;
  - **still**: the paper's frozen state, made relative to the plate. The sphere moves with the plate, has no spin and is never integrated. A sphere enters it only if the balance test passes (friction-limited force and torque balance against its own weight).
- Capture is the base collision with normal restitution zero, with Walton's tangential rule unchanged.
- The paper's restitution on frozen spheres (0.4), its periodic check, its 1.05 d support distance and its energy store-and-return are all dropped.
- Departures are named P1 to P7 and additions A1 to A3.
- Five choices for Chris are at the end of the design, and proposed decision D0069 records the defaults.

## What's next

1. Wait for Chris's answers to the five choices (D0069).
2. Then the first build, on a new branch (for example `method/rest`) in `sequel-data/worktrees/`:
   - the plate part first, reusing the closed-form plate motion from L0019 `method/ride`, plus Coulomb sliding to rolling while riding;
   - frozen engine tests and the replayed stalls before the 2D grid.
3. Optional and cheap: run the balance test on its own over the Nov 16 and 17 stall snapshots (no engine runs).

## Jobs in flight

None.

## Background (older results, still valid)

- E0086 (clusterlifter v4, deep Gamma 5, collected Nov 23):
  - one completed 120 cycles, one hit frozen time at cycle 96, and two timed out;
  - the audit failed in nearly every cycle (worst 2.0e-4, energy removed and never injected).
- E0087: clusterlifter with friction set to zero passed the bulk check against a friction-zero baseline at Gamma 3.5, f* 0.3, depth 10.
- The overlap tolerance in v4 and v5 (1e-3 and 1e-6) has no decision record, and Chris rejects it. The new design keeps the engine's 2e-8 check unchanged.
