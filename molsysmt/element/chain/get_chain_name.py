from molsysmt._private.arg_digestion import arg_digest
from ..molecule import _singular_molecule_type_to_plural
import numpy as np

@arg_digest()
def get_chain_name(molecular_system, element='atom', selection='all',
                   redefine_indices=False, redefine_ids=False, redefine_names=False, syntax='MolSysMT',
                   skip_digestion=False):


    if redefine_names:

        from .get_chain_index import get_chain_index
        from .chain_names import all_chain_names

        chain_indices = get_chain_index(molecular_system, element=element, selection=selection, syntax=syntax,
                                        redefine_indices=redefine_indices, skip_digestion=True)

        chain_names = [all_chain_names[ii] for ii in chain_indices]

        if element=='chain':

            return chain_names

        else:

            raise NotImplementedError

    else:

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     chain_name=True, skip_digestion=True)

    return output

