"""Run the referee's long_contact.py unchanged and, when it ends (any way),
write the engine's counters to OUTDIR/counters.json.

The referee records method counters only through checkpoints, which a run
that stalls in its first cycles never writes.  This wrapper imports the
engine first, remembers the Simulation the referee builds, calls the
referee's main() with the same arguments, and dumps sim.cnt, sim.en and the
resting count afterwards.  It changes nothing in the run.

usage: lc_counters.py <long_contact.py arguments>"""
import importlib.util
import json
import sys
from pathlib import Path

REFEREE = Path(__file__).resolve().parent.parent / "referee/long_contact.py"
argv = sys.argv[1:]
engine = Path(argv[argv.index("--engine") + 1]).expanduser().resolve()
outdir = Path(argv[argv.index("--outdir") + 1]).expanduser().resolve()
sys.path.insert(0, str(engine))
from granular import edmd as K          # noqa: E402
from granular import sim as simmod      # noqa: E402

# optional: SEQUEL_CONTACT_OVERRIDE='{"v_sleep": 1e-3}' changes the engine's
# default contact settings for this run (recorded in counters.json)
import os                                # noqa: E402
override = json.loads(os.environ.get("SEQUEL_CONTACT_OVERRIDE", "{}"))
if override:
    unknown = set(override) - set(simmod.CONTACT_DEFAULTS)
    if unknown:
        raise ValueError("unknown contact settings: %s" % sorted(unknown))
    simmod.CONTACT_DEFAULTS.update(override)

made = []
_init = simmod.Simulation.__init__


# optional: SEQUEL_MU=0.1 sets the friction coefficient of this run (the
# referee builds Simulation with the engine's default; recorded in counters.json)
mu_override = os.environ.get("SEQUEL_MU")


def _counter_dict(sim):
    names = {v: n for n, v in vars(K).items() if n.startswith("C_") and isinstance(v, int)}
    ennames = {v: n for n, v in vars(K).items() if n.startswith("EN_") and isinstance(v, int)}
    return dict(counters={names.get(k, "c%d" % k): int(x) for k, x in enumerate(sim.cnt)},
                energy_terms={ennames.get(k, "en%d" % k): float(x) for k, x in enumerate(sim.en)})


def init(self, *a, **k):
    if mu_override is not None:
        k.setdefault("mu", float(mu_override))
    _init(self, *a, **k)
    made.append(self)
    # also append the cumulative counters after every completed cycle to
    # OUTDIR/counters_by_cycle.jsonl, so a run cut short keeps them
    end_cycle = self.end_cycle

    def logged_end_cycle(*a2, **k2):
        d = _counter_dict(self)
        d["cycles_completed"] = int(self.cycle) + 1
        with open(outdir / "counters_by_cycle.jsonl", "a") as fh:
            fh.write(json.dumps(d) + "\n")
        return end_cycle(*a2, **k2)

    self.end_cycle = logged_end_cycle


simmod.Simulation.__init__ = init
spec = importlib.util.spec_from_file_location("long_contact", REFEREE)
lc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lc)
try:
    lc.main(argv)
finally:
    if made:
        sim = made[-1]
        names = {v: n for n, v in vars(K).items() if n.startswith("C_") and isinstance(v, int)}
        ennames = {v: n for n, v in vars(K).items() if n.startswith("EN_") and isinstance(v, int)}
        out = dict(cycle=int(sim.cycle),
                   event_time=float(sim.ev_t[sim.tree[1]]),
                   counters={names.get(k, "c%d" % k): int(x) for k, x in enumerate(sim.cnt)},
                   energy_terms={ennames.get(k, "en%d" % k): float(x) for k, x in enumerate(sim.en)},
                   mu=float(sim.P[K.P_MU]), mu_override=mu_override, contact_override=override)
        if hasattr(sim, "resting_count"):
            out["resting_at_end"] = sim.resting_count()
            out["contact_settings"] = sim.contact_settings()
        (outdir / "counters.json").write_text(json.dumps(out, indent=1) + "\n")
