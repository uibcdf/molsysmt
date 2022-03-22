from .is_openmm_Topology import is_openmm_Topology
from molsysmt._private.exceptions import WrongFormError, WrongIndicesError, WrongStructureIndicesError
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.indices import digest_indices
from molsysmt._private.structure_indices import digest_structure_indices
from molsysmt._private.box import digest_box
from molsysmt import puw

## System

def set_box_to_system(item, structure_indices='all', value=None, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

        try:
            box = digest_box(value)
        except:
            raise WrongStructureIndicesError()

    box = puw.convert(value, to_unit='nanometers', to_form='openmm.unit')

    n_structures = box.shape[0]

    if n_structures == 1:

        item.setPeriodicBoxVectors(box[0])

    else:

        raise ValueError("The box to set in to a openmm.Topology has more than a frame")

    pass

