from molsysmt._private.arg_digestion import arg_digest

@arg_digest()
def get_chain_index(molecular_system, element='atom', selection='all',
                    redefine_indices=False, syntax='MolSysMT', skip_digestion=False):
    """Returning chain indices for a molecular system.

    Notes
    -----
    This public helper remains form-agnostic. When the input is already
    native and `selection='all'`, it delegates to the native hierarchy layer.
    """

    if selection == 'all':
        from molsysmt.native import MolSys, Topology
        from molsysmt.native._hierarchy import project_chain_index_from_topology

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
