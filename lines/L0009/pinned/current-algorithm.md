# Resting-contact method (line L0009): the current algorithm

As built on branch `method/rest` (worktree `sequel-data/worktrees/rest`), as of the
2026-11-26 08:04Z run of line L0009 (method/rest 607b687 tested; f6d148d adds the untested plate check marked below). Source: `granular/edmd.py`, `granular/sim.py`,
`granular/stack.py`, `granular/rest_kernel.py` on that branch; design in
`lines/L0009/design.md`; decisions D0073 to D0085 and later ones in
`ledger/decisions.jsonl`. Units: sphere diameter D, gravity g, sphere mass.

The base engine is the event-driven hard-sphere code of Bizon et al. (1998): spheres
fly under gravity between instantaneous collisions; collisions use the paper's
restitution e(v) and Walton's friction rule (friction 0.5, rolling limit 0.35); the
plate moves as z_p(t) = A sin(ωt). The method adds lasting contacts without changing
that model, and with the rest speed set to zero it is the base engine exactly.

## Parameters

| Name | Meaning | Value |
|---|---|---|
| rest speed v_rest | below this approach speed a touch becomes a lasting contact | 0.01 √(gD) |
| wake speed v_wake | above this a hit wakes a still sphere (still spheres not built yet) | 0.05 √(gD) |
| overlap check | largest overlap the engine accepts | 2e-8 D (unchanged) |
| integrator tolerance | stack integration, relative / absolute | 1e-12 / 1e-13 |
| slip floor | slip below which a contact counts as not slipping | 1e-13 |
| cell-exit sampling | spacing of the check that a stack sphere stays in its cell | 2e-4 D of motion |

None of these is physics: v_rest and v_wake are the paper's thresholds (bulk checks at
0.003 and 0.03 are planned to show results don't depend on them); the rest are
numerical settings at round-off.

## States of a sphere

```
FREE    flies on a parabola; ordinary event-driven collisions
RIDER   rests on the plate: height = plate height + radius; horizontal motion in
        closed form (slides with friction 0.5 × contact force until it rolls,
        then rolls at constant speed); leaves at the closed-form release time,
        when the plate's downward acceleration reaches g
STACK   part of a moving stack: a set of spheres in lasting contact with each
        other and with the plate, moved together by integrating their equations
        of motion (see below); its path is stored as short polynomial pieces
STILL   (designed, not built) moves rigidly with the plate when the balance test
        says its contacts can hold it
```

## Events and what they do

```
plate hit by FREE sphere at time t:
    if |approach| < v_rest and the plate pushes (plate acceleration > -g):
        capture: collision with restitution 0 (Walton's tangential rule kept)
        centre put exactly on the plate (round-off size, booked)
        sphere -> RIDER
    else: ordinary plate collision

RIDER release time reached:          RIDER -> FREE (same position, velocity, spin)

two spheres touch, one of them a RIDER:
    if approach < v_rest and the other is FREE:
        remove the approach (restitution-0 touch on the rider, which the plate holds)
        build a moving stack of the two (rider on plate, other sphere on rider)
    elif both RIDERs and approach < v_rest:
        (side-by-side stacks not built) riders freed, ordinary collision
    else:
        rider -> FREE, ordinary collision

RIDER reaches a side wall:           RIDER -> FREE, ordinary wall collision

sphere k touches a STACK sphere h:
    if k is in another stack:        break both stacks, ordinary event follows
    elif approach < v_rest:          k joins the stack: contact k-h, plus k-plate
                                     if k was riding; one restitution-0 touch over
                                     the whole new stack removes every closing
                                     contact's approach by normal impulses, the
                                     plate immovable (D0089)
    else:                            break the stack, ordinary collision follows

start of any stack (built, joined, or split):
    a contact whose push would be negative ("pulls") is not a contact:
    drop it and start the parts still joined; single spheres go back
    RIDER/FREE (D0091; before, the whole start was refused and the same
    touch came back at the same instant)

end of a stack's stored span:
    if a contact's push fell to zero ("open"):
        split the stack: parts still on the plate stay stacks (or become RIDER
        when one sphere is left); the rest become FREE
    elif a stack sphere reached a side wall: break the stack
    elif a stack sphere with no plate contact reached the plate:
        break the stack; the plate hit is an ordinary event
        (D0093, committed 2026-11-26 in f6d148d, NOT YET TESTED)
    else (span reached a cell face, the run's stop time, or the store is full):
        start the next span

break a stack:  each sphere -> RIDER if it has a plate contact and the plate
                pushes, else FREE; it keeps its position, velocity and spin
```

## A moving stack

```
state: positions, velocities, spins of its spheres; contacts (sphere-sphere or
       sphere-plate), each "rolling" or "sliding"
forces at any instant: one small linear solve —
    each contact's push keeps that contact's approach acceleration at zero;
    rolling contact: friction keeps its slip acceleration at zero;
    sliding contact: friction = 0.5 × push, against the slip
motion: integrated by an adaptive Dormand-Prince 5(4) method at the tolerances
        above, with dense output; no fixed step, no impulses, no position
        corrections, nothing removed at steps
contact changes, each a located root of the dense output, cut back to it:
    push reaches zero        -> contact opens (span ends, stack splits)
    rolling needs > 0.5 push -> contact slides
    sliding slip reaches 0   -> contact rolls (or slides on if rolling needs
                                more friction than 0.5 × push)
at a stack's start: a contact that slips, or needs more than 0.5 × push to
    roll, starts sliding
plate work and friction loss: integrated with the motion and booked in the
    engine's energy accounts at each span's end, with the plate's vertical
    impulse (change of the stack's vertical momentum plus its weight × time)
```

How the event loop sees a stack (compiled code):

```
span: the stack is integrated in Python from now to the earliest of
      the run's stop time, a contact opening, a stack sphere about to leave its
      cell or reach a side wall, or a full store (2048 pieces)
each integrator step is stored as a quartic polynomial in time per sphere
other spheres search for their first contact with a stack sphere by
      conservative advancement on the stored polynomials: steps that provably
      cannot skip a contact, from the gap, its rate of change, and a bound on
      the acceleration taken from the polynomials; a pair already at
      contact counts as touching only if its gap could go below the search's
      floor (1e-13 on the squared distance) before it opens (D0092): a
      round-off approach (7e-18) between spheres at rest is not a touch
a contact found, or the span's end, hands control back to Python
```

## Built and tested, and not

| Piece | State |
|---|---|
| Capture on the plate, closed-form ride, release | built, tested; energy books close to 1e-14 |
| Contact searches against riders | built, tested against brute force |
| Moving stacks, integrated offline | built, tested; books close to 3e-13 |
| Event loop stops at a slow touch on a rider and builds the stack | built, tested |
| Stacks fed back into the event loop (spans, searches, join, break, split) | built 2026-11-26; no 2D stall layer completes its first cycle yet (best: seed 1, f* 0.3 reaches 5.88 of 7.45) |
| Plate check for stack spheres without a plate contact | committed untested (D0093) |
| Still spheres and the balance test in the event loop | designed, built only as a separate function |
| Bounce off a still sphere between v_rest and v_wake | designed, not built |
| Checkpoints with live stacks | not built (refused with an error) |
| Long-contact test, bulk check, 2D grid | not run |
