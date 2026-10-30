from molsysmt._private.argdigest import arg_digest


@arg_digest()
def get_component_name(
    molecular_system,
    element="component",
    selection="all",
    redefine_indices=False,
    redefine_names=False,
    syntax="MolSysMT",
    skip_digestion=False,
):
    """
    Getting component names from a molecular system.


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
    redefine_names : bool, default=False
        Whether to assign normalized element names.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of str
        List of component names.


    .. versionadded:: 1.0.0
    """

    from molsysmt.native._component_projection import prepare

    source = prepare(molecular_system, indices=redefine_indices, names=redefine_names)
    return source.get(
        element=element,
        selection=selection,
        syntax=syntax,
        component_name=True,
        skip_digestion=True,
    )
