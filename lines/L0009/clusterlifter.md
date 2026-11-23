# Clusterlifter: what the code does

**Branch:** `method/held-contact`, tip commit **8f8f999** (v5).

This document describes v4 (commit **3983f59f**, the latest run on Hatteras, confirmed readable from artifact A0090) plus the two v5 changes described in D0055 (commit 8f8f999 not accessible from this environment). The code is in `granular/granular/edmd.py` and `granular/granular/sim.py`.

---

## 1. What it does, step by step

**Capture.** When an event fires:
- *Plate collision*: if the approaching sphere is slower than `v_hold = 1e-2 √(gD)` relative to the plate, it is captured (held on the plate).
- *Sphere–sphere collision*: if either sphere is already held AND the approach speed is below `v_hold`, OR if neither is held but the approach speed is below `HOLD_TINY = 1e-10 √(gD)`, the pair is captured as a held contact.
- *Side-wall collision*: if the approaching sphere is already held AND its approach speed is below `v_hold`, it is held on the wall.

After any capture, `hold_cluster_step` runs immediately at the capture time.

**Hold state.** Each sphere has an array of `KH = 8` contact slots (`HP[i,k]`), which hold partner indices: a sphere index, `HOLD_PLATE` (−2), or `HOLD_WALL0 − f` (−3 to −6 for the four walls). A sphere is in a hold when any slot is filled. Sphere–sphere holds are symmetric (`HP[i,k]=j` and `HP[j,m]=i`). The normal at capture is stored in `HN[i,k]`. The next-step time is `HT[i] = t + dt_hold`; the event queue fires `EV_HOLD` at that time.

**The hold step (hold_cluster_step).** On every `EV_HOLD`:
1. Walk the graph of sphere–sphere holds to find the connected cluster.
2. Advance all cluster members to `t` and build the constraint list (one entry per active hold contact).
3. Remove contacts already letting go: approach speed > `v_hold` for plate and wall holds; approach speed > `v_hold` OR gap > `gap_release = 1e-4 D` for sphere–sphere in `sphere` mode.
4. Warm-start impulses from the previous step (`HL[i,k]`).
5. Run projected Gauss-Seidel to find non-negative impulses along contact normals.
6. Remove contacts whose impulse settled to zero (the contact would need a pull).
7. Apply friction (if on) and re-predict all cluster members.

**Solver.** Each Gauss-Seidel sweep iterates over all constraints. For a plate contact, the required velocity `vreq` is the minimum needed to stay on or above the plate over the next `dt_hold`, sampled at 32 equally spaced times. For a wall contact, `vreq = −gap/dt_hold`. For a sphere–sphere contact in `sphere` mode, the minimum normal relative velocity to keep the pair's surface distance non-negative over `dt_hold` in free flight (`hold_pair_wreq`); in `fixed` mode, simply `−wn` (stop approach). The impulse update is:
`new = max(0, old + ω × m_eff × (v_req − v_current))` where `ω = 1.0` on sweep 0, `ω = 1.5` on sweeps 1–199. Convergence: stop when the maximum impulse correction is ≤ `1e-15 + 1e-8 × max(λ)`. Unconverged steps count in `C_HNOCONV` but are not fatal.

**Friction.** When `HPAR[H_FRICTION] > 0.5` (default: off), after the normal solve, friction impulses are applied to plate and wall contacts only — **not** sphere–sphere (D0053: sphere–sphere friction causes drift into already-touching neighbours, see below). The formula follows `collide_wall`: tangential surface velocity computed from translational and spin velocities; impulse = `K/(K+1) × (1 + e)_effective × |pn/m| × mu / |vs|`, capped at rolling limit `1 + beta0`. Spin is updated.

**Release.** A held contact ends when (a) its solved impulse is zero, (b) the approach speed exceeds `v_hold`, or (c) in `sphere` mode the gap exceeds `gap_release`. When a sphere is hit faster than `v_hold`, `hold_free` releases all its contacts at once — they become ordinary collisions.

**Events added.** One event type, `EV_HOLD`, fires at each sphere's next-step time `HT[i]`. Captured plate and sphere–sphere events still count as `C_PLATE` and `C_PP` in the collision counters.

**Energy accounting (v3+).** The hold step computes `net = KE_after − KE_before − vp × Σλ_plate`. This `net` goes into `EN_HOLD`, visible as a residual in the referee's energy audit (not hidden in `EN_PLATE_DISS` as in v2). `EN_PLATE_WORK` and `EN_PLATE_JZ` accumulate the plate's work and vertical impulse from hold steps. Steps where `net > 0` count in `C_HGAIN` and `EN_HOLD_GAINS`.

---

## 2. Deviations from the base model

| Deviation | Value | Introduced | Decision |
|---|---|---|---|
| `v_hold`: capture/release threshold | 1e-2 √(gD) | v1, 9860a26 | D0049 |
| `dt_hold`: hold-step interval | 5e-4 √(D/g) | v2, 9860a26 (changed from 1e-4) | D0050 |
| `gap_release`: sphere–sphere gap to release (sphere mode) | 1e-4 D | v1 | D0049 |
| `max_iterations`: Gauss-Seidel sweeps | 200 | v1 | D0049 |
| `HOLD_TINY`: free pairs below this speed captured | 1e-10 √(gD) | v3, df3f4dc | D0051 |
| Solver over-relaxation ω | 1.5 (sweep 1+) | v2, 9860a26 | D0050 |
| Solver stopping rule | max correction ≤ 1e-15 + 1e-8 × max λ | v2, 9860a26 | D0050 |
| Warm start (impulses from previous step) | Yes | v1 | D0049 |
| Sphere–sphere friction | Off (always) | v3, Nov 20 | D0053 |
| Post-hold-step prediction overlap tolerance (`htol`) | 1e-3 (v4), **1e-6 (v5)** | v4 (not in D0049–D0054) | **No decision record** |
| Hold energy in `EN_HOLD` (not `EN_PLATE_DISS`) | v3+ | v3, df3f4dc | see Nov 20 session |
| Gap limiter on friction impulses | Scans all particles; scales impulse to prevent drift | v5, 8f8f999 | D0055 |

**The overlap tolerance** (`htol`): when friction is on, `hold_cluster_step` calls `schedule` with `htol = 1e-3` (v4) or `htol = 1e-6` (v5) instead of the standard `PAIR_PENETRATION_TOL = 2e-8`. This was added in v4 to prevent the post-friction prediction from raising on pre-existing near-overlaps that friction's velocity change reveals. There is no decision record for introducing it. D0055 narrowed it from 1e-3 to 1e-6; the standard 2e-8 applies when friction is off. No completed run has used friction-on mode.

---

## 3. Runs

All runs are 2D, seed 1 unless noted, friction off, `sphere` mode unless noted.

| Exp. | Commit (mode) | Γ | f* | depth | N | L | seed | cycles | fric | pred tol (hold) | outcome | evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E0079 | 9860a26 (sphere) | 3.5 | 0.3–0.5 | 5–15 | 250–750 | 100 | 1 | 120–305 | off | 2e-8 | 6 of 17; Γ5 frozen-time; superseded | E0079-E0080-results.json |
| E0080 | 9860a26 (fixed) | 3.5 | 0.3–0.5 | 5–15 | 250–750 | 100 | 1 | 120–305 | off | 2e-8 | 6 of 17; Γ5 frozen-time; superseded | E0079-E0080-results.json |
| E0081 | df3f4dc (sphere) | 3.5–6 | 0.3–0.5 | 5–15 | 250–3000 | 100–400 | 1–3 | 120–305 | off | 2e-8 | 17 runs complete; Γ5 all complete, no slow episodes, clean audit (worst 1e-12) | E0081-E0082-results.json |
| E0082 | 1a0dcc4 (fixed) | 3.5–6 | 0.3–0.5 | 5–15 | 250–3000 | 100–400 | 1–3 | 120–305 | off | 2e-8 | 17 runs complete; similar to E0081 | E0081-E0082-results.json |
| E0083 | 3983f59f (sphere) | 5 | 0.3–0.5 | 10–15 | wrong N | 20 | 1 | 120 | off | 2e-8 | Abandoned: wrong width (20 instead of 100); 44.75 CPU-h wasted | — |
| E0086 | 3983f59f (sphere) | 5 | 0.3 | 10 | 1000 | 100 | 1 | 120 | off | 2e-8 | 110 cycles; TIMEOUT | E0086/deep-runs-results.json |
| E0086 | 3983f59f (sphere) | 5 | 0.3 | 15 | 1500 | 100 | 1 | 120 | off | 2e-8 | 95 cycles; frozen_time (cycle 96) | E0086/deep-runs-results.json |
| E0086 | 3983f59f (sphere) | 5 | 0.5 | 10 | 1000 | 100 | 1 | 120 | off | 2e-8 | 70 cycles; TIMEOUT | E0086/deep-runs-results.json |
| E0086 | 3983f59f (sphere) | 5 | 0.5 | 15 | 1500 | 100 | 1 | 120 | off | 2e-8 | 120 cycles; completed | E0086/deep-runs-results.json |
| E0087 | ee877c7 (sphere, mu=0) | 3.5 | 0.3 | 10 | 1000 | 100 | 1 | 120 | off | 2e-8 | Completed; bulk check passes (0.69 sd) | E0087-bulk-results.json |

**E0086 energy audit.** All four runs fail every cycle. No energy is injected (`energy_gains = 0` in every run). The residuals are all negative, with means of 2.5e-5 to 5.9e-5 and worst values of 8e-5 to 2e-4 (relative to cycle plate work). The failures arise because v4 books hold energy in `EN_HOLD` separately from `EN_PLATE_DISS`; the same hold energy fraction (~1e-4 at deep Γ=5) was present but invisible in v3 (absorbed into plate dissipation). The audit threshold is 1e-8.

**E0086 survival.** The clusterlifter avoids the unmodified engine's immediate stall at all four conditions (the unmodified engine stalls in cycles 1–2 at Γ=5). Two jobs timed out before 120 cycles (wall-time limit reached without a CPU cap). One ended in frozen time (cycle 96, Γ=5, f*=0.3, depth 15): the same failure mode that the unmodified engine shows, now delayed to cycle 96. One completed 120 cycles (Γ=5, f*=0.5, depth 15).
