"""Block 2 benchmark: neighbor_list_csr_multi — Rust (rayon) vs Numba (prange).

Both are parallel; Numba's parallelism is gated by configure.parallel_mode /
parallel_threshold, Rust's rayon is not. Reports parity + cold/warm.
"""

import math
import time
import warnings

warnings.filterwarnings("ignore")

import numpy as np
import molsysmt.configure as config
from molsysmt._private import rust_backend as rb


def best(fn, repeats=3, **kw):
    b = math.inf
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn(**kw)
        b = min(b, time.perf_counter() - t0)
    return b


rng = np.random.default_rng(7)
ORTHO = np.array([[[6.0, 0.0, 0.0], [0.0, 6.0, 0.0], [0.0, 0.0, 6.0]]])

print(f"{'case':28s} {'parity':7s} {'COLD nb':>10s} {'COLD rs':>9s} {'WARM nb':>9s} {'WARM rs':>9s}")
print("-" * 82)

for ns, na, label in ((1, 8000, "1 struct x 8000"), (50, 2000, "50 struct x 2000")):
    q = np.ascontiguousarray(rng.uniform(0.0, 6.0, size=(ns, na, 3)))
    b = np.repeat(ORTHO, ns, axis=0)
    kw = dict(query_coords=q, box=b, cutoff=0.6, exclude_self=True, sort_by_distance=True)

    t0 = time.perf_counter(); out_nb = rb.neighbor_list_csr_multi(**kw, backend="numba"); t1 = time.perf_counter()
    t2 = time.perf_counter(); out_rs = rb.neighbor_list_csr_multi(**kw, backend="rust"); t3 = time.perf_counter()
    parity = (np.array_equal(out_nb[0], out_rs[0]) and np.array_equal(out_nb[1], out_rs[1])
              and np.allclose(out_nb[2], out_rs[2], atol=1e-9))

    wnb = best(rb.neighbor_list_csr_multi, **kw, backend="numba")
    wrs = best(rb.neighbor_list_csr_multi, **kw, backend="rust")
    print(f"{label:28s} {str(parity):7s} {(t1-t0)*1000:9.1f}ms {(t3-t2)*1000:8.1f}ms "
          f"{wnb*1000:8.1f}ms {wrs*1000:8.1f}ms")

print(f"\n(numba parallel_mode={config.parallel_mode}, parallel_threshold={config.parallel_threshold})")
print("DONE")
