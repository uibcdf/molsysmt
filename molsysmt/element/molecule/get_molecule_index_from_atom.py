from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
import numpy as np

def get_molecule_index_from_atom(molecular_system, indices='all', check=True):

    if check:

        digest_single_molecular_system(molecular_system)
        indices = digest_indices(indices)

    from molsysmt.basic import get

    output = get(molecular_system, element='atom', indices=indices, component_index=True)

    return output

