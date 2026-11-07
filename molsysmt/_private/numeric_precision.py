"""Resolve the native working dtype independently of coordinate publication."""

import numpy as np


def native_float_dtype():
    """Return the supported CPU dtype and diagnose an unavailable arithmetic request."""
    import molsysmt.configure as config
    from molsysmt._private.argdigest.argument.precision import digest_precision
    from molsysmt._private.smonitor import PrecisionFallbackWarning, warn

    requested = digest_precision(
        config.precision, caller="molsysmt.configure.precision"
    )
    if requested == "single":
        warn(
            PrecisionFallbackWarning(
                requested_precision=requested,
                effective_precision="float64",
                backend="MolSysMT native CPU",
            ),
            stacklevel=3,
        )
    return np.float64
