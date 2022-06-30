from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
import numpy as np

def get_entity_id_from_entity(molecular_system, indices='all', check=True):

    if check:

        digest_single_molecular_system(molecular_system)
        indices = digest_indices(indices)

    from . import get_n_entities_from_system

    if indices is 'all':
        n_entities = get_n_entities_from_system(molecular_system, check=False)
        output = np.full(n_entities, None, dtype=object)
    else:
        output = np.full(indices.shape[0], None, dtype=object)

    return output

