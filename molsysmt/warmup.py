import sys
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.jit import compile_registered


def warmup(numba=True, modules=True, skip_digestion=False):
    """
    Precompiling Numba kernels and forcing lazy imports to avoid first-use latency.

    Parameters
    ----------
    numba : bool, default True
        Whether to compile registered Numba JIT kernels.
    modules : bool, default True
        Whether to force load all lazy-loaded submodules and attributes.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    int
        Number of kernels compiled during the warmup (or 0 if numba=False).

    Notes
    -----
    This function triggers pre-compilation and module preloading to ensure
    maximum performance during subsequent calls in timing-sensitive workflows.

    .. versionadded:: 1.0.0
    """
    if modules:
        import molsysmt
        # Force resolution of all lazy attributes to warm up the lazy-loading registry
        if hasattr(molsysmt, "_LAZY_ATTRIBUTES"):
            for attr in molsysmt._LAZY_ATTRIBUTES:
                try:
                    getattr(molsysmt, attr)
                except Exception:
                    pass

    if numba:
        from molsysmt import lib as _lib
        _ = (_lib.math, _lib.series, _lib.pbc, _lib.structure, _lib.topology)
        return compile_registered()

    return 0


def warmup_numba(skip_digestion=False):
    """
    Deprecated alias for warmup.

    .. deprecated:: 1.0.0
        Use molsysmt.warmup() instead.
    """
    from molsysmt._private.smonitor import warn_once
    warn_once(
        "molsysmt.warmup_numba() is deprecated and will be removed in a future version. "
        "Use molsysmt.warmup() instead."
    )
    return warmup(numba=True, modules=True, skip_digestion=skip_digestion)
