from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
import numpy as np

def get_n_entities_from_system(molecular_system, check=True):

    if check:

        digest_single_molecular_system(molecular_system)

    from . import get_entity_index_from_atom

    entity_index_from_atom = get_entity_index_from_atom(molecular_system, check=True)

    if entity_index_from_atom[0] is None:
        n_entities = 0
    else:
        output = np.unique(entity_index_from_atom)
        n_entities = output.shape[0]

    return n_entities
