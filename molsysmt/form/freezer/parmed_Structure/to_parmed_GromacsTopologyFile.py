
    from parmed.gromacs import GromacsTopologyFile as GromacsTopologyFile

    tmp_item, tmp_molecular_system = to_parmed_Structure(item, molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = GromacsTopologyFile.from_structure(tmp_item)
    if tmp_molecular_system is not None:
        tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

