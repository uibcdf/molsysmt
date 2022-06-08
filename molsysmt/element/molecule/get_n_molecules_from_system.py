from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
import numpy as np

def get_n_molecules_from_system(molecular_system, check=True):

    if check:

        digest_single_molecular_system(molecular_system)

    from . import get_molecule_index_from_atom

    molecule_index_from_atom = get_molecule_index_from_atom(molecular_system, check=True)

    if molecule_index_from_atom[0] is None:
        n_molecules = 0
    else:
        output = np.unique(molecule_index_from_atom)
        n_molecules = output.shape[0]

    return n_molecules
