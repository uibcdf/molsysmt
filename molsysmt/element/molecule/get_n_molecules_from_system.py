from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_n_molecules_from_system(molecular_system, digest=True):

    from . import get_molecule_index_from_atom

    molecule_index_from_atom = get_molecule_index_from_atom(molecular_system, digest=False)

    if molecule_index_from_atom[0] is None:
        n_molecules = 0
    else:
        output = np.unique(molecule_index_from_atom)
        n_molecules = output.shape[0]

    return n_molecules
