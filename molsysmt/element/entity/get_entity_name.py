from molsysmt._private.digestion import arg_digest
import numpy as np


@arg_digest()
def get_entity_name(molecular_system, element='entity', selection='all', redefine_indices=False,
                    redefine_names=False, syntax='MolSysMT', skip_digestion=False):

    if redefine_indices:

        raise NotImplementedError

    elif redefine_names:

        from ..molecule import get_molecule_name

        molecule_name_from_entities = get_molecule_name(molecular_system, element='entity',
                selection=selection, redefine_names=True, syntax=syntax, skip_digestion=True)

        output = [ii[0] for ii in molecule_name_from_entities]

    else:

        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     entity_name=True, skip_digestion=True)

    return output

