from molsysmt._private.argdigest import arg_digest


@arg_digest()
def get_entity_type(molecular_system, element='entity', selection='all', redefine_indices=False,
                    redefine_types=False, syntax='MolSysMT', skip_digestion=False):
    """
    Getting entity types from a molecular system.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='entity'
        Structural element level to query ('atom', 'group', 'component', 'molecule', 'chain', 'entity').
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    redefine_indices : bool, default=False
        Whether to reassign contiguous 0-based indices.
    redefine_types : object, default=False
        Argument redefine_types.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of str
        List of entity type classifications ('protein', 'dna', 'water', etc.).


    .. versionadded:: 1.0.0
    """

    if isinstance(selection, str) and selection == 'all':
        from molsysmt.native import MolSys, Topology
        from molsysmt.native._topology_infer import project_entity_type_from_topology

        if isinstance(molecular_system, Topology):
            return project_entity_type_from_topology(
                molecular_system,
                element=element,
                redefine_indices=redefine_indices,
                redefine_types=redefine_types,
            )
        if isinstance(molecular_system, MolSys):
            return project_entity_type_from_topology(
                molecular_system.topology,
                element=element,
                redefine_indices=redefine_indices,
                redefine_types=redefine_types,
            )

    if redefine_indices:

        raise NotImplementedError

    elif redefine_types:

        from ..molecule import get_molecule_type

        molecule_type_from_entities = get_molecule_type(molecular_system, element='entity',
                selection=selection, redefine_types=False, syntax=syntax)

        output = [ii[0] for ii in molecule_type_from_entities]

    else:

        from molsysmt.basic import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     entity_type=True)

    return output
