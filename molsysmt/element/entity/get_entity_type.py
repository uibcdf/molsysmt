from molsysmt._private.digestion import digest
import numpy as np


@digest()
def get_entity_type(molecular_system, element='atom', selection='all', redefine_entities=False,
                       redefine_types=False, syntax='MolSysMT'):

    if redefine_entities:

        raise NotImplementedError

    elif redefine_types:

        from ..molecule import get_molecule_type

        molecule_type_from_entities = get_molecule_type(molecular_system, element='entity',
                selection=selection, redefine_types=True, syntax=syntax)

        output = [ii[0] for ii in molecule_type_from_entities]

    else:

        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     entity_type=True)

    return output

