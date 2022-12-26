from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np

@digest()
def get_component_index_from_atom(molecular_system, indices='all', digest=True):

    from molsysmt.basic import get
    from molsysmt.lib import bonds as _libbonds

    n_atoms, n_bonds = get(molecular_system, element='system', n_atoms=True, n_bonds=True, digest=False)

    if n_bonds==0:

        output = np.full(n_atoms, None, dtype=object)

    else:

        atoms_indices = get(molecular_system, element='bond', indices='all', atom_index=True, digest=False)

        output = _libbonds.component_indices(atoms_indices, n_atoms, n_bonds)
        output = np.ascontiguousarray(output, dtype=int)

    if not is_all(indices):

        output = output[indices]

    return output

