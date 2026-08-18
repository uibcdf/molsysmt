from molsysmt._private.argdigest import arg_digest

@arg_digest()
def get_chain_index(molecular_system, element='atom', selection='all',
                    redefine_indices=False, syntax='MolSysMT', skip_digestion=False):
    """
    Getting 0-based chain indices from a molecular system.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='atom'
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
        List of 0-based chain indices.


    .. versionadded:: 1.0.0
    """

    if isinstance(selection, str) and selection == 'all':
        from molsysmt.native import MolSys, Topology
        from molsysmt.native._topology_infer import project_chain_index_from_topology

        if isinstance(molecular_system, Topology):
            return project_chain_index_from_topology(
                molecular_system, element=element, redefine_indices=redefine_indices
            )
        if isinstance(molecular_system, MolSys):
            return project_chain_index_from_topology(
                molecular_system.topology, element=element, redefine_indices=redefine_indices
            )

    from molsysmt import get

    if redefine_indices:

        match element:

            case 'atom':

                n_atoms = get(molecular_system, element='system', n_atoms=True, skip_digestion=True)
                output = n_atoms * [0]

            case 'group':

                n_groups = get(molecular_system, element='system', n_groups=True, skip_digestion=True)
                output = n_groups * [0]

            case 'molecule':

                n_molecules = get(molecular_system, element='system', n_molecules=True, skip_digestion=True)
                output = n_molecules * [0]

            case 'entity':

                n_entities = get(molecular_system, element='system', n_entities=True, skip_digestion=True)
                output = n_entities * [0]

            case 'component':

                n_components = get(molecular_system, element='system', n_components=True, skip_digestion=True)
                output = n_components * [0]

            case 'chain':

                output = [0]

    else:

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     chain_index=True, skip_digestion=True)

    return output
