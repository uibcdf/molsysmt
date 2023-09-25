from molsysmt._private.digestion import digest
import numpy as np

@digest()
def define_new_chain(molecular_system, selection=None, id=None, name=None, syntax='MolSysMT'):
    """
    To be written soon...
    """

    from molsysmt.basic import get, set

    former_id = get(molecular_system, element='chain', chain_id=True)

    if id in former_id:
        raise ValueError()

    kwargs={}

    if id is not None:
        kwargs['chain_id']=id

    if name is not None:
        kwargs['chain_name']=name

    set(molecular_system, element='atom', selection=selection, syntax=syntax, **kwargs)

    pass

