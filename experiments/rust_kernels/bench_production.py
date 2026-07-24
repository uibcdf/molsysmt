"""Item 1: port ONE real production Numba kernel and validate on real data.

Target: molsysmt.lib.structure.get_mic_distances.get_mic_distances_single_system
(all-pairs minimum-image distances per structure; orthogonal + triclinic with the
27-image refinement). Compares parity + cold/warm against the Rust port on real
MolSysMT coordinates.
"""

import math
import time
import warnings

warnings.filterwarnings("ignore")

import numpy as np
import molsysmt as msm
from molsysmt import lib as msmlib
from molsysmt import systems

import msm_rust_kernels as rust

puw = msm.pyunitwizard


def best(func, *args, repeats=5):
    b = math.inf
    for _ in range(repeats):
        t0 = time.perf_counter()
        func(*args)
        b = min(b, time.perf_counter() - t0)
    return b


# Real coordinates from a periodic MolSysMT system, trimmed for a reasonable N.
m = msm.convert(systems["pentalanine"]["traj_pentalanine.h5msm"], to_form="molsysmt.MolSys")
m = msm.extract(m, structure_indices=[0])
coords = np.ascontiguousarray(puw.get_value(msm.get(m, coordinates=True), "nm"), dtype=np.float64)
# Replicate atoms to reach a meaningful N for warm timing (real coordinates, shifted).
reps = 24  # 62 * 24 = 1488 atoms
big = np.concatenate([coords[0] + np.array([0.11 * i, 0.07 * i, 0.05 * i]) for i in range(reps)], axis=0)
coords = big[np.newaxis, :, :].copy()
n_atoms = coords.shape[1]

ortho_box = np.array([[[6.0, 0.0, 0.0], [0.0, 6.0, 0.0], [0.0, 0.0, 6.0]]], dtype=np.float64)
tric_box = np.array([[[6.0, 0.0, 0.0], [1.2, 6.0, 0.0], [0.8, 0.6, 6.0]]], dtype=np.float64)

prod = msmlib.structure.get_mic_distances_single_system

print(f"Production kernel: get_mic_distances_single_system   N_atoms={n_atoms}  (1 structure)")
print("-" * 78)
for name, box in (("orthogonal", ortho_box), ("triclinic", tric_box)):
    # cold: first call of each (Numba compiles here)
    t0 = time.perf_counter(); nb_out = prod(coords, box); t1 = time.perf_counter()
    t2 = time.perf_counter(); rs_out = rust.get_mic_distances_single_system(coords, box); t3 = time.perf_counter()
    parity = np.allclose(nb_out, rs_out, atol=1e-9)
    maxdiff = float(np.max(np.abs(nb_out - rs_out)))
    wnb = best(prod, coords, box)
    wrs = best(rust.get_mic_distances_single_system, coords, box)
    print(f"{name:11s}  parity={parity}  max|diff|={maxdiff:.1e}   "
          f"COLD nb={ (t1-t0)*1000:8.1f}ms rs={ (t3-t2)*1000:7.1f}ms   "
          f"WARM nb={ wnb*1000:7.2f}ms rs={ wrs*1000:7.2f}ms")
print("DONE")
