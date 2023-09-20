from molsysmt._private.digestion import digest
import numpy as np

@digest()
def define_chain(molecular_system, selection=None, id=None, name=None, syntax='MolSysMT'):
    """
    To be written soon...
    """

    from molsysmt.basic import get, set

    former_id, former_name = get(molecular_system, element='chain', chain_id=True)

    if id in former_id:
        raise ValueError()

    set(molecular_system, element='atom', selection=selection, syntax=syntax,
            chain_id=id, chain_name=name)

    pass
