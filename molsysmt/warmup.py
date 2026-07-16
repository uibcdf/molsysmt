import warnings

from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.jit import compile_registered
from molsysmt._private.smonitor import LibraryNotFoundError, WarmupFailureWarning


@arg_digest()
def warmup(
    numba=True,
    modules=True,
    strict=False,
    return_report=False,
    skip_digestion=False,
):
    """
    Precompiling Numba kernels and forcing lazy imports to avoid first-use latency.

    Parameters
    ----------
    numba : bool, default True
        Whether to compile registered Numba JIT kernels.
    modules : bool, default True
        Whether to force load all lazy-loaded submodules and attributes.
    strict : bool, default False
        Whether to propagate an unexpected lazy-loading failure immediately.
        Missing optional dependencies remain reported as skipped capabilities.
    return_report : bool, default False
        Whether to return a structured report instead of only the number of
        compiled kernels.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    int or dict
        Number of compiled kernels by default. If ``return_report=True``, a
        dictionary containing ``compiled_kernels``, ``loaded_attributes``,
        ``skipped_attributes``, and ``failures``.

    Notes
    -----
    This function triggers pre-compilation and module preloading to ensure
    maximum performance during subsequent calls in timing-sensitive workflows.

    .. versionadded:: 1.0.0
    """
    report = {
        "compiled_kernels": 0,
        "loaded_attributes": [],
        "skipped_attributes": [],
        "failures": [],
    }

    if modules:
        import molsysmt
        # Force resolution of all lazy attributes to warm up the lazy-loading registry
        if hasattr(molsysmt, "_LAZY_ATTRIBUTES"):
            for attr in molsysmt._LAZY_ATTRIBUTES:
                try:
                    getattr(molsysmt, attr)
                except LibraryNotFoundError as error:
                    report["skipped_attributes"].append({
                        "attribute": attr,
                        "error_type": type(error).__name__,
                        "reason": str(error),
                    })
                except Exception as error:
                    failure = {
                        "attribute": attr,
                        "error_type": type(error).__name__,
                        "reason": str(error),
                    }
                    report["failures"].append(failure)
                    if strict:
                        raise
                    warnings.warn(
                        WarmupFailureWarning(**failure),
                        stacklevel=2,
                    )
                else:
                    report["loaded_attributes"].append(attr)

    if numba:
        from molsysmt import lib as _lib
        _ = (_lib.math, _lib.series, _lib.pbc, _lib.structure, _lib.topology)
        report["compiled_kernels"] = compile_registered()

    if return_report:
        return report
    return report["compiled_kernels"]


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
