# L0018: Wider or deeper box

## Status

Active, waiting on Chris (B0009). All thirty width-200 loops have ended.
E0076 (baseline) and E0075 (nudge): all ten each, collected. E0074 (friction
off): f* 0.84, 0.74, 0.65 completed all 213 steps; the other seven were
cancelled Nov 26 about 11:24Z (D0094) because each had passed the 100
CPU-hour per-run limit (101.1 CPU-hours by Slurm, one core). None had a
stopped step. Resuming them is Chris's call: about 118 to 274 CPU-hours a
loop in total. Nothing is running for this line.

## What is done

- Cost holds (E0070, Nov 18): twice as wide costs 4.7 to 5.6 times the
  paper's box per cycle; twice as deep costs 12 to 18 times, not the 3.8
  scaled from 2D.
- Onset loop at L 200 (E0071, completed Nov 20): f* 0.44, Gamma 1.7 to
  3.0 and back, 25 cycles per step, no friction. 53 steps, all completed.
  22.9 CPU-hours, 311 MB.
- Tradeoff written (evidence/wider-vs-deeper.md).
- Field storage (D0054, D0057): width-200 passes store no height grids, only
  ring spectra and variances (fields.npz: time, frame, var, spec), at 32
  phases a cycle; checkpoints at Gamma multiples of 0.5.
- E0076 per-loop evidence: evidence/E0076-interim.json (every step of every
  loop from the mirrored summary.json, with sha256; end_comparison per loop;
  width100_stop_modes; down_leg_cost_ratio, 75 pairs, median 7.42;
  up_leg_cost_ratio, 114 pairs, median 7.31; width100_cost_jump_near_3_35).
- E0076 working ranges (Nov 25): evidence/E0076-results.json. Table per f*
  of floor and highest Gamma at both widths with the stop type at each end
  (CPU cap, overlap, stall). At no end where the comparison means something
  (physical stop at both widths, or one-sided) did width 200 reach further
  than width 100. NOT "never": at the f* 0.50 floor (cap stop at both
  widths) width 200 went 0.05 lower (2.35 vs 2.4); checker Nov 25, fixed.
  Comparable ends (physical stop at both widths): f* 0.65 floor 2.4 vs 2.25,
  top 3.9 vs 4.1; f* 0.57 top 3.8 vs 4.0; f* 0.44 top 4.0 vs 4.0. First-step
  failures: four of ten at width 200, one at width 100. 343.6 CPU-hours.
- f* 0.38 (Nov 25): floor 2.45 (cap at 2.4), top 4.0 (8.0 CPU-hour up cap at
  4.05 after 17 cycles; cost per cycle 14 times the 4.0 step). Width 100:
  2.35 (overlap at 2.3) to 4.0 (stall at 4.05, cost per cycle 17 times).
- Checker Nov 24 third review answered: f* 0.57 up median is 11.35 (write
  11.4, not 11.5); the high up-leg medians come from width-100 cost jumps
  near Gamma 3.35 (down at 0.44 and 0.57, up 1.7 times at 0.38), so they do
  not size up-leg caps; that proposal is withdrawn. Timestamps: write the
  real time when appending to the ledger.
- E0075 nudge f* 0.27 (164684, A0094): first-step cap after 49 of 50 cycles.
- E0075 nudge f* 0.38 (164681, A0186, Nov 25): floor 2.45 (2.0 CPU-hour cap
  at 2.4, 24 of 25 cycles), top 4.35, stall (frozen_time) at 4.4 in cycle 25
  at 6.51 CPU-hours (under the 8.0 cap). 50 steps, 75.1 CPU-hours, clean.
  Width-100 nudge (E0065 loop nudge-3d-f0.38): 2.25 (0.5 cap at 2.2) to 4.35
  (0.5 cap at 4.4 after 19 cycles). Top: same last step, one-sided (wall at
  Gamma 4.4 in both boxes). Floors: cost floors, not comparable. Matched-step
  cost ratio 7.6 down (11 pairs), 10.3 up (38 pairs). In E0076-interim.json
  (loops[-1]). The up leg resumes at floor+0.05 by design (ramp.py skips
  steps at or below the floor).
- E0075 nudge f* 0.74 (164676, A0187, Nov 25 third run): floor 2.3 (2.0
  CPU-hour cap at 2.25, 23 of 25 cycles), top 4.45 (8.0 CPU-hour cap at 4.5,
  12 of 25 cycles). 58 steps, 77.1 CPU-hours, clean, no stall. Width-100
  nudge: 2.05 (0.5 cap at 2.0) to 4.4 (0.5 cap at 4.45). All four ends are
  cap stops: not comparable. Matched-step cost ratio 8.8 down (14 pairs), 7.7
  up (42 pairs). In E0076-interim.json (loops[-1]).
- Checker Nov 25 second review answered: width-100 nudge loops stopped at
  4.45 (five), 4.4 (two), 4.5 (one), not all at 4.4; up caps are 16 times
  width 100's (8.0 vs 0.5), above the cost ratio, so only down caps are too
  small; 09:50Z stamps corrected to 09:37Z.
- E0075 all ten nudge loops (Nov 26): evidence/E0075-results.json
  (summary_table, findings, per-step data of the last seven loops; the
  first three are in E0076-interim.json). Collected with
  tools/collect_width200_loops.py (reads the mirror and job records).
  Floors 2.3 to 2.5 at width 200, 0.1 to 0.3 above width 100 at every f*;
  tops 4.35 to 4.5. Every end a CPU cap stop except the f* 0.38 stall at
  4.4, so none is comparable. Against the width-100 loops continued with a
  2 CPU-hour up cap (E0072, from evidence/E0085-nudge-wall-fields.json):
  width 200 never further, 0.05 to 0.15 short at five f*, still caps.
  Cost per cycle: steep rise from 4.35-4.4 in both boxes for f* 0.84-0.38,
  a bit steeper at width 200; at f* 0.33 one step earlier at width 200
  (10.3 times from 4.3 to 4.4 vs 2.0). Matched-step cost ratio down
  8.7-9.5, up 7.3-7.9 (f* 0.84-0.44), 10.1-10.3 (0.33, 0.30).
- E0074 all ten (Nov 26 second run): evidence/E0074-results.json (summary_table,
  findings, per-step data; supersedes E0074-interim.json, whose two loops
  reproduce step for step). No step stopped in any loop. Matched-step cost
  ratio median up 9.7 to 11.1, down 7.0 to 9.9. collect_width200_loops.py now
  lists a step still running at cancel as interrupted_steps.
- E0074 f* 0.84 and 0.74 (Nov 26): evidence/E0074-interim.json. All 213
  steps, clean, 80.5 and 89.9 CPU-hours; costliest step 0.95 CPU-hours (cap
  4); matched-step cost ratio about 10 (E0070's cost holds said 4.7-5.6).
- Pinned table lines/L0018/pinned/working-ranges.md, regenerate with
  `python3 -I tools/l0018_pinned_ranges.py` after new evidence.
- Checker Nov 25 third review answered (Nov 26): "up caps exceed the cost
  ratio" holds for NUDGE loops only (16 times vs 7.3-10.3). Baseline
  (E0076) up caps were 4 times (2.0 vs 8.0), below its cost ratio 7.4-11.4;
  baseline floors include physical stops (f* 0.65 both widths; width-100
  overlap at f* 0.38). closes_when's "about seven times down" updated to
  about 9 down, 7-10 up (nudge).

## Jobs in flight

None. E0074 jobs 164668 to 164674 cancelled Nov 26 (artifacts A0204 to
A0210); 164667 (f* 0.65) completed (A0203).

To resume a cancelled loop (only if Chris says so): submit the same command
as its job record (evidence/E0074/hatteras-<job>.json) with the run folder as
`--input A02xx` and ramp.py's outdir pointing at a copy of it; ramp.py skips
completed steps and continues from the latest kept checkpoint (step 0, every
Gamma multiple of 0.5, and the latest completed step). Use
`--max-cpu-hours-total` so a loop cannot pass whatever allowance Chris sets.

## What is next

- B0009 (Chris): resume the seven cancelled E0074 loops or not, and under
  what per-run allowance. Default if unanswered: leave them cancelled.
- LESSON: a Hatteras job with a wall time over 100 hours on one core can pass
  the 100 CPU-hour per-run limit. Check wall time x cores against it at
  submission, and use ramp.py --max-cpu-hours-total.
- E0076's registered judgement is on onset (where the pattern appears),
  not on the working range: "fails if at 3 or more f* where both boxes have
  an onset the L 200 onset is more than 0.1 in Gamma from the paper's box".
  No onset has been measured for E0073 (width 100) or E0076. The rule named
  in E0071 (tools/loop_analysis.py, first of three rising steps above the
  flat level) is not in the repository. Next: record a decision on the
  amplitude measure and onset rule, measure at both widths, then write the
  E0076 outcome. A pilot at f* 0.38 was run Nov 25 (see the session summary):
  it says whether these loops reach a flat layer at all.
- Fetching: tmp/fetch is shared with other lines running at the same time
  and gets emptied under you. Copy each fetched file to tmp/L0018/ at once.
  One fetch takes about 3 to 7 s; a whole loop's fields.npz about 3 to 5 min.
  For all 15 loops, a Hatteras job next to the data is quicker.
- Onset rule (checker Nov 25): judge the pattern by its wavelength in sphere
  diameters, not by ring index or a variance share above one half; at width
  200 the pattern ring holds a smaller share (0.3 to 0.54 vs 0.5 to 0.76)
  because rings at larger k hold more modes, and width 100 cannot resolve
  wavelengths between 33 and 25 diameters.
- Compare the E0071 onset at L 200 with E0060 at L 100 for f* 0.44.
- If E0089 shows the nudge cost drops above Gamma 4.65, a width-200 nudge
  rerun above the wall would need far larger caps (all E0075 loops ended).
- Cap scaling: for the NUDGE loops only the width-200 down caps are short
  of the cost ratio (4 times vs 8.7 to 9.5); nudge up caps (16 times vs
  width 100's half hour) exceed it (7.3 to 10.3), but against the continued
  width-100 loops (2 CPU-hour up cap) they are only 4 times. BASELINE loops:
  down and up caps both 4 times, below the cost ratio 7.4 to 11.4.

## Key evidence

- evidence/E0074-results.json (friction off, all ten loops)
- evidence/E0076-results.json (working ranges, all ten loops)
- evidence/E0076-interim.json (per-step data, cost ratios)
- evidence/E0070-results.json (cost holds)
- evidence/wider-vs-deeper.md (tradeoff)
- evidence/D0054-width200-fields.json (field storage reduction)
- sequel-data/runs/E0071/ (onset loop data, 311 MB)
