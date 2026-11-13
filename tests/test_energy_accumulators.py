"""Energy terms summed per call from zero (fix/energy-accumulators).

Where the main checkout's engine still accumulates per event (before the fix
was merged, D0021), it is loaded under another name and compared.  Once main
has the fix there is nothing to compare with, and loading the same source
under a second module name must not happen: numba's on-disk cache is keyed by
source file, so the alias's entries break the next plain import."""

import importlib
import importlib.util
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

from granular import edmd as K
from granular.sim import Simulation

ROOT = Path(__file__).resolve().parents[1]


def _main_engine():
    """The main checkout's engine if it predates the fix, else None."""
    name = "granular_main"
    if name in sys.modules:
        return sys.modules[name]
    common = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--git-common-dir"],
                            check=True, capture_output=True, text=True).stdout.strip()
    pkg = (ROOT / common).resolve().parent / "granular"
    if "def add_terms(" in (pkg / "edmd.py").read_text():
        return None
    spec = importlib.util.spec_from_file_location(
        name, pkg / "__init__.py", submodule_search_locations=[str(pkg)])
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    importlib.import_module(name + ".sim")
    return module


def _cycle_residual(sim):
    e0, _ = sim.layer_energy()
    en0 = sim.en.copy()
    for k in range(1, 33):
        while sim.run_to(sim.T * k / 32, max_events=100 * sim.N):
            pass
    e1, _ = sim.layer_energy()
    d = sim.en - en0
    terms = [d[K.EN_PLATE_WORK], d[K.EN_PLATE_DISS], d[K.EN_PP_DISS], d[K.EN_WALL_DISS]]
    sim.end_cycle()
    sim.rebuild(sort=True)
    return ((e1 - e0) - sum(terms)) / sum(abs(x) for x in terms)


def test_dynamics_unchanged_and_terms_agree_with_main():
    main = _main_engine()
    if main is None:
        pytest.skip("main has the fix (D0021): no per-event engine to compare with")
    a = main.sim.Simulation(500, 100.0, 3.5, 0.3, 5.0, 1, dim=2)
    b = Simulation(500, 100.0, 3.5, 0.3, 5.0, 1, dim=2)
    for _ in range(20):
        _cycle_residual(a)
        _cycle_residual(b)
    assert np.array_equal(a.S, b.S) and np.array_equal(a.W, b.W)
    assert np.array_equal(a.cnt, b.cnt)
    assert np.allclose(a.en, b.en, rtol=1e-9, atol=1e-9)


def test_large_run_totals_do_not_spoil_the_audit():
    """With run totals already large (as after many cycles; 2e9 makes the effect plain in an ordinary cycle), main's per-event
    accumulation leaves residuals far above the audit tolerance in a
    collision-heavy cycle; summing per call from zero does not."""
    main = _main_engine()
    b = Simulation(500, 100.0, 5.0, 0.3, 5.0, 2, dim=2)
    sims = [b]
    if main is not None:
        a = main.sim.Simulation(500, 100.0, 5.0, 0.3, 5.0, 2, dim=2)
        sims.append(a)
    for sim in sims:
        for k in (K.EN_PLATE_WORK, K.EN_PP_DISS, K.EN_PLATE_DISS, K.EN_WALL_DISS):
            sim.en[k] = 2e9 if k == K.EN_PLATE_WORK else -2e9
    rb = max(abs(_cycle_residual(b)) for _ in range(3))
    assert rb < 1e-10
    if main is None:
        return
    ra = max(abs(_cycle_residual(a)) for _ in range(3))
    assert np.array_equal(a.S, b.S)
    # the gain grows with events per run_to call; an ordinary cycle has few
    # (the collision-heavy E0031 cycle: 2.1e-6 per-event vs 1.4e-11 zeroed)
    assert ra > 5 * rb
