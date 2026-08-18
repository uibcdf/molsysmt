from molsysmt._private.argdigest import arg_digest

@arg_digest()
def get_n_molecules(molecular_system, selection='all', syntax='MolSysMT', skip_digestion=False):
    """
    Getting the total number of molecules in a molecular system or selection.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection filter.
    syntax : str, default='MolSysMT'
        Selection syntax used.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    int
        Number of molecules.

    .. versionadded:: 1.0.0
    """
    from molsysmt.basic import get
    return get(molecular_system, element='molecule', selection=selection, syntax=syntax, n_molecules=True, skip_digestion=True)
