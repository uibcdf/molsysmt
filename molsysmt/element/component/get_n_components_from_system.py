from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_n_components_from_system(molecular_system, digest=True):

    from . import get_component_index_from_atom

    component_index_from_atom = get_component_index_from_atom(molecular_system, indices='all', digest=False)

    if component_index_from_atom[0] is None:
        n_components = 0
    else:
        output = np.unique(component_index_from_atom)
        n_components = output.shape[0]

    return n_components

