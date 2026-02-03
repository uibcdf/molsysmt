from molsysmt._private.arg_digestion import arg_digest
import numpy as np


@arg_digest()
def get_entity_type(molecular_system, element='type', selection='all', redefine_indices=False,
                    redefine_types=False, syntax='MolSysMT', skip_digestion=False):

    if redefine_indices:

        raise NotImplementedError

    elif redefine_types:

        from ..molecule import get_molecule_type

        molecule_type_from_entities = get_molecule_type(molecular_system, element='entity',
                selection=selection, redefine_types=False, syntax=syntax)

        output = [ii[0] for ii in molecule_type_from_entities]

    else:

        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     entity_type=True)

    return output

