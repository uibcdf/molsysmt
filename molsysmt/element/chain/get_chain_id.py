from molsysmt._private.argdigest import arg_digest

@arg_digest()
def get_chain_id(molecular_system, element='chain', selection='all', syntax='MolSysMT', skip_digestion=False):
    """
    Getting chain identifier strings from a molecular system.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form.
    element : str, default='chain'
        Target element level.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection of elements to query.
    syntax : str, default='MolSysMT'
        Selection syntax used.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    list of str
        List of chain IDs.

    .. versionadded:: 1.0.0
    """
    from molsysmt.basic import get
    return get(molecular_system, element=element, selection=selection, syntax=syntax, chain_id=True, skip_digestion=True)
