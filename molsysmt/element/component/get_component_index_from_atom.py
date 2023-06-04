from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np

@digest()
def get_component_index_from_atom(molecular_system, indices='all'):

    from molsysmt.basic import get
    from molsysmt.element.component import get_component_index_from_bonded_atoms

    n_atoms, n_bonds = get(molecular_system, element='system', n_atoms=True, n_bonds=True)

    if n_bonds==0:

        output = np.full(n_atoms, None, dtype=object)

    else:

        atoms_indices = get(molecular_system, element='bond', indices='all', bonded_atoms=True)

        output = get_component_index_from_bonded_atoms(atoms_indices, n_atoms)

    if not is_all(indices):

        output = output[indices]

    return output

