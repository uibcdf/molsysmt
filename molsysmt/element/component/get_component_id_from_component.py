from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np

@digest()
def get_component_id_from_component(molecular_system, indices='all'):

    if is_all(indices):
        from . import get_n_components_from_system
        n_components = get_n_components_from_system(molecular_system)
        output = np.full(n_components, None, dtype=object)
    else:
        output = np.full(indices.shape[0], None, dtype=object)

    return output

