import numpy as np

from molsysmt._private.smonitor import ArgumentError


def digest_donors(donors, syntax="MolSysMT", caller=None):
    """Normalize explicit donor anchors or intact donor-H rows without coercion."""
    if donors is None:
        return None
    try:
        if hasattr(donors, "unit") or hasattr(donors, "units"):
            raise ValueError
        array = np.asarray(donors)
        if array.ndim == 0:
            array = array.reshape(1)
        mixed_boolean = isinstance(donors, (list, tuple)) and any(
            isinstance(value, (bool, np.bool_))
            for value in np.asarray(donors, dtype=object).flat
        )
        valid_shape = array.ndim == 1 or (array.ndim == 2 and array.shape[1] == 2)
        if valid_shape and not mixed_boolean:
            if not array.size:
                return np.empty(array.shape, dtype=np.int64)
            if (
                array.dtype.kind in "iu"
                and np.all(array >= 0)
                and np.all(array < 2**63)
            ):
                return array.astype(np.int64)
    except (TypeError, ValueError, OverflowError):
        pass

    raise ArgumentError(
        "donors",
        value=donors,
        caller=caller,
        message="Supply integer donor atom indices or an (n, 2) array of donor-H pairs.",
    )
