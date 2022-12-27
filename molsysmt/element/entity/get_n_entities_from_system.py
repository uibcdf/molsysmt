from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_n_entities_from_system(molecular_system, digest=True):

    from . import get_entity_index_from_atom

    entity_index_from_atom = get_entity_index_from_atom(molecular_system, digest=False)

    if entity_index_from_atom[0] is None:
        n_entities = 0
    else:
        output = np.unique(entity_index_from_atom)
        n_entities = output.shape[0]

    return n_entities
