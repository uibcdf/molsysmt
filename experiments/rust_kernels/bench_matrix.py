"""Benchmark matrix: Rust vs Numba across different computational profiles.

Profiles exercised:
  1. regular arithmetic  O(N^2)   -> pairwise squared distances
  2. transcendental      O(N^2)   -> Coulomb-like potential (sqrt + division)
  3. transcendental //   O(N^2)   -> parallel Coulomb (rayon vs numba prange)
  4. branchy/irregular   ~O(N)    -> cell-list neighbour counts

Reports per (kernel, N): parity, COLD (first call; Numba pays JIT), WARM (best of N).
Also the aggregate cold cost across kernels (the cumulative warmup story) and a
parallel-scaling comparison.
"""

import math
import time

import numpy as np
import numba as nb

import msm_rust_kernels as rust


def best(func, *args, repeats=5):
    b = math.inf
    for _ in range(repeats):
        t0 = time.perf_counter()
        func(*args)
        b = min(b, time.perf_counter() - t0)
    return b


def cold(func, *args):
    t0 = time.perf_counter()
    func(*args)
    return time.perf_counter() - t0


# ---------------------------------------------------------------- Numba baselines
@nb.njit(cache=False)
def pairwise_nb(c):
    n = c.shape[0]
    out = np.empty((n, n))
    for i in range(n):
        xi, yi, zi = c[i, 0], c[i, 1], c[i, 2]
        for j in range(n):
            dx = xi - c[j, 0]; dy = yi - c[j, 1]; dz = zi - c[j, 2]
            out[i, j] = dx * dx + dy * dy + dz * dz
    return out


@nb.njit(cache=False)
def coulomb_nb(c, q):
    n = c.shape[0]
    out = np.zeros(n)
    for i in range(n):
        xi, yi, zi = c[i, 0], c[i, 1], c[i, 2]
        s = 0.0
        for j in range(n):
            if i == j:
                continue
            dx = xi - c[j, 0]; dy = yi - c[j, 1]; dz = zi - c[j, 2]
            s += q[j] / math.sqrt(dx * dx + dy * dy + dz * dz)
        out[i] = s
    return out


@nb.njit(parallel=True, cache=False)
def coulomb_nb_parallel(c, q):
    n = c.shape[0]
    out = np.zeros(n)
    for i in nb.prange(n):
        xi, yi, zi = c[i, 0], c[i, 1], c[i, 2]
        s = 0.0
        for j in range(n):
            if i == j:
                continue
            dx = xi - c[j, 0]; dy = yi - c[j, 1]; dz = zi - c[j, 2]
            s += q[j] / math.sqrt(dx * dx + dy * dy + dz * dz)
        out[i] = s
    return out


@nb.njit(cache=False)
def neighbor_counts_nb(c, cutoff):
    n = c.shape[0]
    cutoff_sq = cutoff * cutoff
    xmin = c[:, 0].min(); xmax = c[:, 0].max()
    ymin = c[:, 1].min(); ymax = c[:, 1].max()
    zmin = c[:, 2].min(); zmax = c[:, 2].max()
    lx = max(cutoff, xmax - xmin + 1e-5)
    ly = max(cutoff, ymax - ymin + 1e-5)
    lz = max(cutoff, zmax - zmin + 1e-5)
    nx = max(1, int(math.floor(lx / cutoff)))
    ny = max(1, int(math.floor(ly / cutoff)))
    nz = max(1, int(math.floor(lz / cutoff)))
    dx = lx / nx; dy = ly / ny; dz = lz / nz
    head = np.full(nx * ny * nz, -1, dtype=np.int64)
    nxt = np.full(n, -1, dtype=np.int64)
    for a in range(n):
        cx = min(nx - 1, max(0, int((c[a, 0] - xmin) / dx)))
        cy = min(ny - 1, max(0, int((c[a, 1] - ymin) / dy)))
        cz = min(nz - 1, max(0, int((c[a, 2] - zmin) / dz)))
        cc = cx + nx * (cy + ny * cz)
        nxt[a] = head[cc]; head[cc] = a
    out = np.zeros(n, dtype=np.int64)
    for i in range(n):
        cx = min(nx - 1, max(0, int((c[i, 0] - xmin) / dx)))
        cy = min(ny - 1, max(0, int((c[i, 1] - ymin) / dy)))
        cz = min(nz - 1, max(0, int((c[i, 2] - zmin) / dz)))
        cnt = 0
        for ox in range(max(0, cx - 1), min(nx, cx + 2)):
            for oy in range(max(0, cy - 1), min(ny, cy + 2)):
                for oz in range(max(0, cz - 1), min(nz, cz + 2)):
                    cc = ox + nx * (oy + ny * oz)
                    j = head[cc]
                    while j != -1:
                        if j != i:
                            ddx = c[i, 0] - c[j, 0]; ddy = c[i, 1] - c[j, 1]; ddz = c[i, 2] - c[j, 2]
                            if ddx * ddx + ddy * ddy + ddz * ddz <= cutoff_sq:
                                cnt += 1
                        j = nxt[j]
        out[i] = cnt
    return out


rng = np.random.default_rng(0)
cold_numba_total = 0.0
cold_rust_total = 0.0

print(f"{'kernel (profile)':38s} {'N':>6s}  parity   {'COLD nb':>9s} {'COLD rs':>9s}   {'WARM nb':>8s} {'WARM rs':>8s}")
print("-" * 100)


def row(label, n, parity, cnb, crs, wnb, wrs):
    global cold_numba_total, cold_rust_total
    cold_numba_total += cnb
    cold_rust_total += crs
    print(f"{label:38s} {n:6d}  {str(parity):5s}   {cnb*1000:8.1f} {crs*1000:8.1f}   {wnb*1000:7.2f} {wrs*1000:7.2f}")


first = True
for n in (500, 2000, 4000):
    c = np.ascontiguousarray(rng.uniform(0, 3, size=(n, 3)))
    q = np.ascontiguousarray(rng.uniform(-1, 1, size=n))
    # regular arithmetic
    if first:
        cnb = cold(pairwise_nb, c); crs = cold(rust.pairwise_sqdistances, c)
    else:
        cnb = crs = 0.0
    p = np.allclose(pairwise_nb(c), rust.pairwise_sqdistances(c), atol=1e-9)
    row("pairwise_sqdist (regular)", n, p, cnb, crs, best(pairwise_nb, c), best(rust.pairwise_sqdistances, c))
    # transcendental
    if first:
        cnb = cold(coulomb_nb, c, q); crs = cold(rust.coulomb_potential, c, q)
    else:
        cnb = crs = 0.0
    p = np.allclose(coulomb_nb(c, q), rust.coulomb_potential(c, q), atol=1e-9)
    row("coulomb (transcendental)", n, p, cnb, crs, best(coulomb_nb, c, q), best(rust.coulomb_potential, c, q))
    first = False

# branchy / irregular, larger N
for n in (5000, 20000):
    c = np.ascontiguousarray(rng.uniform(0, 6, size=(n, 3)))
    cnb = cold(neighbor_counts_nb, c, 0.5) if n == 5000 else 0.0
    crs = cold(rust.neighbor_counts, c, 0.5) if n == 5000 else 0.0
    p = np.array_equal(neighbor_counts_nb(c, 0.5), rust.neighbor_counts(c, 0.5))
    row("neighbor_counts (branchy)", n, p, cnb, crs,
        best(neighbor_counts_nb, c, 0.5), best(rust.neighbor_counts, c, 0.5))

print("-" * 100)
print(f"AGGREGATE COLD across distinct kernels:  numba(JIT)={cold_numba_total*1000:8.1f} ms   "
      f"rust(AOT)={cold_rust_total*1000:8.1f} ms")

# ---------------------------------------------------------------- parallel scaling
print("\nParallel scaling (Coulomb, N=4000, transcendental):")
c = np.ascontiguousarray(rng.uniform(0, 3, size=(4000, 3)))
q = np.ascontiguousarray(rng.uniform(-1, 1, size=4000))
nb.set_num_threads(nb.config.NUMBA_NUM_THREADS)
# warm both parallels
coulomb_nb_parallel(c, q); rust.coulomb_potential_parallel(c, q)
p = np.allclose(coulomb_nb_parallel(c, q), rust.coulomb_potential_parallel(c, q), atol=1e-9)
serial_nb = best(coulomb_nb, c, q)
par_nb = best(coulomb_nb_parallel, c, q)
serial_rs = best(rust.coulomb_potential, c, q)
par_rs = best(rust.coulomb_potential_parallel, c, q)
print(f"  parity(parallel)={p}   threads={nb.get_num_threads()}")
print(f"  serial:   numba={serial_nb*1000:7.2f} ms   rust={serial_rs*1000:7.2f} ms")
print(f"  parallel: numba={par_nb*1000:7.2f} ms   rust={par_rs*1000:7.2f} ms   "
      f"(speedup nb={serial_nb/par_nb:.1f}x, rs={serial_rs/par_rs:.1f}x)")
print("DONE")
