from molsysmt._private.arg_digestion import arg_digest

@arg_digest()
def get_chain_name(molecular_system, element='atom', selection='all',
                   redefine_indices=False, redefine_ids=False, redefine_names=False, syntax='MolSysMT',
                   skip_digestion=False):
    """Returning chain names for a molecular system.

    Notes
    -----
    Explicit names are preserved when available. If names are redefined, the
    result follows the deterministic local chain naming rules of the native
    layer.
    """

    if selection == 'all':
        from molsysmt.native import MolSys, Topology
        from molsysmt.native._hierarchy import project_chain_name_from_topology

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
