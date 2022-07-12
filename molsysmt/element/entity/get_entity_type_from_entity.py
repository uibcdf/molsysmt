from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from molsysmt._private.variables import is_all
import numpy as np

def get_entity_type_from_entity(molecular_system, indices='all', check=True):

    if check:

        digest_single_molecular_system(molecular_system)
        indices = digest_indices(indices)

    from .get_entity_all_from_atom import get_entity_all_from_atom

    entity_index_from_atom, _, entity_type_from_atom = get_entity_all_from_atom(molecular_system,
            check=False)

    if is_all(indices):
        indices = np.unique(entity_index_from_atom)

    output=[]
    for ii in indices:
        atom_index = np.where(entity_index_from_atom==ii)[0][0]
        output.append(entity_type_from_atom[atom_index])

    output = np.array(output, dtype=object)

    return output


