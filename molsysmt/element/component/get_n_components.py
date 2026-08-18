from molsysmt._private.argdigest import arg_digest


@arg_digest()
def get_n_components(molecular_system, selection='all', redefine_components=False,
                     syntax='MolSysMT'):
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

    Returns
    -------
    int
        Number of components.


    .. versionadded:: 1.0.0
    """

    if isinstance(selection, str) and selection == 'all':
        from molsysmt.native import MolSys, Topology
        from .get_component_index import get_component_index

        if isinstance(molecular_system, Topology):
            return len(molecular_system.components.index) if not redefine_components else len(
                get_component_index(
                    molecular_system, element='component', selection='all', redefine_indices=True, syntax=syntax
                )
            )
        if isinstance(molecular_system, MolSys):
            return len(molecular_system.topology.components.index) if not redefine_components else len(
                get_component_index(
                    molecular_system, element='component', selection='all', redefine_indices=True, syntax=syntax
                )
            )

    if redefine_components:

        from .get_component_index import get_component_index

        aux = get_component_index(molecular_system, element='component', selection=selection,
                                  redefine_indices=True, syntax=syntax)
        output = len(aux)

        del aux

    else:

        from molsysmt.basic import get

        output = get(molecular_system, element='atom', selection=selection, syntax=syntax,
                     n_components=True)

    return output
