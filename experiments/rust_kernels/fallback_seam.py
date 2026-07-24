"""Illustrative opt-in seam (item 3) — NOT added to molsysmt.

Shows how molsysmt would *optionally* use the Rust kernels when a prebuilt wheel is
present, transparently falling back to the existing Numba kernels otherwise. Nothing
in molsysmt imports `msm_rust_kernels`; this is only the pattern a future integration
would follow, gated by an explicit backend flag so behaviour stays testable and the
Numba path remains the oracle.
"""

try:
    import msm_rust_kernels as _rust
    HAVE_RUST = True
except Exception:  # pragma: no cover - absence is the normal, supported state
    _rust = None
    HAVE_RUST = False


def mic_distances_single_system(coordinates, box, backend="auto"):
    """MIC all-pairs distances, Rust when available else Numba.

    backend: 'auto' (Rust if the wheel is installed, else Numba), 'rust', or 'numba'.
    Results are identical (verified bit-for-bit in bench_production.py).
    """
    use_rust = HAVE_RUST if backend == "auto" else (backend == "rust")
    if use_rust:
        if _rust is None:
            raise RuntimeError("Rust backend requested but msm_rust_kernels is not installed.")
        return _rust.mic_distances_single_system(coordinates, box)
    from molsysmt.lib.structure.get_mic_distances import get_mic_distances_single_system
    return get_mic_distances_single_system(coordinates, box)


if __name__ == "__main__":
    import numpy as np
    print("HAVE_RUST =", HAVE_RUST)
    coords = np.random.default_rng(0).uniform(0, 3, size=(1, 200, 3))
    box = np.array([[[6.0, 0, 0], [0, 6.0, 0], [0, 0, 6.0]]])
    a = mic_distances_single_system(coords, box, backend="numba")
    if HAVE_RUST:
        b = mic_distances_single_system(coords, box, backend="rust")
        print("auto==rust and numba parity:", np.allclose(a, b, atol=1e-9))
