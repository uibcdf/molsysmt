from molsysmt._private.argdigest import arg_digest


@arg_digest()
def get_n_entities(molecular_system, selection='all', redefine_entities=False,
                     syntax='MolSysMT'):
    """
    Getting the total number of entities in a molecular system or selection.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    redefine_entities : bool, default=False
        Whether to rebuild entity partitioning.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').

    Returns
    -------
    int
        Number of entities.


    .. versionadded:: 1.0.0
    """

    if isinstance(selection, str) and selection == 'all':
        from molsysmt.native import MolSys, Topology
        from .get_entity_index import get_entity_index

        if isinstance(molecular_system, Topology):
            return len(molecular_system.entities.index) if not redefine_entities else len(
                get_entity_index(
                    molecular_system, element='entity', selection='all', redefine_indices=True, syntax=syntax
                )
            )
        if isinstance(molecular_system, MolSys):
            return len(molecular_system.topology.entities.index) if not redefine_entities else len(
                get_entity_index(
                    molecular_system, element='entity', selection='all', redefine_indices=True, syntax=syntax
                )
            )

    if redefine_entities:

        from .get_entity_index import get_entity_index

        aux = get_entity_index(molecular_system, element='entity', selection=selection,
                                  redefine_indices=True, syntax=syntax)
        output = len(aux)

        del aux

    else:

        from molsysmt.basic import get

        output = get(molecular_system, element='atom', selection=selection, syntax=syntax,
                     n_entities=True)

    return output
