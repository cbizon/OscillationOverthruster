# Option 4 for a vibrated layer: a design for review

Agent, 2026-11-08. Proposed (decision D0015); nothing here is built. Option 4
is not approved, so this note is the default action for last session's first
question ("transitive sticking or option 4?"). It follows
`notes/contact-options.md` and González, Risso & Soto (2009) as summarised
there, and uses what plate-stick taught us.

## What plate-stick showed (E0022, E0026)

- Every plate-stick failure is a free sphere resting at an angle on a sphere
  stuck to the plate.
- E0026 replayed the failures with counters added. The pair collides every
  2.5e-12 time units, millions of times, and never separates. A collision
  between equal masses only cancels the approach speed. The stuck sphere's
  downward recoil is then absorbed when it is captured again. So the next
  contact is again a pressed contact, and the search steps twice
  (`stuck_pair_root`) to the next collision.
- Time is effectively frozen: a stall. Each of these tiny intervals moves the
  pair together by about one position rounding error, about 1.4e-15 D. After
  millions of them the overlap reaches the engine's 2e-8 limit. So the
  overlap comes from rounding inside a stall, not from the physics of the
  pair.
- The pair needs a state of its own: a sphere at rest on something that rides
  the plate. That is option 4's frozen sphere.

## The design

### States

- **free**: ballistic, as now.
- **stuck**: on the plate, as plate-stick (option 2).
- **frozen**: at rest relative to the plate, held up by one or more stuck or
  frozen supporters. It keeps a fixed offset from the plate. Its x and y are
  constant, z = z_p(t) + h, v = (0, 0, v_p(t)), and its spin is zero.

Stuck spheres become fully at rest relative to the plate too (x, y and spin
fixed), not vertical-only as in plate-stick's current default. A sphere
resting on another at an angle feels a sideways force. If its supporter
could slide, the pair would never be at rest.

### Freezing

- Checked at a collision between a free sphere i and a stuck or frozen
  sphere j.
- i freezes if all of these hold:
  - in the plate frame, its relative normal speed is below V_sleep;
  - it is moving downward relative to the plate;
  - its speed is lower than at its previous collision (González);
  - the plate acceleration is above -g (otherwise nothing is pressed).
- It freezes at the contact point, at the collision instant. González put
  frozen spheres halfway to the next collision, but there is no need here:
  contact is exact.
- The kinetic energy relative to the plate frame that freezing removes
  (translation and spin) is booked as dissipation (EN_FREEZE, like
  EN_CAPTURE). It is not stored and returned later, so nothing can be
  injected.

### A sphere hitting a frozen or stuck sphere

- A collision faster than V_wakeup wakes the frozen sphere. It becomes free
  with the plate's velocity, and the binary collision with the paper's law
  follows.
- A slower collision treats the frozen sphere as part of the plate: a rigid
  body of infinite mass, moving with the plate, with the paper's restitution
  law and friction, exactly as for a plate collision.
- This is what González's frozen particles do, with α_frozen replaced by the
  paper's law, which the 1998 model already applies to the plate.
- Plate-stick's D0009 rejected this as a change to the collision model. In
  this design the frozen sphere is part of the plate. Even so, it is Chris's
  decision.

### Waking

- **Release:** when a_p reaches -g (the plate-stick event), every stuck and
  frozen sphere leaves together with the plate's velocity. The resting column
  takes off as the layer does.
- **Supporter loss:** each frozen sphere keeps a list of its supporters (at
  most 2 in 2D, at most 6 in 3D). When a supporter wakes, its dependents wake
  in a cascade. This is exact and event-driven, and replaces González's
  periodic τ_check.
- **Fast hit:** as above.

### Stability

- González freezes a sphere on a single frozen supporter. A sphere at an
  angle on one sphere is not statically stable: it would roll or slide off.
- In plate-stick's failures the free sphere sits 0.4 to 0.9 D to the side,
  at 25 to 65 degrees from vertical. With friction 0.5, sliding starts above
  about 27 degrees.
- Two choices:
  1. **González:** one supporter is enough. A sphere is held at most until
     the next release, less than one cycle. Simple. It may freeze some
     spheres that would have rolled off.
  2. **Geometric:** freeze only if the sphere's centre lies above the convex
     hull of its contact points (the plate counts as a contact). A sphere on
     one oblique supporter then stays free, keeps rattling, and can stall
     again. That may still be rare enough to be fine.
- Recommendation: build 1, then count frozen spheres on a single supporter
  and their angles, and report how often 1 and 2 would differ.

### Parameters

- V_sleep: 1e-4 √(gD), the same as v_stick. The pilot also uses 1e-3.
- V_wakeup: 1e-2 √(gD).
- Results must be shown insensitive to both: acceptance bar 3 forbids tuned
  constants that the result depends on. The bulk check is run at two values
  of each.

## Engine changes (on `method/persistent-contact`, branched from plate-stick)

- A new state value (frozen), the plate offset h, and a supporter list per
  sphere.
- Frozen spheres move like stuck ones: `zmove` with an offset. Frozen and
  stuck pairs are never predicted (no relative motion).
- A collision with a frozen or stuck sphere below V_wakeup uses the plate
  operator (`collide_wall` with the frozen sphere's surface velocity).
  Otherwise it wakes the sphere and uses `collide_pp`.
- The release event frees every stuck and frozen sphere at once. The
  supporter cascade happens on wake.
- Energy books:
  - the plate's work on frozen spheres while they ride, as in `advance_s`;
  - freeze and capture losses;
  - impulses of collisions against frozen spheres, booked as plate work and
    impulse.

## Tests before the referee

- A two-sphere stack landing on the plate: capture, freeze, ride, and
  release together at a_p = -g, against the closed form.
- Energy books balance to round-off over a cycle with freezing.
- Frozen engine tests unchanged.
- Then the referee's long-contact test, survival first, on the stalled
  conditions.

## Decisions for Chris

1. Full rest relative to the plate (x, y and spin fixed) for stuck and frozen
   spheres, instead of vertical-only sticking.
2. A slow collision with a frozen sphere uses the plate's collision (infinite
   mass, the paper's law).
3. One supporter is enough to freeze (González), with the count reported.
4. V_sleep 1e-4 and V_wakeup 1e-2 √(gD), with a sensitivity check.
5. No stored energy returned on early wake: dissipative only.
