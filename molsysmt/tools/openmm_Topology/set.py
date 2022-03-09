from .is_openmm_Topology import is_openmm_Topology
from molsysmt._private_tools.exceptions import WrongFormError, WrongIndicesError, WrongStructureIndicesError
from molsysmt._private_tools.exceptions import NotImplementedMethodError
from molsysmt._private_tools.indices import digest_indices
from molsysmt._private_tools.structure_indices import digest_structure_indices

def set_box_to_system(item, structure_indices='all', value=None, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    value = puw.convert(value, 'nanometers', to_form='openmm.unit')

    n_structures = value.shape[0]

    if n_structures == 1:

        item.setPeriodicBoxVectors(value[0])

    else:

        raise ValueError("The box to set in to a openmm.Topology has corresponds to more than a frame")

    pass

