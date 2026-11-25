# Instructions for L0009

Newest last. Chris writes this file.

## 2026-11-24 23:13, Chris, from the dashboard

You asked:

> Should a sphere be able to ride on a sphere that is itself rolling, which means moving a whole rolling stack together with a small solver for its contact forces? Or should the first build let only the plate and still spheres carry a rider?

Answer:

yes a sphere is going to have to ride on a rolling sphere I think.

## 2026-11-24 23:13, Chris, from the dashboard

You asked:

> Should the wake speed equal the rest speed (one threshold), or be higher as in the paper, with hits in between bouncing off the resting sphere as if it were immovable?

Answer:

These are all parameters to tune. To start, let's make it higher, but it's something to tweak later.

## 2026-11-24 23:13, Chris, from the dashboard

You asked:

> Is a rest speed of 0.01 (the paper's deposition value) right, with bulk checks at 0.003 and 0.03 to show results don't depend on it?

Answer:

That's fine, but again, these are parameters to bake into the code.

## 2026-11-24 23:14, Chris, from the dashboard

You asked:

> Should the paper's store-and-return of the energy removed at freezing be dropped?

Answer:

Yes, I think drop it
