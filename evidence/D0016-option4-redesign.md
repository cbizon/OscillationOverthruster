# Option 4 redesign: one resting state, the plate as a supporter

Agent, 2026-11-09. Proposed (decision D0016, superseding D0015). Redesign
only, nothing built, per the instruction of 2026-11-09. It follows
`notes/contact-options.md`, González, Risso & Soto (2009) (read again tonight
from ar5iv, sections 2 to 4), and what plate-stick and the nudge taught us.

## The idea in one paragraph

Work in the plate's frame. There the plate is a fixed floor and gravity is
replaced by an effective gravity g_eff(t) = g + a_p(t) that points down
while the plate accelerates upward faster than -g and flips sign once per
cycle, at sin(ωt) = 1/Γ. That is the same situation as González's rotating
drum: walls fixed in the drum's frame, gravity rotating in it, and the wall
built from frozen particles that never wake. So the vibrated layer is the
drum with gravity that changes in magnitude instead of direction. A sphere
is **resting** when it is at rest in the plate frame and held up by
supporters, and the plate is just a supporter that never wakes. There is
no separate "stuck on the plate" state: plate-stick's stuck sphere is a
resting sphere whose only supporter is the plate.

## What González's drum does, and what we keep

From the paper (section 4, figures 6 and 7):

- A thin 3D drum, R = 25 d, 5 d thick, half filled; rotation by turning
  gravity at Ω = 0.075 √(g/d). The wall is frozen particles that never wake.
- V_sleep = 0.05, V_wakeup scanned over 0.01, 0.05, 0.25 and 0.5 √(gd);
  α_frozen = 0.4; τ_check = 0.1 √(d/g); a bulk regularisation (e = 1 below
  V_c = 1e-4 √(gd)).
- Validated against experiments (shear band, static region), not against
  plain EDMD. With V_wakeup = 0.05 no static region forms (over-fluidised);
  0.5 resembles the experiments. The authors say V_wakeup and α_frozen
  have no first-principles value yet.
- Deposition (section 3): mid-deposit packing fraction falls linearly with
  the threshold, φ = 0.640 − 0.11 V_t/√(gd), while cost grows as V_t^-1.2.
  Freezing one grain at a time without a fluid layer above (V_wakeup = ∞)
  gives 0.586, far below 0.640. **That is the paper's own evidence that
  over-aggressive freezing locks in voids.**
- The τ_check test: a frozen particle is re-tested every τ_check and woken
  if its supporters, frozen neighbours closer than 1.05 d below it **along
  gravity**, are gone.

What we keep: the state, the supporter test along gravity, a periodic
check, the thresholds as named settings, and the deposition result as the
test for voids. What we change: thresholds act on velocities relative to
the plate (the paper notes moving walls need this and doesn't do it), and
"along gravity" means along g_eff(t), which flips sign once per cycle.

## The resting state

- **free**: ballistic, as now.
- **resting**: at rest in the plate frame, z = z_p(t) + h, horizontal
  position fixed, v = (0, 0, v_p(t)), spin zero. Its supporters (the plate,
  or resting spheres touching it below along g_eff) are recorded at entry.

### Entering it (sleep)

At a collision between a free sphere i and the plate or a resting sphere j,
i goes to rest if all of these hold (each one a setting that can be turned
off):

- its speed relative to the plate is below **V_sleep**;
- it is moving toward its supporter along g_eff (González's "downward");
- its speed is lower than at its previous collision (González);
- g_eff > 0.

It rests at the contact point at the collision instant (contact is exact
here, so González's "halfway" placement isn't needed). The kinetic energy
it loses relative to the plate is booked as dissipation (EN_REST). Whether
it is stored and returned on an early wake (González) is a setting, off by
default: off is dissipative only.

### Leaving it (wake)

- **g_eff reaches zero** (sin(ωt) = 1/Γ): the supporter test along g_eff
  fails for every resting sphere at once, so the whole resting region
  leaves with the plate's velocity. This is the plate-stick release event,
  now a consequence of the supporter rule rather than a separate rule.
- **A supporter wakes**: dependents wake in a cascade (exact, event-driven).
- **A hit faster than V_wakeup** (relative to the plate) wakes the struck
  sphere; the binary collision with the paper's law follows.
- **Periodic check every τ_check** (setting; off by default): re-test each
  resting sphere's stability (below). González uses it to catch marginal
  freezes; here it is the hook for the stability test.

### A free sphere hitting a resting one, below V_wakeup

The resting sphere is part of the plate, so the collision is a plate
collision: infinite mass, the paper's restitution law and Walton friction,
at the resting sphere's surface. Setting: `rest_hit = plate_law` (default)
or `alpha_frozen` (González's constant 0.4, for the sensitivity check).
Either changes the collision model for these collisions, which is Chris's
call (DIRECTION.md); plate_law changes it least, because it is the law the
1998 model already applies to the plate.

## Chatter: reduce it to something integrable, don't eliminate it

The stalls are Zeno sequences: with e(v) = 1 − 0.3 v^0.75, e → 1 as v → 0,
so a pressed contact bounces forever at shrinking amplitude and the bounce
count diverges. The goal is not zero collisions in contact, but a finite,
resolvable number per contact that the engine integrates exactly, ending in
rest.

- Single sphere on a resting support, bouncing down from v0 to V_sleep:
  bounces n ≈ (1/0.225)(V_sleep^-0.75 − v0^-0.75). From v0 = 0.1 that is
  about 4,400 at V_sleep = 1e-4, 770 at 1e-3 and 115 at 1e-2. For
  comparison, the nudge does about 269 plate collisions per particle per
  cycle at case e.
- Above V_sleep every bounce is resolved with the paper's law, so the
  approach to rest is physical; only the infinite tail below V_sleep is
  replaced by its limit (rest), which removes at most ½ m V_sleep² per
  contact.
- So V_sleep sets the chatter that remains. It should be chosen where the
  bulk physics has stopped changing as V_sleep falls, and the plots that
  justify it go in the evidence: collision rate per particle per cycle,
  CPU per cycle, and the bulk quantities against V_sleep.

## What happens when a sphere is held up non-physically

- One supporter is enough to rest (González). A sphere resting on one
  supporter at an angle above the friction angle (about 27 degrees at
  μ = 0.5) would roll or slide off. Resting, it is held in place until the
  next release, at most the part of one cycle while g_eff > 0.
- Consequences: (1) a void under or beside it stays open instead of
  filling, so the layer is less dense near the plate during contact;
  (2) spheres landing on it are stopped higher than they would be, so the
  centre of mass rides higher; (3) the layer dissipates less at landing (a
  locked arch is stiffer than a settling pile), which can shift the
  take-off phase; (4) it lasts at most one cycle, because the release
  dissolves the whole resting region every cycle. Errors are therefore
  bounded per cycle but can bias every cycle the same way.
- Settings: `stability = one_supporter` (González) or `hull` (the centre's
  projection along g_eff must lie inside the hull of its contact points,
  the plate counting as one). With `hull`, an oblique sphere stays free and
  keeps bouncing, and may stall again. The count of resting spheres with
  one oblique supporter, and their angles, is recorded in either mode.

### How we'll see it: density against depth

- Measure the packing fraction against height above the plate, φ(z), in
  slabs 0.5 D thick, averaged over many cycles at fixed phases (the phase
  of deepest compaction, the take-off phase, and the phase-0 checkpoint).
- Compare with freezing and without it, where without runs: the unmodified
  engine at the shallow 2D conditions and case g, the nudge everywhere, and
  the C code at Γ = 3.5. Over-aggressive freezing shows as lower φ near the
  plate and a higher, smoother top, growing as V_sleep and V_wakeup rise.
- A deposition test with no vibration (Γ = 0, a fixed plate): rain spheres
  onto the plate and compare mid-deposit φ with González's 0.640 −
  0.11 V_t, and with the unmodified engine where it can finish.

## Every cutoff is a setting

| setting | default | range for sweeps |
| --- | --- | --- |
| V_sleep (relative to plate) | 1e-4 √(gD) | 1e-5, 1e-4, 1e-3, 1e-2 |
| V_wakeup (relative to plate) | 1e-2 √(gD) | 1e-3, 1e-2, 5e-2, 0.25, 0.5 |
| rest_hit | plate_law | plate_law, alpha_frozen (0.4) |
| stability | one_supporter | one_supporter, hull |
| tau_check | off | off, 0.1, 0.01 √(D/g) |
| store_energy (González) | off | off, on |
| slower_than_previous | on | on, off |
| downward_only | on | on, off |

All live in the engine's parameter array, are written to the checkpoint and
to the run summary, and have no hidden internal constants. V_sleep = 0
turns the method off; the engine must then be bit-identical to main (a
test, below).

## Sweeps

- **Intrinsic:** one setting at a time from the defaults, then V_sleep ×
  V_wakeup jointly (4 × 5) at a small set of conditions. Judged by the bulk
  quantities, φ(z), the collision rate and CPU per cycle, and survival.
  Acceptance bar 3 needs the bulk physics flat in V_sleep and V_wakeup over
  at least a factor of 10 each.
- **External:** the 12-point 2D grid at L = 100 (Γ 3.5, 5; f* 0.3, 0.5;
  depths 5, 10, 15), then 3D cases b and g and the Γ = 5 survival case,
  then 3D N = 60000. At each, the comparison is with the unmodified engine
  where it runs, the nudge where it doesn't, and the C code at Γ = 3.5.
- Seeds 1 to 3 everywhere, identical starts for every engine, 1000 cycles.

## Code versions and their tests

Each version is a commit on `method/persistent-contact`, branched from main
(not plate-stick: one state replaces stuck), and each passes the tests
before the next starts.

1. **v1, settings and bookkeeping only.** Parameter array entries, state
   and supporter arrays, checkpoint and summary fields; no behaviour.
   Tests: frozen referee tests; bit-identical trajectories to main at
   V_sleep = 0 on three 2D conditions, 50 cycles.
2. **v2, resting on the plate.** Sleep on the plate, ride, release at
   g_eff = 0, wake by fast hit. Tests: one sphere dropped on the plate
   against the closed form (capture time, ride, release phase); energy
   books balance to round-off with resting; frozen tests; V_sleep = 0
   identity. Referee: survival and bulk on the 2D grid (expected to match
   plate-stick: it fails at the pair, by design).
3. **v3, resting on resting spheres, one supporter.** Supporter lists,
   cascade wake, plate-law hits on resting spheres. Tests: a two-sphere
   vertical stack lands, rests, rides and releases together (closed form);
   an oblique pair (the E0026 geometry) comes to rest instead of stalling;
   replays of the five E0026 failures complete; energy books. Referee:
   survival on the 8 stalled 2D conditions, then all 12; bulk where a
   baseline exists; φ(z) against depth with and without.
4. **v4, stability and periodic check.** `hull` mode and τ_check. Tests: a
   sphere on one oblique supporter stays free under `hull`; a pile on a
   plate held at constant g_eff keeps its rest set under both modes; counts
   of single-supporter rests. Referee as v3, both modes.
5. **v5, options for sensitivity.** `alpha_frozen`, `store_energy`.
   Tests: stored energy is returned exactly on early wake, and never more
   than was removed. Referee: the intrinsic sweeps.
6. **Candidate.** Frozen tests, survival on the full grid and 3D cases,
   energy audit, bulk physics, φ(z), the sweeps; then Figure 1 once its
   spec is set.

## Decisions for Chris

1. One resting state with the plate as a supporter, release when g_eff
   reaches zero (replaces D0015's stuck + frozen states).
2. A slow hit on a resting sphere uses the plate's collision law
   (`plate_law`), with González's α_frozen as a sensitivity setting only.
3. One supporter is enough by default, with `hull` built and compared.
4. Defaults V_sleep 1e-4 and V_wakeup 1e-2 √(gD), all settings swept.
5. Dissipative by default (no stored energy returned), with González's
   storage as a setting.
