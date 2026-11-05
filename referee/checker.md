# Checks specific to sequel

Human-only. The checker runs these in addition to `CHECKER.md`.

- For any contact-method claim, rerun the energy audit or recompute it from
  the run's `audit.json`: every completed cycle must pass, with no energy
  gains. Check the method routes every velocity or position change it makes
  through the accounted terms (`granular/edmd.py`, `run_events`); a change
  outside them shows up as a residual, but only if the method doesn't hide
  it in plate work.
- Check that tolerances, sampling, settling and comparison windows are the
  same for the method and the baseline.
- For anything shown at one driving condition, check a neighbouring one.
- For any claim that a method is minimally invasive (acceptance criterion 3
  in `DIRECTION.md`), read the method's diff against `main` and say plainly
  what it changes beyond long-lasting contacts: ordinary collisions, tuned
  constants the result depends on, extra state. Argue the other side.
- For survival claims, read the runs' `slow_episodes`: a run that completed
  only because its episodes cleared after hours is different from one that
  never slowed down. Say which.
