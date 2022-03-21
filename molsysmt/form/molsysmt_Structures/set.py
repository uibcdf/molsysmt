from .is_molsysmt_Structures import is_molsysmt_Structures
from molsysmt._private.exceptions import WrongFormError, WrongIndicesError, WrongStructureIndicesError
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.indices import digest_indices
from molsysmt._private.structure_indices import digest_structure_indices

###### Set

## System

def set_box_to_system(item, indices='all', structure_indices='all', value=None, check=True):

    if check:

        try:
            is_molsysmt_Structures(item)
        except:
            raise WrongFormError('molsysmt.Structures')

        try:
            indices = digest_indices(indices)
        except:
            raise WrongIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    n_structures_trajectory = item.coordinates.shape[0]
    n_structures_box = value.shape[0]

    if n_structures_trajectory == n_structures_box:
        item.box = value
    else:
        if n_structures_box == 1:
            item.box = np.broadcast_to(value[0]._value, (n_structures_trajectory,3,3)) * value.unit
        else:
            raise ValueError("box and coordinates have different shape")

    pass

