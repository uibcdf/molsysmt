from molsysmt._private.digestion import digest_item as _digest_item
from molsysmt._private.digestion import digest_structure_indices as _digest_structure_indices
from molsysmt._private.digestion import digest_box as _digest_box
from molsysmt import puw as _puw

## System

def set_box_to_system(item, structure_indices='all', value=None):

    if check:

        _digest_item(item, 'openmm.Topology')
        structure_indices = _digest_structure_indices(structure_indices)
        box = _digest_box(value)

    box = _puw.convert(value, to_unit='nanometers', to_form='openmm.unit')

    n_structures = box.shape[0]

    if n_structures == 1:

        item.setPeriodicBoxVectors(box[0])

    else:

        raise ValueError("The box to set in to a openmm.Topology has more than a frame")

    pass

