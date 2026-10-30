from molsysmt._private.argdigest import arg_digest


@arg_digest()
def get_component_index(
    molecular_system,
    element="component",
    selection="all",
    redefine_indices=False,
    syntax="MolSysMT",
    skip_digestion=False,
):
    """
    Getting 0-based component indices from a molecular system.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='component'
        Structural element level to query ('atom', 'group', 'component', 'molecule', 'chain', 'entity').
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    redefine_indices : bool, default=False
        Whether to reassign contiguous 0-based indices.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of int
        List of 0-based component indices.


    .. versionadded:: 1.0.0
    """

    from molsysmt.native._component_projection import prepare

    source = prepare(molecular_system, indices=redefine_indices)
    return source.get(
        element=element,
        selection=selection,
        syntax=syntax,
        component_index=True,
        skip_digestion=True,
    )
