"""Parity + warm/cold timing: Rust kernels vs their Python/Numba equivalents.

Run inside the worktree after building the MolSysMT extension. The headline of the
Numba-replacement pilot is the COLD column: Numba pays a JIT-compilation cost on
the first call, Rust (AOT) does not.
"""

import math
import time

import numpy as np
import numba as nb

import molsysmt._rust as rust


def _min_time(func, *args, repeats=5):
    best = math.inf
    for _ in range(repeats):
        t0 = time.perf_counter()
        func(*args)
        best = min(best, time.perf_counter() - t0)
    return best


# ---------------------------------------------------------------------------
# 1. Fibonacci sphere points (pure-Python baseline -> parity only)
# ---------------------------------------------------------------------------
def fibonacci_py(n_points):
    golden = (1.0 + math.sqrt(5.0)) / 2.0
    pts = []
    for i in range(n_points):
        theta = math.acos(1.0 - 2.0 * (i + 0.5) / n_points)
        phi = 2.0 * math.pi * i / golden
        pts.append([math.sin(theta) * math.cos(phi),
                    math.sin(theta) * math.sin(phi),
                    math.cos(theta)])
    return np.array(pts, dtype=np.float64)

py = fibonacci_py(240)
rs = rust.fibonacci_sphere_points(240)
print(f"fibonacci_sphere_points  parity={np.allclose(py, rs, atol=1e-12)}  "
      f"max|diff|={np.max(np.abs(py - rs)):.2e}")


# ---------------------------------------------------------------------------
# 2. All-pairs squared distances (Numba njit baseline -> parity + cold/warm)
# ---------------------------------------------------------------------------
@nb.njit(cache=False)  # cache=False -> a genuine cold JIT compile on first call
def pairwise_sqdist_numba(c):
    n = c.shape[0]
    out = np.empty((n, n), dtype=np.float64)
    for i in range(n):
        xi = c[i, 0]; yi = c[i, 1]; zi = c[i, 2]
        for j in range(n):
            dx = xi - c[j, 0]; dy = yi - c[j, 1]; dz = zi - c[j, 2]
            out[i, j] = dx * dx + dy * dy + dz * dz
    return out


rng = np.random.default_rng(0)
coords = np.ascontiguousarray(rng.uniform(0.0, 3.0, size=(2000, 3)))

# COLD: first call of each (Numba compiles here; Rust is already AOT-compiled).
t0 = time.perf_counter(); nb_cold = pairwise_sqdist_numba(coords); t1 = time.perf_counter()
t2 = time.perf_counter(); rs_cold = rust.pairwise_sqdistances(coords); t3 = time.perf_counter()

print(f"pairwise_sqdistances     parity={np.allclose(rs_cold, nb_cold, atol=1e-9)}  "
      f"max|diff|={np.max(np.abs(rs_cold - nb_cold)):.2e}")

# WARM: best of several after both are hot.
nb_warm = _min_time(pairwise_sqdist_numba, coords)
rs_warm = _min_time(rust.pairwise_sqdistances, coords)

print(f"  N=2000  COLD  numba(JIT)={ (t1 - t0) * 1000:9.1f} ms   rust={ (t3 - t2) * 1000:9.1f} ms")
print(f"  N=2000  WARM  numba     ={ nb_warm * 1000:9.1f} ms   rust={ rs_warm * 1000:9.1f} ms")
print("DONE")
