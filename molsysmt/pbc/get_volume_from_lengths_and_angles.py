from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest()
def get_volume_from_lengths_and_angles(box_lengths, box_angles):

    from .get_box_from_lengths_and_angles import get_box_from_lengths_and_angles
    from .get_volume_from_box import get_volume_from_box

    box = get_box_from_lengths_and_angles(box_lengths, box_angles)

    return get_volume_from_box(box)

