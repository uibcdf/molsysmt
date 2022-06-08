from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
import numpy as np

def get_n_components_from_system(molecular_system, check=True):

    if check:

        digest_single_molecular_system(molecular_system)

    from . import get_component_index_from_atom

    component_index_from_atom = get_component_index_from_atom(molecular_system, indices='all', check=False)

    if component_index_from_atom[0] is None:
        n_components = 0
    else:
        output = np.unique(component_index_from_atom)
        n_components = output.shape[0]

    return n_components

