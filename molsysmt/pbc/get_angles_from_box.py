from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
from molsysmt import lib as msmlib

@digest()
def get_angles_from_box(box):

    box_value, box_unit  = puw.get_value_and_unit(box)
    angles_value = msmlib.pbc.get_angles_from_box(box_value)
    angles = puw.quantity(angles.round(6), 'radians')


    return angles

