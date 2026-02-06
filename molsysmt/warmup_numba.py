from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.jit import compile_registered


@arg_digest()
def warmup_numba(skip_digestion=False):
    """
    Precompiling Numba kernels to avoid first-use latency.

    Parameters
    ----------
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    int
        Number of kernels compiled during the warmup.

    Notes
    -----
    This function triggers compilation of all registered Numba kernels. The
    first call may take time, but subsequent calls are fast.

    .. versionadded:: 1.0.0
    """

    from molsysmt import lib as _lib

    _ = (_lib.math, _lib.series, _lib.pbc, _lib.structure)

    return compile_registered()
