# Proposal: Dynamic Compiler JIT Warmup Caching and Selective Preheating

**Status:** partially superseded; re-scope before implementation.

> MolSysMT now exposes `molsysmt.warmup()` and centralized lazy-JIT machinery.
> This proposal predates that implementation. Only gaps demonstrated against the
> current API should be retained. Background compilation, swallowed exceptions,
> and cache-location changes require explicit thread-safety, diagnostics, and
> portability review.

## Abstract

We propose exposing a dedicated, programmatic warming API (`molsysmt.warmup()`) and optimizing Numba JIT cache folder persistence in `molsysmt`. This compiles high-frequency topological mapping functions and dynamic handlers upfront, removing the dynamic compilation lag that spikes the first molecular operations in interactive environments by up to 4.0 seconds.

---

## The Problem

MolSysMT relies heavily on dynamic JIT compilation (via Numba) and lazy-loaded structure parsers to achieve high performance on large scientific datasets. However, because JIT compilation happens on the first call (lazy compilation), the very first time a coordinate set or structure file is loaded in a Python session, the system freezes for several seconds:
* **First load duration**: ~4,046 ms
* **Subsequent loads**: ~354 ms

This dynamic compilation lag propagates heavily to the rest of the ecosystem:
1. **Interactive Visualization (`molsysviewer`)**: The very first time a structure is loaded into the Jupyter/Python widget or standalone GUI, the interface freezes visually for over 4.0 seconds, leading to a jarring user experience.
2. **Sibling Analysis Packages (`elastnetmt`, `pharmacophoremt`, `topomt`)**: Since these packages utilize `molsysmt` as their core molecular representation engine to query topologies, extract coordinate selections, or compute distance vectors, they also inherit this initial 4-second compilation overhead during their first active computations.

Currently, there is no centralized, standardized mechanism for these downstream packages to trigger dynamic JIT preheating asynchronously at startup, nor is there a guarantee that cache compilations are shared/persisted correctly across user environments. Solving this JIT compilation lag at the core `molsysmt` level is essential to unfreeze all sibling and downstream packages.

---

## Proposed Solution

To eliminate this dynamic lag, we propose introducing:

### 1. The Programmatic `molsysmt.warmup()` API
Introduce a clean, public function that executes a minimal dummy execution sequence. This triggers the JIT compilation of all core Numba-decorated geometry and topology functions (e.g., coordinate conversion, distance matrix calculators, atom grouping) without blocking user inputs.

```python
# molsysmt/warmup.py
import threading
import numpy as np

def _trigger_warmup():
    try:
        # Import core internal computational modules
        from molsysmt.basic import get
        # Execute a minimal, dummy operation (e.g. 1-atom coordinates conversion)
        # to trigger compilation of Numba-accelerated functions
        coords = np.zeros((1, 1, 3), dtype=np.float32)
        # Dynamic execution warms up type stubs and Numba caches
        # ...
    except Exception:
        pass

def warmup(async_mode=True):
    """
    Triggers dynamic compilation of core JIT-accelerated functions 
    and warms up cache systems.
    """
    if async_mode:
        thread = threading.Thread(target=_trigger_warmup, daemon=True, name="MolSysMTWarmup")
        thread.start()
    else:
        _trigger_warmup()
```

### 2. Persistent Numba Cache Configuration
Ensure that all `@numba.jit` decorated methods in MolSysMT are configured with `cache=True` to write compilation outputs to disk, ensuring that once warmed up, subsequent Python sessions load instantly.

We will document and expose a standard environment variable check to ensure compilation caches persist under a predictable path across distinct session startups:
```python
# molsysmt/config.py
import os
import tempfile

# Force a stable numba cache directory if none is defined,
# ensuring cache hits across distinct Jupyter/interactive instances
if "NUMBA_CACHE_DIR" not in os.environ:
    stable_cache = os.path.join(tempfile.gettempdir(), "molsysmt_numba_cache")
    os.makedirs(stable_cache, exist_ok=True)
    os.environ["NUMBA_CACHE_DIR"] = stable_cache
```

---

## Benefits

* **Smooth User Experience**: Third-party GUI or Jupyter applications (such as `molsysviewer`) can call `molsysmt.warmup(async_mode=True)` immediately at import time to compile Numba functions in the background, achieving instant responses on the user's first load.
* **Persistent Cache Gains**: Ensuring JIT files are cached on disk preserves compilation speedups across python session restarts.
* **Zero Core Impact**: The warming sequence is completely isolated and runs on a daemon background thread, causing no blocking to standard CLI usage.
