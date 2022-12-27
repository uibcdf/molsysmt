from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np

@digest()
def get_entity_index_from_atom(molecular_system, indices='all', digest=True):

    from .get_entity_all_from_atom import get_entity_all_from_atom

    output, _,  _ = get_entity_all_from_atom(molecular_system, digest=False)

    if not is_all(indices):
        output = output[indices]

    return output


