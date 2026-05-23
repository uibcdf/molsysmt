"""
GPU availability detection and use_gpu parameter resolution.

Public helpers
--------------
gpu_available()
    True when a CUDA-capable GPU is accessible via numba.cuda.

resolve_use_gpu(use_gpu_arg, payload_size)
    Resolves the per-call ``use_gpu`` argument against the global config flag
    and hardware availability, returning True/False.

Priority rules
--------------
* ``use_gpu=True``   — force GPU; emit warning and fall back if none available.
* ``use_gpu=False``  — force CPU.
* ``use_gpu='auto'`` — use GPU when a GPU is available AND payload_size >=
                       config.gpu_threshold.
* ``use_gpu=None``   — inherit entirely from config.use_gpu (default).

Design
------
``config.use_gpu = False`` (default) — CPU only.
``config.use_gpu = True``            — always GPU when available.
``config.use_gpu = 'auto'``          — GPU when payload threshold is met.

Per-call ``use_gpu=None`` inherits from config, so changing ``config.use_gpu``
is the global on/off switch.  Per-call values always override config.

Usage inside a public wrapper
------------------------------
    from molsysmt._private.gpu import resolve_use_gpu

    def get_rmsd(molecular_system, ..., use_gpu=None):
        ...
        payload = n_structures * n_atoms * 3
        if resolve_use_gpu(use_gpu, payload):
            from molsysmt.lib.structure.get_rmsd_cuda import get_rmsd as _kernel
        else:
            from molsysmt.lib.structure.get_rmsd import get_rmsd as _kernel
"""

from __future__ import annotations

_CUDA_AVAILABLE: bool | None = None  # cached after first probe


def gpu_available() -> bool:
    """Return True if a CUDA GPU is accessible via numba.cuda."""
    global _CUDA_AVAILABLE
    if _CUDA_AVAILABLE is None:
        try:
            from numba import cuda
            _CUDA_AVAILABLE = cuda.is_available()
        except Exception:
            _CUDA_AVAILABLE = False
    return _CUDA_AVAILABLE


def resolve_use_gpu(use_gpu_arg, payload_size: int = 0) -> bool:
    """
    Resolve whether to use the GPU kernel for this call.

    Priority:  per-call argument  >  config.use_gpu  >  False

    Parameters
    ----------
    use_gpu_arg : None | bool | 'auto'
        Value passed by the caller.  None means "inherit from config".
    payload_size : int
        Number of floating-point elements involved (used by 'auto' threshold).

    Returns
    -------
    bool
    """
    import molsysmt.configure as config

    # Determine effective setting
    global_use_gpu = getattr(config, 'gpu_mode', None)
    if global_use_gpu is None:
        global_use_gpu = getattr(config, 'use_gpu', False)

    effective = use_gpu_arg if use_gpu_arg is not None else global_use_gpu

    if effective is False:

        return False

    if effective is True:
        if not gpu_available():
            _warn_gpu_unavailable()
            return False
        return True

    if effective == 'auto':
        return gpu_available() and payload_size >= config.gpu_threshold

    # Unknown value — fall back silently
    return False


def _warn_gpu_unavailable() -> None:
    try:
        from molsysmt._private.smonitor import warn, GpuNotAvailableWarning
        warn(GpuNotAvailableWarning,
             message="use_gpu=True was requested but no CUDA GPU is available. "
                     "Falling back to CPU kernel.")
    except Exception:
        import warnings
        warnings.warn(
            "use_gpu=True was requested but no CUDA GPU is available. "
            "Falling back to CPU kernel.",
            RuntimeWarning,
            stacklevel=4,
        )
