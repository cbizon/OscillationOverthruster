# L0018: Wider or deeper box

## Status

Active. All ten E0076 (baseline) loops have ended (last: f* 0.38, job
164691, collected Nov 25). E0075 (nudge) f* 0.27 (164684) and f* 0.38
(164681, collected Nov 25 second run) have ended. 18 width-200 loops still
run on Hatteras: ten E0074 (no friction) and eight E0075 (nudge). Slurm marks every
ended loop FAILED (exit 1): that is how ramp.py exits when a loop stops, not
a crash. Read the step outcomes.

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

## Jobs in flight

| Experiment | Host | Jobs | f* | Description | Wall time |
|---|---|---|---|---|---|
| E0074 | hatteras | 164665-164674 (all running) | 0.27-0.84 | no friction, L 200, N 240000, 213 steps | 5 days |
| E0075 | hatteras | 164675-164680, 164682, 164683 running; 164681, 164684 ended | 0.27-0.84 | nudge, L 200, N 240000, 239 steps | 7 days |

E0074: Gamma 1.7 to 7.0 and back, 25 cycles per step, 4 CPU-hour cap.
E0075: Gamma 3.0 down to 1.7, up to 7.0, back, 50/25 cycles first/rest,
  2/8 CPU-hour cap down/up, turn on stop. Engine: method/nudge.
E0074 started about Nov 22 06:15Z, so its 5-day wall time ends about Nov 27
06:15Z; E0075 about Nov 29.

## What is next

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
- Collect E0074 and E0075 loops as they end, same per-step form.
- Onset rule (checker Nov 25): judge the pattern by its wavelength in sphere
  diameters, not by ring index or a variance share above one half; at width
  200 the pattern ring holds a smaller share (0.3 to 0.54 vs 0.5 to 0.76)
  because rings at larger k hold more modes, and width 100 cannot resolve
  wavelengths between 33 and 25 diameters.
- Compare the E0071 onset at L 200 with E0060 at L 100 for f* 0.44.
- If E0089 shows the nudge cost drops above Gamma 4.65, raise the E0075 caps.

## Key evidence

- evidence/E0076-results.json (working ranges, all ten loops)
- evidence/E0076-interim.json (per-step data, cost ratios)
- evidence/E0070-results.json (cost holds)
- evidence/wider-vs-deeper.md (tradeoff)
- evidence/D0054-width200-fields.json (field storage reduction)
- sequel-data/runs/E0071/ (onset loop data, 311 MB)
