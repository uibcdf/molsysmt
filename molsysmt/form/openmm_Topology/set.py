from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw

## System

@digest(form='openmm.Topology')
def set_box_to_system(item, structure_indices='all', value=None):

    box = puw.convert(value, to_unit='nanometers', to_form='openmm.unit')

    n_structures = box.shape[0]

    if n_structures == 1:

        item.setPeriodicBoxVectors(box[0])

    else:

        raise ValueError("The box to set in to a openmm.Topology has more than a frame")

    pass

