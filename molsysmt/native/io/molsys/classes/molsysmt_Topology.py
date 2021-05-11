def to_molsysmt_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    tmp_item = item.topology.copy()
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

