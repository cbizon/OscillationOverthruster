# Option four from the paper: a design for resting contacts in a vibrated layer

Line L0009, written Nov 24, 2026, for the Nov 23 instruction. This is a design written out on paper only:
no code was changed and nothing was run. The paper is González, Risso and
Soto, "Extended event driven molecular dynamics for simulating dense
granular matter" (arXiv 1012.4844, Eur. Phys. J. Special Topics 179, 33,
2009). It was read tonight in the ar5iv version.

The base model is the 1998 model, and nothing in this design changes it:
- normal restitution e(v) = 1 − 0.3 v^0.75 below v = 1 √(gD), and 0.7 above;
- Walton's tangential rule: sliding friction with coefficient 0.5, capped at the rolling limit with tangential restitution 0.35;
- a sinusoidal plate, and side walls that do not move.

## 1. The paper's method, and what clusterlifter kept of it

In the paper a sphere is either **normal**, meaning it flies and collides as an ordinary
hard sphere, or **frozen**, meaning it does not move at all relative to the ground. Tonight's checklist splits the method into seven elements:

| Element of the paper | In clusterlifter? |
|---|---|
| A frozen state: the sphere does not move relative to the ground | **No.** A "held" sphere keeps flying freely, and is pushed every 0.0005 time units. |
| Frozen spheres are not integrated, which is where the paper's speed comes from | **No.** Held spheres need more work than free ones: a push every step, solved jointly over the whole cluster. |
| Freeze test: on hitting a frozen sphere, moving down, slower than at its last such hit, and below a sleep speed | **Partly.** It captures below a speed of 0.01 (the paper's range), but tests only the approach speed. It has no "moving down" or "slowing" test. It also captures pairs of free spheres at 1e-10. |
| A slow hit on a frozen sphere treated as a hit on an infinite mass, with restitution 0.4 | **No.** The hitter joins the held cluster and the joint solver handles it. |
| A fast hit wakes the frozen sphere | **Yes.** A hit faster than 0.01 releases all of that sphere's holds. |
| A periodic check (every 0.1) that a frozen sphere's supporters are still there | **Partly, but it means something else.** Every push step checks whether each contact's push has fallen to zero. That is a force-sign test every 0.0005, not a supporter check. |
| The energy removed at freezing is stored and returned if the sphere wakes early | **No.** Energy removed by the push steps is booked as a new term and never returned. |

Decision D0049 replaced the paper's resting state with periodic pushes, solved jointly by an iterative solver. In effect it bolted a time-stepped contact solver onto the event-driven engine, and that is where it left the paper. The cost was:
- a time step and five more numerical constants that the paper does not have: the solver's sweep limit, its over-relaxation and stopping rule, a release gap, and a capture speed for free pairs;
- a little energy removed at every step, so the energy audit failed in every deep Gamma 5 cycle, at about 1e-4;
- overlaps once friction was added, which brought in an overlap tolerance;
- none of the paper's speed-up, because held spheres were never left alone.

## 2. The design: three states

The design keeps the paper's idea that a sphere can be at rest and not integrated. It changes only what a vibrating plate and friction force it to change. Each change is numbered as a departure (**P1** to **P7**) or an addition (**A1** to **A3**). All motion below is in the **plate frame**: the frame that moves up and down with the plate. In that frame, gravity is replaced by the **effective gravity** g + a_p(t), where a_p(t) is the plate's acceleration. It pushes down as long as the plate's upward acceleration is greater than −g.

- **Free.** The sphere flies and collides by the base model, unchanged.
- **Riding.** The sphere is in a *lasting contact*, meaning one whose speed of approach has been brought to zero and is kept at zero. The contact is with the plate or with a still sphere (defined next). Motion along the contact surface continues.
  - *On the plate*, the sphere's height is exactly the plate's height plus its radius. Its horizontal motion is in closed form: it slides against friction until it rolls, then rolls at a constant velocity. The friction force is 0.5 times the contact force, and the contact force is the mass times g + a_p(t). Both the plate's motion and these integrals are known exactly, so nothing is stepped.
  - *On a still sphere*, the rider rolls or slides over the surface of that sphere. That sphere is fixed in the plate frame, so this is motion on a fixed ball under the effective gravity. It has no closed form, so it is integrated numerically to round-off accuracy. That calculation also gives the contact force at every moment. **This is the only place the design integrates anything (A1).**
- **Still.** This is the paper's frozen state, made relative to the plate (**P1**). A still sphere moves rigidly with the plate and has zero spin. Nothing about it is integrated. No collisions are predicted between two still spheres, or between a still sphere and the plate, because their distances never change. Only collisions with free or riding spheres are predicted. Those follow the plate's sine curve, using the root search the engine already has for the plate.

**Becoming still (P2, replaces the paper's freeze test).** A riding sphere becomes still when two conditions hold:
1. Its speed relative to the plate frame, including how fast its surface slips at each contact, is below the rest speed V_rest.
2. Its lasting contacts can hold it still: there are pushing contact forces, with friction no larger than 0.5 times each contact's force, that balance its own weight in both force and twisting. This is the **balance test**.

Because every force scales with the effective gravity, the balance test depends only on where the contacts sit, not on the phase of the plate.
- One supporter directly underneath passes. One supporter off to the side fails, because nothing stops the sphere from rolling off.
- Several contacts are not required, but they often pass. A sphere sitting in the groove between two spheres passes.
- The paper's "moving down" and "slower than last time" tests are dropped. The balance test does their job.
- The paper's "halfway to the next collision" placement is dropped (**P3**). A still sphere stays exactly where it is, touching its supporters.

**Capture (P4, replaces the paper's restitution of 0.4 on frozen spheres).** A free sphere becomes riding when it hits the plate or a still sphere with an approach speed below V_rest.
- The capture is the base model's collision with the normal restitution set to zero.
- The tangential part is Walton's rule unchanged, with the struck sphere as an immovable object moving with the plate. This is the rule the engine already uses for the walls.
- A restitution of zero is where the base model's own bounces end up. As the bounces shrink they converge to contact in finite time, and every bit of the approach energy is lost along the way. Capture removes the same energy at once, instead of over millions of events.

**Fast hits (P5, the paper's wake).** A sphere hit faster than V_wake becomes free with its current velocity and spin, and then the ordinary base-model collision happens. Every sphere it touched is checked again at once (see Collapse). The default is V_wake = V_rest. Then every hit on a resting sphere is either a capture or a wake, and the paper's infinite-mass bounce with restitution 0.4 is never needed. It is dropped (**P6**).

**Supporter check (P7, replaces the periodic check).** A resting sphere's supporters can only change at known events: a wake, the plate's release time, or a rider's contact force reaching zero. So the check happens at those events, not every 0.1. The paper's 1.05-diameter search distance is dropped too. Contacts are known exactly because each one was made by a capture.

### Stacks that last but are not stable

A sphere that lands slowly on a still sphere, off to one side, is captured and becomes riding. It does not become still, because it fails the balance test. It stays in contact for as long as the contact force is positive, rolling or sliding over its supporter.
- It rolls without slipping while the friction it needs stays below 0.5 times the contact force. Otherwise it slides, with friction equal to 0.5 times the contact force.
- On a fixed ball, rolling speeds up at 1/1.4 of the effective gravity's downhill part. The 0.4 here is the base model's moment-of-inertia factor.
- A slow touch on a second still sphere adds a second contact, and the sphere is put through the balance test again. It may become still there, for example in a groove.

So a pair or column can last a long time without being stable, and it ends by the physics: the rider rolls off. **A2** is the friction rule at a lasting contact (sliding at 0.5 times the force, then rolling). It is the limit of Walton's rule over a sequence of ever smaller impacts. Each impact slides or hits the rolling limit, and the rolling limit reverses the slip at 0.35 of its value, so the slip shrinks to zero.

Restriction for the first build (**A3**): only the plate and still spheres can carry riders. A sphere that lands slowly on a *riding* sphere is not captured. It bounces by the base model (question 1 below).

### Collapse

Nothing moves by fiat at collapse. Each sphere leaves with the position, velocity and spin it has at that instant.
- **The plate drops away.** At the closed-form time when the plate's acceleration falls to −g, every contact force in a chain resting on the plate reaches zero together. All still spheres and all riders on the plate become free. Still spheres leave with the plate's velocity and zero spin, and riders with their own velocity and spin. Neighbours leave touching, at the same velocity and under the same gravity, so their gaps stay at zero and nothing is predicted between them. A rider on a curved supporter may leave earlier, when its own contact force reaches zero.
- **A supporter leaves (a fast hit wakes it).** Each sphere that touched it is checked again at once:
  - still with the contacts it has left if it passes the balance test;
  - riding if any of its remaining contacts still carries a positive force;
  - free otherwise.
  This is a cascade and can spread up a column within the same instant.
- **A sphere rolls off.** The integration of its motion on the supporter shows the contact force reaching zero. It becomes free at that point, touching but separating.
- **A fast hit.** As above: the struck sphere becomes free with its current state, and then the ordinary collision happens.

### Energy

The paper's store-and-return of energy is **dropped**. Returning stored energy is a gain, and the audit would rightly report it as energy injected. The base model's own bounce sequence never gives that energy back either. The paper needed the return to stop sleep–wake cycles from collapsing a region. Here, between a wake and a new capture there are only ordinary base-model collisions.

What the referee's energy audit will see:
- **At capture and at becoming still**, an ordinary dissipative collision, booked in the plate or pair collision losses. Capture removes at most half the mass times V_rest²; becoming still removes the remaining motion relative to the plate, which is also below V_rest.
- **While resting**, the plate does work on still and plate-riding spheres. That work is written down in closed form: the mass times g + a_p(t), times the plate's velocity, integrated. It matches their change in energy exactly, so the residual is at round-off. For riders on a still sphere, the contact force passes through to the plate and is booked as plate work, and slipping is booked as pair losses. The residual there is the integrator's error, which must be held far below the audit's tolerance of 1e-8.
- **At collapse**, nothing, because no velocities change.

Nothing removes energy step by step, unlike clusterlifter.

### Overlaps

The engine's 2e-8 overlap check stays as it is.
- Becoming still and collapse change no positions, so they cannot create an overlap.
- Still spheres keep fixed distances to each other and to the plate.
- Riders on the plate sit exactly at the plate's surface height.
- Capture changes only velocities, at a contact that has already been checked.

Overlaps could still appear in two places:
1. the numerical integration of a rider on a still sphere, if its error were allowed to approach 2e-8;
2. a collision missed by the root search against the sine curves of still and riding spheres. This is the same risk the plate already carries, and the check would catch it.

## 3. Parameters

| Added threshold or time | Paper's value | Here |
|---|---|---|
| Rest speed V_rest (capture, and the speed limit for becoming still) | V_sleep, 0.01 to 0.10 √(gd) in deposition, 0.05 in the drum | 0.01 √(gD); check 0.003 and 0.03 in the bulk-physics check |
| Wake speed V_wake | V_wakeup, 0.01 to 0.5 √(gd) | equal to V_rest |
| Restitution on frozen spheres | α_frozen = 0.4 | dropped |
| Check interval | τ_check = 0.1 √(d/g) | dropped (checks at events) |
| Support distance | 1.05 d | dropped (contacts are exact) |
| Energy storage time | 2 V_sleep / ((1 − α_frozen) g) | dropped |
| Elastic collisions below a small speed (the paper's regularisation) | V_c = 1e-4 √(gd) | not used; the base model's e(v) already goes to 1 |
| Integration accuracy for riders on spheres | none (the paper integrates nothing) | a numerical setting, not physics: tight enough that the audit residual stays below 1e-10 |

The balance test and the friction at contacts use the base model's 0.5, 0.35 and 0.4, with no new constants.

## 4. How this differs from L0019 (analytical motion, `method/ride`)

The ride method already moves spheres on the plate in closed form, using the plate's sine curve, and lets go at the time the plate's acceleration reaches −g. This design would reuse that machinery. There are three main differences:
1. **Ride locks a sphere on a sphere rigidly.** At capture, the rider takes its supporter's full velocity and keeps a fixed offset from it, even when the rider sits off to one side. A rider here rolls or slides off under the effective gravity, and becomes still only if it passes the balance test.
2. **Ride has no friction or spin rule while riding.** Here, friction at a lasting contact slides at 0.5 times the force until the sphere rolls, and still spheres have no spin.
3. **Ride lets go of a cluster only at the plate's release time, or when collisions knock it apart.** Here, a sphere also leaves when its own contact force reaches zero, and a fast hit sets off an immediate re-check of the spheres around the struck one.

## 5. Choices for Chris

1. **Riders on moving spheres.** The first build lets only the plate and still spheres carry a rider. A sphere landing slowly on a rolling sphere bounces by the base model, which could chatter. The alternative is to move a whole rolling stack together, which needs a small joint solver for the stack's contact forces. *Default: restrict first, and measure chatter on the replayed stalls.*
2. **One threshold or two.** Should the wake speed equal the rest speed (default), or be higher, as in the paper? With a higher wake speed, hits between the two speeds bounce off the resting sphere as if it were immovable.
3. **Rest speed.** Should it be 0.01 √(gD), the paper's deposition value (default), and is a check at 0.003 and 0.03 enough to show the results don't depend on it?
4. **Energy return.** Should the paper's store-and-return be dropped (default), given that it would show up in the audit as injected energy?
5. **Friction in the balance test.** Should a sphere count as able to rest with friction helping (0.5 times each contact's force; default), or only if frictionless contacts could hold it? The frictionless version is stricter and gives fewer still spheres.
