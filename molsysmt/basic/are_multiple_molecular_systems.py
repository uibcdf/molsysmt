import numpy as np

def are_multiple_molecular_systems(items):

    from . import is_molecular_system

    output = False

    aux_list = []
    if isinstance(items, (list, tuple)):

        for item in items:
            aux_list.append(is_molecular_system(item))

        output = np.all(aux_list)

    return output

