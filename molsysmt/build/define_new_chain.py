from molsysmt._private.argdigest import arg_digest

def define_new_chain(molecular_system, selection='all', chain_id=None, chain_name=None, syntax='MolSysMT', skip_digestion=False):
    """
    Defining a new chain for a selection of atoms.




    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    chain_id : object, default=None
        Argument chain_id.
    chain_name : object, default=None
        Argument chain_name.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molecular_system
        The modified molecular system.




    .. versionadded:: 1.0.0
    """
    if chain_name is not None and chain_id is None:
        chain_id = chain_name
    elif chain_id is not None and chain_name is None:
        chain_name = chain_id
    elif chain_id is None and chain_name is None:
        chain_id = 'new'
        chain_name = 'new'

    return _define_new_chain(molecular_system, selection=selection, chain_id=chain_id, chain_name=chain_name, syntax=syntax, skip_digestion=skip_digestion)


@arg_digest()
def _define_new_chain(molecular_system, selection='all', chain_id=None, chain_name=None, syntax='MolSysMT', skip_digestion=False):
    from molsysmt import set as set_attr
    set_attr(molecular_system, selection=selection, syntax=syntax, chain_id=chain_id, chain_name=chain_name, skip_digestion=True)
    return molecular_system
