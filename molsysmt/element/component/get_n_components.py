from molsysmt._private.argdigest import arg_digest


@arg_digest()
def get_n_components(
    molecular_system,
    selection="all",
    redefine_components=False,
    syntax="MolSysMT",
    skip_digestion=False,
):
    """
    Getting the total number of components in a molecular system or selection.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    redefine_components : bool, default=False
        Whether to rebuild component partitioning.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').

    skip_digestion : bool, default=False
        Skip argument digestion only for already validated input.

    Returns
    -------
    int
        Number of components.


    .. versionadded:: 1.0.0
    """

    from molsysmt.native._component_projection import prepare

    source = prepare(molecular_system, indices=redefine_components)
    return source.get(
        element="atom", selection=selection, syntax=syntax, n_components=True
    )
