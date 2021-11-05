def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    tmp_item = item.topology.copy()
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

