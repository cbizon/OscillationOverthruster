# Grapenuts: what the code does (for the checker)

Written Nov 24 from the code at grapenuts commit **486d8eb** (clone in
`~/Projects/experiments/sequel-data/grapenuts`), by reading
`granular/edmd.py`, `granular/sim.py` and diffing both against sequel commit
`6eae1cb`, which grapenuts' README names as the source of its engine.
`runner.py`, `export.py` and `__init__.py` are byte-identical to sequel's at
6eae1cb; all changes are in `edmd.py` (+654 diff lines) and `sim.py` (+141).
The repository's own results are in `results/engine_checks.md` and
`results/column_pilot.md` (written by grapenuts, not checked by this program).

## The idea

A hybrid of hard and soft spheres. A touch either stays an instantaneous hard
collision (sequel's operator, unchanged) or becomes a **spring**: a linear
spring-dashpot between two spheres or a sphere and the plate, applied as
impulses ("kicks") every `dt`. Between kicks all spheres fly freely under
gravity, so event prediction, the cell grid and the plate root solver are
sequel's. A sphere pair (or sphere and plate) holding a spring is skipped in
prediction (`predict`, edmd.py:798 and :835), so the spring replaces their
collisions while it lasts. Side walls are always hard.

## Step by step (edmd.py at 486d8eb)

1. **Touch.** At a pair event (`run_events`, ~:1196) or plate event (~:1255)
   the closing speed is computed. If `touch_is_soft` (:277) says so, a spring
   is created at zero compression with velocities untouched (`spring_add`,
   :299); otherwise sequel's hard collision runs as before.
2. **Which touches become springs** (`contact_mode`): `never` (sequel's hard
   engine; the default in `Simulation`), `always`, or `tc` (term T0033): a
   spring if either sphere had a hard collision or lost a spring within the
   last `tc_window` (default the contact time t_c), or holds any spring now,
   optionally only below an approach speed `soft_speed_limit` (default
   infinite). So in `tc` a sphere resting in a cluster draws every new touch
   into springs; a clean isolated binary collision stays hard.
3. **Spring constants at creation.** Normal stiffness `kn = k` (the one
   setting, units m g / D). Damping `gamma = 2 zeta sqrt(kn m_eff)` with zeta
   chosen so that an *isolated* linear spring-dashpot collision at this
   approach speed has the paper's e(v) (:314). The damping is then fixed for
   the life of the spring.
4. **Kick** (`kick`, :919), every `dt = t_c / steps_per_contact` (default
   20), with `t_c = pi sqrt(m_eff/k)`, m_eff = 1/2 for two unit spheres
   (sim.py:229). All springs' forces are computed from one state, then
   applied together, then every kicked sphere re-predicts its events.
   - Normal force `kn delta + gamma * closing`, **not clamped at zero**, so
     the dashpot pulls (tension) near the end of a contact; the docstring
     says this is so an isolated collision has exactly the target
     restitution.
   - Tangential, `walton` law (default): for as long as an isolated collision
     of this contact would last (plus one kick), deliver the Walton
     tangential impulse that sequel's operator would give for the creation
     state (mu, beta0 from the paper), in proportion to the normal force.
     Afterwards a tangential spring `kt = 0.125 kn` (KT_RATIO, sim.py:22,
     "gives beta0 = 0.35 (measured)") with Coulomb cap `kt |xi| <= mu
     max(fn, 0)`; the stretch xi is rotated into the current tangent plane
     each kick. `spring` law: the tangential spring throughout.
   - **Release**: a spring found with compression `<= 0` at a kick is
     removed; its stored tangential energy is booked as dissipated, and
     both spheres' "last collision" time is set to now (so the tc window
     restarts).
5. **Plate springs** add their vertical impulse to the plate's impulse and
   work books like a plate collision.
6. **Nudge option** (`plate_nudge`, ported from sequel's method/nudge
   16f3334): after a hard plate collision, raise the sphere to two floating
   point steps above the plate, booking m g dz to `EN_NUDGE`. Off by default;
   meant with `contact_mode="never"`.

## Deviations from the paper's model and sequel

| what | value | where |
| --- | --- | --- |
| Collision model inside springs: linear spring-dashpot, finite duration, overlap | k chosen by the user; grapenuts ran 1e4 to 1e9 | edmd.py:299, :919 |
| Restitution matched only for an isolated two-body contact at its creation speed | zeta from e(v) once | :314 |
| Normal force allowed to be tensile (dashpot) | — | :919 docstring |
| Tangential spring and its stiffness ratio | kt/kn = 0.125 | sim.py:22 |
| Time step of kicks | t_c / 20 | sim.py:232 |
| Trigger window | t_c | sim.py:233 |
| Approach-speed limit for springs | infinite by default | sim.py:235 |
| Overlap allowed inside a spring; no limit enforced (largest recorded only) | 0.0048 D at k = 1e7 in grapenuts' 2D Gamma 5 runs | :1092 |
| Partner skipped in prediction while sprung | — | :798, :835 |
| Up to 16 springs per sphere, 8N + 16 in total; more raises | MAXC = 16 | :49, sim.py:262 |

Unchanged: the hard operator (`collide_pp`, `collide_wall`), sequel's pair
overlap check (relative 2e-8) for every pair not holding a spring, the plate
penetration and plate-contact checks, event prediction otherwise. Grapenuts
has no commit history that splits these choices into separate decisions;
they arrived together in f5bbc07 (springs in the engine, Nov 13) and 7cda4dc
(the walton tangential law, Nov 13). Nothing in this program's ledger decided
them: they are grapenuts' design.

Under `DIRECTION.md` this is a change of the collision model (finite-duration
spring contacts with overlap instead of the paper's instantaneous operator,
with three constants the paper doesn't have), which is reserved for Chris.
Chris asked for the evaluation, so it runs; whether such a model can become
sequel's default is Chris's call.

## Energy bookkeeping

`layer_energy` adds the springs' stored energy (normal `kn delta^2 / 2`,
tangential `kt |xi|^2 / 2`, sim.py:394). One new book, `EN_SOFT_DISS`, takes
the dashpot's work (its impulse times the mean closing rate across the
kick, an approximation), the friction work of sliding and collision-phase
contacts (from the mean surface velocity across the kick), and the
tangential energy dropped at release. A separate counter `SF_FRICTION_GAIN`
sums the positive work friction impulses did (it is inside `EN_SOFT_DISS`
too). What remains in a per-cycle balance is the integrator's error, which
grapenuts measured as second order in dt, mostly a loss (about -1e-3 to
-3e-4 of throughput at 20 kicks per t_c), and a gain with the speed-limited
trigger.

**sequel's referee can't audit this as it stands.** `referee/long_contact.py`
sums plate work and plate, pair and wall dissipation only, at a tolerance of
1e-8 of throughput. A local 3-cycle smoke test of grapenuts (2D, Gamma 3.5,
f* 0.5, depth 5, tc, k = 1e7) gives a residual of -2e-2 to -8e-2 by the
referee's sum and -4e-5 to -2e-4 once the springs' dissipation is counted
(hard mode: 1e-14). E0099 reports both.

## Tested so far

By grapenuts itself (its results files; one 1D column pilot, single-contact
checks, 2D L = 100 layers, three seeds): 2D Gamma 3.5, f* 0.5, depth 5 against
the hard engine (heights agree within 0.001 to 0.04 depending on k); 2D
Gamma 5, f* 0.3 and 0.6, depth 10, where the hard engine stalls, at k = 1e5
to 1e9 (all spring runs completed 120 to 160 cycles; height levels off from
k = 1e7); agreement with the nudge engine at Gamma 5, f* 0.6 within 0.2% in
height. By this program: nothing until E0099 (submitted Nov 24: the twelve
2D grid conditions and the 3D Gamma 5 case at k = 1e7, plus five hard
controls).
