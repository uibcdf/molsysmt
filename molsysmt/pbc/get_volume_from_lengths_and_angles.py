from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest()
def get_volume_from_lengths_and_angles(box_lengths, box_angles):
    """
    Computing box volume from lengths and angles.

    Parameters
    ----------
    box_lengths : quantity
        Edge lengths (a, b, c).
    box_angles : quantity
        Angles (alpha, beta, gamma).

    Returns
    -------
    quantity
        Volume in cubic length units.

    .. versionadded:: 1.0.0
    """

    from .get_box_from_lengths_and_angles import get_box_from_lengths_and_angles
    from .get_volume_from_box import get_volume_from_box

    box = get_box_from_lengths_and_angles(box_lengths, box_angles)

    return get_volume_from_box(box)
