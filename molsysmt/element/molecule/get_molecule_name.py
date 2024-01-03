from molsysmt._private.digestion import digest
import numpy as np


@digest()
def get_molecule_name(molecular_system, element='atom', selection='all', redefine_molecules=False,
                       redefine_names=False, syntax='MolSysMT'):

    if redefine_molecules:

        from .get_molecule_index import get_molecule_index
        return get_molecule_index(molecular_system, element=element, selection=selection,
                syntax=syntax, redefine_indices=True)

    elif redefine_names:

        from .get_molecule_index import get_molecule_index
        return get_molecule_index(molecular_system, element=element, selection=selection,
                syntax=syntax, redefine_indices=True)

    else:

        from molsysmt.basic import get

        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     molecule_name=True)

    return output
