from molsysmt._private.digestion import arg_digest
import numpy as np

@arg_digest()
def get_chain_id(molecular_system, element='atom', selection='all',
                 redefine_indices=False, redefine_ids=False,
                 syntax='MolSysMT', skip_digestion=False):

    if redefine_ids:

        from .get_chain_index import get_chain_index

        chain_indices = get_chain_index(molecular_system, element=element, selection=selection, syntax=syntax,
                                        redefine_indices=redefine_indices, skip_digestion=True)

        chain_ids = chain_indices

        if element=='chain':

            return chain_ids

        else:

            raise NotImplementedError

    else:

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     chain_id=True, skip_digestion=True)

    if output is not None:
        arr = np.asarray(output)
        if arr.shape == ():
            output = str(arr.astype(str))
        else:
            output = arr.astype(str)

    return output
