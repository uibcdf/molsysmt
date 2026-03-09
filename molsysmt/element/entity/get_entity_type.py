from molsysmt._private.arg_digestion import arg_digest


@arg_digest()
def get_entity_type(molecular_system, element='entity', selection='all', redefine_indices=False,
                    redefine_types=False, syntax='MolSysMT', skip_digestion=False):

    if selection == 'all':
        from molsysmt.native import MolSys, Topology
        from molsysmt.native._hierarchy import project_entity_type_from_topology

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
