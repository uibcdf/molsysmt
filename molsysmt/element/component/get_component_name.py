from molsysmt._private.digestion import digest
import numpy as np


@digest()
def get_component_name(molecular_system, element='atom', selection='all', redefine_components=False,
                       redefine_names=False, syntax='MolSysMT'):

    if redefine_components:

        from .get_component_index import get_component_index
        return get_component_index(molecular_system, element=element, selection=selection,
                redefine_indices=True)

    elif redefine_names:

        from .get_component_index import get_component_index
        return get_component_index(molecular_system, element=element, selection=selection,
                redefine_indices=True)

    else:

        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     component_name=True)

    return output
