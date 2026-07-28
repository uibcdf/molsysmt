"""Compatibility policy for the retired experimental GPU backends.

MolSysMT 1.0 uses the bundled Rust CPU kernels exclusively. Public arguments
related to GPU execution remain accepted while the future Rust GPU design is
evaluated, but they never select an unsupported implementation.
"""

from __future__ import annotations


def gpu_available() -> bool:
    """Returning whether a supported MolSysMT GPU backend is available."""
    return False


def resolve_use_gpu(use_gpu_arg, payload_size: int = 0) -> bool:
    """Resolving GPU requests to the supported CPU implementation."""
    import molsysmt.configure as config

    effective = use_gpu_arg
    if effective is None:
        effective = getattr(config, "gpu_mode", False)

    if effective is True:
        _warn_gpu_unavailable()
    return False


def _warn_gpu_unavailable() -> None:
    import warnings

    try:
        from molsysmt._private.smonitor import GpuNotAvailableWarning

        warnings.warn(
            GpuNotAvailableWarning(
                reason="MolSysMT 1.0 has no supported GPU kernel backend"
            ),
            stacklevel=4,
        )
    except Exception:
        warnings.warn(
            "GPU acceleration is not supported by this MolSysMT release. "
            "Falling back to the Rust CPU kernel.",
            RuntimeWarning,
            stacklevel=4,
        )
