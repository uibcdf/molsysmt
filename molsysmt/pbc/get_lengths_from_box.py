from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
from molsysmt import lib as msmlib

@digest()
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

    box_value, box_unit  = puw.get_value_and_unit(box)
    lengths_value = msmlib.pbc.get_lengths_from_box(box_value)
    lengths = puw.quantity(lengths_value.round(6), box_unit)
    lengths = puw.standardize(lengths)

    return lengths
