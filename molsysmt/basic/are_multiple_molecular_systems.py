from molsysmt._private.digestion import digest
import numpy as np

@digest()
def are_multiple_molecular_systems(items, digest=True):

    from . import is_a_molecular_system

    output = False

    aux_list = []
    if isinstance(items, (list, tuple)):

        for item in items:
            aux_list.append(is_a_molecular_system(item))

        output = np.all(aux_list)

    return output

