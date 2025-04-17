from molsysmt._private.digestion import digest
from ..molecule import _singular_molecule_type_to_plural
import numpy as np

@digest()
def get_chain_name(molecular_system, element='atom', selection='all',
                   redefine_indices=False, redefine_names=False, syntax='MolSysMT'):

    if redefine_indices:

        raise NotImplementedError

    if redefine_names:

        raise NotImplementedError

    else:

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     chain_name=True)

    return output

#from molsysmt.element.chain import all_chain_names
#self.chains["chain_name"]=np.array(all_chain_names[:self.chains.shape[0]], dtype=object)

