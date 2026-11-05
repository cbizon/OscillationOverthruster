# Resting-contact regularization options

Chris Bizon, 2026-11-03. Copied into the repository on 2026-11-05 from the
Claude Docs page of the same name, so sessions can read it; this copy is the
one to keep current.

Persistent contact (option 4) is the method that should win; options 1–3
are cheaper regularizations to measure it against, and option 5 is a
trigger, not a method.

## The problem

With the plate rebound floor removed, sequel stalls on sustained contact
against the plate. In a Γ = 5, f* = 0.44 run (N = 2400, L = 20 D), cycle 3
reached phase 0.88 with the plate accelerating upward at 3.4 g. One sphere
pressed against the plate, with a neighbour above it, then produced about 2
million events per 1e-8 time units.

- Relative normal speeds were about 1e-11 √(gD), so e(v) = 1 − 0.3 v^0.75
  was already 0.9999999983.
- Restitution is therefore not the cause. The physical state is lasting
  contact, which instantaneous binary collisions cannot represent: with
  e < 1 the bounces converge to sticking in finite time (a Zeno sequence),
  and with e ≈ 1 the sphere rattles indefinitely at shrinking amplitude.
- The 1998 C code fails in the same regime. It has no stuck state in the
  build used for the reference. It snaps each sphere onto the plate surface
  after a hit, solves for plate contacts to a 1e-9 time tolerance, and
  aborts when a sphere ends up more than 1e-2 D below the plate. Its Γ = 5
  reference run hit that abort in cycle 4–5 (particle 5400, 0.16 D below the
  plate), so the case-e reference covers only four unequilibrated cycles.

Each option below must let that run continue without injecting energy, or
say exactly how much it injects.

## Option 1: position nudge onto the plate (astra)

After every plate collision, put the sphere a fixed tiny distance above the
plate surface. This is what the astra-low engine does, and is the most
likely reason it got through case e with no velocity floor.

- **What astra does:** sets z to the plate surface plus one or two
  floating-point steps, `nextafter(surface + spacing(A + r))`, about
  1e-15 D (`granular/engine.py:342-345` in the astra trial). The 1998 C code
  does the same kind of thing at a coarser scale: it snaps z exactly onto
  the surface and steps contact times in 1e-9 increments.
- **Why it helps:** the sphere always leaves the plate with a strictly
  positive gap, so the next contact is a finite time away instead of zero
  or below the time resolution.
- **Energy:** it injects potential energy m g δ per plate hit. At
  δ = 1e-15 that is negligible; the concern is not the amount but that the
  regularization is set by the floating-point format rather than by physics.
- **It will eventually overlap spheres (Chris, 2026-11-05).** Moving a
  sphere up without moving anything else closes the gap to whatever rests
  on it. With a sphere above in lasting contact, repeated nudges eventually
  push the pair into overlap. There is no way around it: the nudge can at
  best postpone the failure, and sequel's fail-fast overlap check will
  catch it when it happens.
- **Open question:** astra-low still showed 269 plate collisions per
  particle per cycle in case e, about 15 times the other cases. The nudge
  keeps the run alive by letting the rattle continue at a manageable rate,
  not by removing it.
- **Effort:** a few lines in sequel. Useful mainly as a baseline: if a
  principled method gives the same layer dynamics, the rattle did not
  matter.

## Option 2: stuck state on the plate, captured by e = 0

Give a sphere touching the plate a third state besides flying and
colliding: riding with the plate. It enters that state through a perfectly
inelastic collision below a tiny speed, and leaves it at an analytically
known phase.

- **Capture:** a plate collision with relative normal speed below v_stick
  uses e = 0, and the sphere becomes stuck. Without the e = 0 step, capture
  would have to wait for a bounce sequence to converge, which never happens
  when e(v) → 1.
- **While stuck:** z = z_p(t) + r and v_z = v_p(t). The contact force
  m(g + a_p) stays non-negative as long as the plate acceleration
  a_p ≥ −g.
- **Release:** when a_p drops to −g, at plate phase where sin(ωt) = 1/Γ.
  That time is known in closed form, so it is an ordinary scheduled event.
- **Energy:** dissipative only. Each capture removes at most ½ m v_stick²
  of relative kinetic energy; nothing is added.
- **Modeling choices it forces:** whether a stuck sphere can slide or roll
  horizontally on the plate (friction), and what happens to a sphere
  resting on a stuck sphere. The stall above involved exactly that pair.
  Making stacks stick transitively (as the sonnet-5-max trial did) is a
  model change; leaving them free means the upper sphere still rattles.
- **Limit:** it fixes contact with the plate only. Lasting contacts between
  spheres inside a dense layer are untouched, which is why it is a stepping
  stone toward option 4 rather than an end point.
- **Effort:** moderate. One new event type (release), a state flag, and a
  plate-velocity substitution in prediction.

## Option 3: elastic window near zero speed

Set e = 1 for relative normal speeds below a small v_el, and keep the
paper's e(v) above it. Dissipation then cannot drive relative speeds much
below v_el, so a sphere in lasting contact keeps bouncing at a finite,
resolvable rate instead of a vanishing one.

- **Why it should break the stall:** in the plate frame, a sphere pressed
  on by effective gravity g + a_p bounces with period about 2v/(g + a_p).
  The stall happened because v had decayed to 1e-11. With the window, v
  stays near v_el: for v_el = 0.01 √(gD) and Γ = 5 the period is about
  3e-3 √(D/g), roughly 1,500 plate hits per contact per cycle. That is
  costly but finite. Not yet tested in sequel.
- **Energy:** nothing is injected. But up to ½ m v_el² per lasting contact
  is stored as micro-bouncing and never dissipated while it stays in the
  window. That is the same kind of stored energy as the soft-sphere spring
  problem, only far smaller (v_el² = 1e-4 against typical v² ≈ 1).
- **Discontinuity:** e jumps at v_el, from 1 − 0.3 v_el^0.75 (0.9905 at
  v_el = 0.01) to 1. A continuous variant, such as 1 − B (v − v_el)^0.75
  above the window, changes the paper's law slightly; which one to use is a
  choice to make explicitly.
- **Prior use:** two campaign trials had it. fable-5.1-max kept it as an
  unused fallback (`edmd.py:201-202`, v_min = 0.01). sonnet-5.5-max ran
  with it in production (`walton.py:15`, cutoff 0.03), together with a
  plate rebound floor.
- **Scope:** it applies to every collision type, so it also guards against
  inelastic collapse inside the layer, not only at the plate.
- **Effort:** one branch in the restitution function. The cheapest option
  to test.

## Option 4: persistent contact (the target)

Give the model a state for spheres in lasting contact, so the event-driven
engine stops simulating that contact as a stream of collisions. The method
to follow is [Extended event driven molecular dynamics for simulating dense
granular matter](https://arxiv.org/abs/1012.4844) by J. S. González, D.
Risso and R. Soto, Eur. Phys. J. Special Topics 179, 33 (2009). It comes
from Cordero's group in Santiago; Cordero is acknowledged, not an author.
No paper by Cordero himself on persistent contacts turned up in his group's
publication list.

What the paper does:

- Each particle is either normal (inelastic hard sphere dynamics) or
  frozen (no motion relative to a fixed ground). Only normal particles are
  integrated, which is where its large speedup comes from.
- **Freezing:** checked when a particle collides with a frozen one. It
  freezes if it is moving down, its speed is below V_sleep and lower than
  at its previous collision. One frozen supporter is enough; the freeze is
  placed halfway to the next would-be collision.
- **Waking:** a collision faster than V_wakeup wakes a frozen particle. A
  slower one is treated as hitting an infinite mass with restitution
  α_frozen. A periodic check every τ_check also wakes a particle whose
  supporters (within 1.05 d along gravity) are gone.
- **Energy:** freezing is inelastic. The kinetic energy removed is stored
  for about 2 V_sleep / ((1 − α_frozen) g) and returned if the particle
  wakes sooner, so nothing is injected beyond what was taken.
- **Parameters used:** V_sleep and V_wakeup from 0.01 to 0.10 √(gd) for
  deposition, 0.05 and 0.50 √(gd) for a rotating drum; α_frozen = 0.4;
  τ_check = 0.1 √(d/g). The authors say the choice of V_wakeup and
  α_frozen needs further work.
- **Scope:** 3D, frictionless spheres without rotation. Static floors are
  frozen particles that never wake; the drum rotates gravity, not the
  walls.

What we would have to add for a vibrated layer:

- Freeze relative to the plate, not a fixed ground: frozen particles
  co-move with the plate, and all thresholds use relative velocity (the
  paper notes this is required for moving walls but does not do it).
- Release on the plate's acceleration: the whole frozen column must leave
  when a_p falls below −g, which option 2 already provides.
- Friction and spin: the paper has neither, so the Walton operator needs a
  rule for collisions with frozen spheres and for their spin while frozen.
- A better stability test than "one frozen supporter", since in a vibrated
  layer the frozen region forms and dissolves every cycle.

## Option 5: cutoffs

A cutoff on its own is a trigger, not a method: it says when to intervene
but not what to do. It only becomes a regularization once an action is
attached, and then it turns into one of the options above.

- **The known pairing is the TC model** (Luding & McNamara, Granular
  Matter 1, 113 (1998)): if a particle collided less than t_c ago, the next
  collision uses e = 1. That is option 3 with a time trigger instead of a
  speed trigger.
- The 1998 C code has this as a compile-time option (`LUDING`), switched
  off in the reference build. The fable-5 trial used a variant with e = 0
  instead, which is dissipative.
- Other triggers (an event-rate limit, a minimum time between a particle's
  collisions) are useful as diagnostics: they detect where a run is about
  to stall. The action they trigger would be option 2, 3 or 4.

Recommendation: drop this as a separate option, and keep event-rate
counters as instrumentation for whichever option is chosen.

## Side by side

| Option | Energy | Lasting contacts handled | Free parameters | Effort in sequel |
| --- | --- | --- | --- | --- |
| 1. Position nudge | Injects m g δ per plate hit (δ ≈ 1e-15 D); eventually overlaps spheres | Plate only; rattle continues | δ (set by float precision) | A few lines |
| 2. Stuck on plate, e = 0 capture | Dissipative only | Plate only; stacks are a choice | v_stick | One event type + state flag |
| 3. Elastic window | None injected; ≤ ½ m v_el² stored per contact | All, by keeping speeds ≥ ~v_el | v_el (and continuity choice) | One branch |
| 4. Persistent contact | Dissipative; stored energy returned on early wake | All, as a frozen state | V_sleep, V_wakeup, α_frozen, τ_check | Largest: states, wake rules, plate frame, friction |
| 5. Cutoffs | Depends on the action attached | Trigger only | t_c or rate limit | Instrumentation |

Suggested order: 3 and 1 first as cheap baselines that show whether the
Γ = 5 run gets past cycle 3, then 2 as the plate-frame core of 4, then 4.

## Sources

- J. S. González, D. Risso, R. Soto, [Extended event driven molecular
  dynamics for simulating dense granular
  matter](https://arxiv.org/abs/1012.4844), Eur. Phys. J. Special Topics
  179, 33 (2009); read via
  [ar5iv](https://ar5iv.labs.arxiv.org/html/1012.4844). The published
  journal version was not opened.
- [P. Cordero group page, Universidad de
  Chile](https://www.cec.uchile.cl/cinetica/pcordero/RG.html), checked for
  other persistent-contact papers; none listed.
- S. Luding, S. McNamara, Granular Matter 1, 113 (1998): TC model, cited
  from the paper above, not opened.
- 1998 C code: `balls_56_independent/original/modern-port` (`collide.c`,
  `detect.c`), with reference build settings from
  `harness/balls_bench/historical.py`.
- Reference case-e record:
  `granular_mean/reference/generated/e/manifest.json`.
- Sequel stall: Γ = 5 diagnostic run on branch `port-astra-plate-root`
  (now merged into `main`), described in the repo README.
