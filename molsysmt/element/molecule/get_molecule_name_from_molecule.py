from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from molsysmt._private.arguments import *
import numpy as np

def get_molecule_name_from_molecule(molecular_system, indices='all', check=True):

    if check:

        digest_single_molecular_system(molecular_system)
        indices = digest_indices(indices)

    from . import get_n_molecules_from_system

    if is_all(indices):
        n_molecules = get_n_molecules_from_system(molecular_system, check=False)
        output = np.full(n_molecules, None, dtype=object)
    else:
        output = np.full(indices.shape[0], None, dtype=object)

    return output

