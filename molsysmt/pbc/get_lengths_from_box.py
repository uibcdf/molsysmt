from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw
from molsysmt._private import rust_backend as _kernels
import numpy as np

@arg_digest()
def get_lengths_from_box(box, skip_digestion=False):
    """
    Extracting box edge lengths from a box matrix.

    Parameters
    ----------
    box : quantity
        Box matrix (single or array), shape (3, 3) or (n, 3, 3).
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    quantity
        Edge lengths (a, b, c) in the same units as the input.

    .. versionadded:: 1.0.0
    """

    if isinstance(box, np.ndarray):
        box_value = box
        box_unit = puw.unit('nm')
    else:
        box_value, box_unit  = puw.get_value_and_unit(box)
    lengths_value = _kernels.get_lengths_from_box(np.asarray(box_value, dtype=np.float64))
    lengths = puw.quantity(lengths_value.round(6), box_unit)
    lengths = puw.standardize(lengths)

    return lengths
