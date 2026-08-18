from molsysmt._private.argdigest import arg_digest

@arg_digest()
def get_chain_name(molecular_system, element='atom', selection='all',
                   redefine_indices=False, redefine_ids=False, redefine_names=False, syntax='MolSysMT',
                   skip_digestion=False):
    """
    Getting chain names from a molecular system.


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
    redefine_ids : bool, default=False
        Whether to assign sequential string identifiers.
    redefine_names : bool, default=False
        Whether to assign normalized element names.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of str
        List of chain names.


    .. versionadded:: 1.0.0
    """

    if isinstance(selection, str) and selection == 'all':
        from molsysmt.native import MolSys, Topology
        from molsysmt.native._topology_infer import project_chain_name_from_topology

        if isinstance(molecular_system, Topology):
            return project_chain_name_from_topology(
                molecular_system, element=element, redefine_indices=redefine_indices, redefine_names=redefine_names
            )
        if isinstance(molecular_system, MolSys):
            return project_chain_name_from_topology(
                molecular_system.topology, element=element, redefine_indices=redefine_indices, redefine_names=redefine_names
            )

    if redefine_names:

        from .get_chain_index import get_chain_index
        from .chain_names import all_chain_names

        chain_indices = get_chain_index(molecular_system, element=element, selection=selection, syntax=syntax,
                                        redefine_indices=redefine_indices, skip_digestion=True)

        chain_names = [all_chain_names[ii] for ii in chain_indices]

        if element=='chain':

            return chain_names

        else:

            raise NotImplementedError

    else:

        from molsysmt import get
        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     chain_name=True, skip_digestion=True)

    return output
