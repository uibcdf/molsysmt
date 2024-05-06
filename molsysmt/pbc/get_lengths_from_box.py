from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
from molsysmt import lib as msmlib

@digest()
def get_lengths_from_box(box, skip_digestion=False):
    """
    To be written soon...
    """

    box_value, box_unit  = puw.get_value_and_unit(box)
    lengths_value = msmlib.pbc.get_lengths_from_box(box_value)
    lengths = puw.quantity(lengths_value.round(6), box_unit)
    lengths = puw.standardize(lengths)

    return lengths

