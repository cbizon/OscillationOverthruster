# Resting-contact method (line L0009): the current algorithm

As built on branch `method/rest` (worktree `sequel-data/worktrees/rest`), as of the
2026-11-28 07:02Z run of line L0009 (method/rest dbc0f59: the check of pairs inside a stack ignores crossings within the touch search's round-off floor, D0104, tested in E0126; before it 39e28e3: spheres detached by a pulling contact at a stack's start stay in it as members with no contact, D0103, tested in E0122; contacts carried over rolling keep rolling at a new stack's start, D0101, and a touch on a stack sphere is reported where the gap actually crosses the search floor, D0102, both tested in E0120 and E0121; pairs inside a stack checked, D0100; direct force-matrix build, E0117; earlier versions tested in E0108 to E0116). Source: `granular/edmd.py`, `granular/sim.py`,
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
| cell-exit sampling | spacing of the check that a stack sphere stays in its cell (plate and side-wall crossings are then found exactly, by bisection) | 2e-4 D of motion |

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

a contact whose push would be negative ("pulls") is not a contact:
    at a stack's start (built, joined, or split), before its first piece:
        drop it; if that leaves one part on the plate and other parts off
        it, the stack starts with every sphere, the detached ones as members
        with no contact (gravity only), joined again by the check of pairs
        inside a stack where their gap closes past its start value, and
        released at the stack's next span restart (D0103, 2026-11-28);
        a pair inside a stack with no contact counts as reaching each other only once its gap is
        below its start gap less the round-off floor RIDER_GAP_TOL/(4 (Ra+Rb)) (D0104, 2026-11-28);
        otherwise start the parts still joined; single spheres go back
        RIDER/FREE (D0091)
    found later (at a span restart, or after a contact switches between
    rolling and sliding inside a span): the span ends there as at an
    opening contact and the stack splits (D0095, 2026-11-27)
    (before D0091/D0095 the start was refused, every sphere handed back
    unchanged, and the same touch came back at the same instant)

end of a stack's stored span:
    if a contact's push fell to zero ("open"):
        split the stack: parts still on the plate stay stacks (or become RIDER
        when one sphere is left); the rest become FREE
    elif a stack sphere reached a side wall it has no contact with (D0098;
            span cut at the crossing, found by bisection):
        if it moves towards the wall slower than v_rest: it joins the stack
            with a wall contact (normal push, rolling or sliding friction 0.5,
            as the engine's wall collision); one restitution-0 touch over the
            whole stack removes the approach, as at a join
        else: break the stack; the wall hit is an ordinary collision
    elif two spheres of the stack with no contact between them touch (D0100,
            2026-11-27; span cut at the crossing, found by bisection):
        if they approach slower than v_rest: a rolling contact between them
            is added; one restitution-0 touch over the whole stack removes
            the approach, as at a join
        else: break the stack; the two collide by the ordinary collision at once
    elif a stack sphere with no plate contact reached the plate (D0093;
            span cut at the crossing, found by bisection):
        break the stack; that sphere is handed back by the capture rule at
        once: RIDER if its approach is below v_rest and the plate pushes,
        else FREE and the plate hit is an ordinary event (D0096; acted once
        in E0109, seed 2)
    else (span reached a cell face, the run's stop time, or the store is full):
        start the next span

break a stack:  each sphere -> RIDER if it has a plate contact and the plate
                pushes, else FREE; it keeps its position, velocity and spin
```

## A moving stack

```
state: positions, velocities, spins of its spheres; contacts (sphere-sphere,
       sphere-plate or sphere-side-wall), each "rolling" or "sliding"
forces at any instant: one small linear solve (its matrix filled directly from
    each force's effect on the accelerations, 2026-11-27, E0117) —
    each contact's push keeps that contact's approach acceleration at zero;
    rolling contact: friction keeps its slip acceleration at zero;
    sliding contact: friction = 0.5 × push, against the slip
    if the contacts fix the forces more than once over (a sphere rolling on the
    plate and a wall at once can), the smallest forces that do it (D0098; counted)
motion: integrated by an adaptive Dormand-Prince 5(4) method at the tolerances
        above, with dense output; no fixed step, no impulses, no position
        corrections, nothing removed at steps
contact changes, each a located root of the dense output, cut back to it:
    push reaches zero        -> contact opens (span ends, stack splits)
    rolling needs > 0.5 push -> contact slides
    sliding slip reaches 0   -> contact rolls (or slides on if rolling needs
                                more friction than 0.5 × push)
at a stack's start: a contact that slips, or needs more than 0.5 × push to
    roll, starts sliding; except that a contact which was rolling in the
    live stack the new one comes from (join, split, wall or inner join,
    dropped contact) keeps rolling unless it needs more than 0.5 × push:
    its slip there is the integration's drift, e.g. 1.75e-11 (D0101,
    2026-11-28)
plate work and friction loss: integrated with the motion and booked in the
    engine's energy accounts at each span's end, with the plate's vertical
    impulse (change of the stack's vertical momentum plus its weight × time)
```

How the event loop sees a stack (compiled code):

```
span: the stack is integrated in Python from now to the earliest of
      the run's stop time, a contact opening, a stack sphere about to leave its
      cell, reaching a side wall or the plate it has no contact with (exact
      crossing), or a full store (2048 pieces)
each integrator step is stored as a quartic polynomial in time per sphere
other spheres search for their first contact with a stack sphere by
      conservative advancement on the stored polynomials: steps that provably
      cannot skip a contact, from the gap, its rate of change, and a bound on
      the acceleration taken from the polynomials; a pair already at
      contact counts as touching only when its gap actually goes below the
      search's floor (1e-13 on the squared distance): the search steps on
      by steps that provably keep it above the floor and reports the touch
      where it reaches half the floor (D0092; D0102, 2026-11-28: before, a
      pair still closing one step later was reported at the step's start);
      a round-off approach (7e-18) between spheres at rest is not a touch
a contact found, or the span's end, hands control back to Python
```

## Built and tested, and not

| Piece | State |
|---|---|
| Capture on the plate, closed-form ride, release | built, tested; energy books close to 1e-14 |
| Contact searches against riders | built, tested against brute force |
| Moving stacks, integrated offline | built, tested; books close to 3e-13 |
| Event loop stops at a slow touch on a rider and builds the stack | built, tested |
| Stacks fed back into the event loop (spans, searches, join, break, split) | built 2026-11-26; no 2D stall layer completes its first cycle (7.45) yet. Furthest on 2026-11-27: seed 2, f* 0.3 to 6.59 (E0109, E0111, E0116; stopped by the 900 s CPU cap); seed 1, f* 0.3 to 5.92, then a same-instant loop at 5.9205 (E0116, traced in E0118; at fde8612 at 5.9205062, E0121); seed 1, f* 0.4 completes 5.28, then a same-instant loop at 5.2816 (E0110; at fde8612 at 5.2815952, E0121); with D0103 (39e28e3) it completes 5.29 from a snapshot at 5.2816 (E0122) |
| Same-instant loop after a dropped join contact | open. 2026-11-28 (E0119 to E0121): not a round-off approach and not a singular force matrix. At the joined stack's start another contact slides with a small slip (1.5e-7 at f* 0.4, 3.4e-5 in seed 1); with it sliding the joining contact pulls (push -0.41, -0.079), with it rolling it would push (+0.43, +0.37). The sliding contact sticks soon after, but the joining sphere has already been handed back free, past the search floor, and touches again at once. Fixed on the way: the slip test switching drifted rolling contacts to sliding (D0101), the start-instant modes (D0101), the touch reported at the start of the round-off zone (D0102). Undone joins now count as join_dropped, not joined. D0103 (2026-11-28) keeps the joining sphere in the stack as a member with no contact: with it the f* 0.4 layer completes the step to 5.29 from the old loop instant (E0122: 31 members kept, 27 joined later, at most 8 calls at one instant); seed 1's step 5.92 to 5.93 had not finished after 19.5 minutes (unknown why). 2026-11-28 07:02Z (E0123 to E0126): with D0103 seed 1 crawls rather than loops: first the kept sphere is rejoined every 4.45e-10 because the pair check was cut by gap round-off (fixed by D0104, which removes that chatter), then two neighbouring stacks [84, 93] and [92, 94] are broken by a 93-94 touch and rebuilt every 1e-14 time units (with D0104 for 1380 calls to the 900 s cap). f* 0.4 completes 5.29 and then crawls the same way near 5.292 |
| Pairs inside a stack with no contact between them | checked since 2026-11-27 (D0100); E0115 found two such spheres overlapping by 4.6e-5 when their stack broke (E0113's error); in E0116 the check acted once (a join) |
| Plate check for stack spheres without a plate contact | built (D0093); acted twice in E0108 and stopped the plate penetration; the landing on the plate (D0096) acted once in E0109 |
| Side walls as stack contacts | built 2026-11-27 (D0098); in E0111 seed 1 it acted 5 times (2 joins) and the layer passed the side-wall loop at 5.918 |
| Restart of a stack paused at a step's end | handled like a span-end restart since 2026-11-27 (D0099); acted in E0113 |
| Cost of a stack | 99% of a stack's CPU was its force solves (E0112): about 9 per integrator step, about 14 integrator steps per stored piece; a 5-sphere join cost 185 s under the profiler. The direct matrix build (2026-11-27, E0117) makes each solve 6 to 10 times cheaper with the same results (2e-15 where the matrix is well conditioned); not yet timed in a layer. Still open: up to 200 full steps to locate each contact change, and sequential joins at one instant redoing the whole integration |
| Still spheres and the balance test in the event loop | designed, built only as a separate function |
| Bounce off a still sphere between v_rest and v_wake | designed, not built |
| Checkpoints with live stacks | not built (refused with an error) |
| Long-contact test, bulk check, 2D grid | not run |
