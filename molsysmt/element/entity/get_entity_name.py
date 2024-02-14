from molsysmt._private.digestion import digest
import numpy as np


@digest()
def get_entity_name(molecular_system, element='atom', selection='all', redefine_entities=False,
                       redefine_names=False, syntax='MolSysMT'):

    if redefine_entities:

        raise NotImplementedError

    elif redefine_names:

        from ..molecule import get_molecule_name

        molecule_name_from_entities = get_molecule_name(molecular_system, element='entity',
                selection=selection, redefine_names=True, syntax=syntax)

        output = [ii[0] for ii in molecule_name_from_entities]

    else:

        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     entity_name=True)

    return output

