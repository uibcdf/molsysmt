from molsysmt._private.digestion import digest
import numpy as np


@digest()
def get_molecule_id(molecular_system, element='molecule', selection='all', redefine_indices=False,
                    redefine_ids=False, syntax='MolSysMT', skip_digestion=False):

    if redefine_indices:
        from .get_molecule_index import get_molecule_index
        output = get_molecule_index(molecular_system, element=element, selection=selection,
                                     redefine_indices=True, syntax=syntax)
    elif redefine_ids:
        from .get_molecule_index import get_molecule_index
        output = get_molecule_index(molecular_system, element=element, selection=selection,
                                    redefine_indices=False, syntax=syntax)
    else:
        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     molecule_id=True)

    if output is not None:
        arr = np.asarray(output)
        if arr.shape == ():
            output = str(arr.astype(str))
        else:
            output = arr.astype(str)
        output = output.tolist()

    return output
