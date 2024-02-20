from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np

@digest()
def define_new_chain(molecular_system, selection='all', chain_id=None, chain_name=None, syntax='MolSysMT',
                     skip_digestion=False):
    """
    To be written soon...
    """

    from molsysmt.basic import get, set

    if is_all(selection):

        if chain_id is None:
            chain_id = 0
        if chain_name is None:
            chain_name = 'A'

        set(molecular_system, element='atom', selection='all', chain_id=chain_id, skip_digestion=True)
        set(molecular_system, element='chain', selection=0, chain_name=chain_name, skip_digestion=True)

    else:

        raise NotImplementedError

    pass

