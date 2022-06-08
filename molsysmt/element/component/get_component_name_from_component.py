from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
import numpy as np

def component_name_from_component(item, indices='all'):

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

