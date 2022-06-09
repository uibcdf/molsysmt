from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
import numpy as np

def get_component_id_from_component(molecular_system, indices='all', check=True):

    if check:

        digest_single_molecular_system(molecular_system)
        indices = digest_indices(indices)

    if indices is 'all':
        from . import get_n_components_from_system
        n_components = get_n_components_from_system(molecular_system, check=False)
        output = np.full(n_components, None, dtype=object)
    else:
        output = np.full(indices.shape[0], None, dtype=object)

    return output

