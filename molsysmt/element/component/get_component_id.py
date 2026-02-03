from molsysmt._private.digestion import arg_digest
import numpy as np


@arg_digest()
def get_component_id(molecular_system, element='component', selection='all', redefine_indices=False,
                     redefine_ids=False, syntax='MolSysMT', skip_digestion=False):

    if redefine_indices:
        from .get_component_index import get_component_index
        output = get_component_index(molecular_system, element=element, selection=selection,
                                     redefine_indices=True, syntax=syntax, skip_digestion=True)
    elif redefine_ids:
        from .get_component_index import get_component_index
        output = get_component_index(molecular_system, element=element, selection=selection,
                                     redefine_indices=False, syntax=syntax, skip_digestion=True)
    else:
        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     component_id=True, skip_digestion=True)

    if output is not None:
        arr = np.asarray(output)
        if arr.shape == ():
            output = str(arr.astype(str))
        else:
            output = arr.astype(str)
        output = output.tolist()

    return output
