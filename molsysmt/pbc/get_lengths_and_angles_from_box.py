from molsysmt._private.digestion import arg_digest
from molsysmt import pyunitwizard as puw
from molsysmt import lib as msmlib

@arg_digest()
def get_lengths_and_angles_from_box(box, skip_digestion=False):
    """Return box lengths and angles from a 3x3 box matrix or an array of boxes.

    Parameters
    ----------
    box : array-like
        A single box with shape (3, 3) or an array of boxes with shape (n, 3, 3).
        Vectors correspond to the three box edges: v0, v1, v2.

    Returns
    -------
    lengths, angles
        - lengths: |v0|, |v1|, |v2| in the same units as the input (often labeled
          as a, b, c in other libraries/software).
        - angles: (alpha, beta, gamma) in radians where:
            alpha = angle between v1 and v2,
            beta  = angle between v0 and v2,
            gamma = angle between v0 and v1.
          This matches the conventional nomenclature (alpha between b and c,
          beta between a and c, gamma between a and b).
    .. versionadded:: 1.0.0
    """

    box_value, box_unit  = puw.get_value_and_unit(box)
    lengths_value, angles_value = msmlib.pbc.get_lengths_and_angles_from_box(box_value)
    lengths = puw.quantity(lengths_value.round(6), box_unit)
    lengths = puw.standardize(lengths)
    angles = puw.quantity(angles_value.round(6), 'radians')
    angles = puw.standardize(angles)

    return lengths, angles
