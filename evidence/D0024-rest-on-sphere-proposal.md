# Rest on a sphere under the normal rule: how tangential motion could be handled

Agent, 2026-11-12. Proposed (decision D0024), nothing built, as the Nov 12
instruction asked. It uses what tonight's runs showed (E0041 to E0045).

## What has to be handled

Measured at the first stall of the unmodified engine with friction, with every
velocity taken at the event time (E0043, `evidence/E0043-results.json`):

- sphere A is on the plate, with normal speed relative to the plate of about
  1e-11, rolling without slip (slip at the plate contact 1e-13 to 1e-10) at
  horizontal speeds from 0.03 to 0.65;
- sphere B is pressed on A from above, 22 to 61 degrees from vertical, with
  pair normal speed about 1e-11;
- in five of six pairs B is also in rolling contact with A (tangential surface
  speed about 1e-11); in one it slides on A at 0.06.

So both contacts carry tangential motion, and the pair's geometry changes
while the contact lasts: B moves around A.

## What tonight ruled in and out

- The plate contact under the normal rule is simple: A keeps its horizontal
  velocity and spin and rides the plate. For a sphere that rolls without slip
  this is exact with friction too, because the model has no rolling
  resistance.
- Any step that removes a fixed fraction of a pressed pair's energy makes the
  pair collapse. Friction does it in the paper's model (E0041, E0043). Waking
  A on every hit and recapturing it with zero restitution does it without
  friction (E0042). A rule for B on A must not add such a step in the hit path.

## Proposal: tangent-plane rest with re-capture

B goes to rest on A when their normal relative speed is below v_sleep and the
contact is pressed (the relative acceleration along the line of centres pushes
them together). Then:

1. **Normal part.** The normal relative velocity is set to zero by an impulse
   along the line of centres, shared by the masses (A held vertically by the
   plate if A rests on it). This removes at most m v_sleep^2 / 2 per capture
   and is booked as dissipation.
2. **Tangential part.** B keeps its tangential velocity and spin. While it
   rests, B moves in the plane tangent to A at the contact point, relative to
   A, under the tangential part of gravity in the plate's frame. In that frame
   A does not move vertically, so B's path has a closed form (a polynomial
   plus the plate's sine terms), and its events are found with the root
   search the engine already uses for resting pairs.
3. **Re-capture.** Moving in the tangent plane takes B off A's surface,
   outward, by (tangential distance)^2 / (2 (r_A + r_B)). The error is always
   a positive gap, never an overlap. When the gap reaches a set size the rest
   ends (a scheduled event, like the release at g_eff = 0), B is free, the
   pressing acceleration brings it back, and it is captured again with a new
   tangent plane. With the gap set to v_sleep^2 / (2 a), where a is the
   pressing acceleration, the re-capture speed stays below v_sleep.
4. **Wake.** As for the plate: release when the pressing acceleration changes
   sign (for the whole pile at g_eff = 0), a hit faster than v_wakeup, or the
   supporter waking.

Cost: a contact with tangential speed v_t is re-captured every
sqrt(2 (r_A + r_B) gap) / v_t. For v_sleep = 1e-2 and v_t = 0.1 that is a few
hundred events per contact per cycle; for v_sleep = 1e-4, tens of thousands.
It is the same trade as D0016's: a finite, resolvable number of events instead
of an endless sequence, set by v_sleep.

With friction (the target model), two more pieces are needed, in this order:

- the plate contact of a sphere that slips: Coulomb friction mu m g_eff(t)
  against the slip until it rolls, which has a closed form, then uniform
  rolling;
- the same for B on A: sliding friction along the tangent plane while B
  slips, rolling contact otherwise (five of the six stalled pairs).

## Alternatives

- **Rigid rest (D0016, v3):** B stops relative to A. Only acceptable when the
  tangential speed is also below v_sleep; the stalled pairs move at 0.03 to
  0.65, so it does not reach them (E0039).
- **Exact constrained motion:** B moves on the sphere of radius r_A + r_B
  about A, a pendulum equation with time-dependent gravity. No closed form;
  every prediction would integrate an ordinary differential equation.
- **Leave B free and make the hit on A lossless (the held slow hit, E0045):**
  no collapse is added, and without friction nothing collapses anyway. With
  friction B still collapses onto A through the tangential loss, so this does
  not remove the stall in the target model.

## What I would test first

Frictionless, 2D, the E0042 failure case (Gamma 3.5, f* 0.3, depth 15,
v_sleep 1e-3), where the wake variant collapses in cycle 6: tangent-plane rest
should run it with a finite event count and balanced books. Then the seven
stalled conditions with friction.
