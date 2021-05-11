def from_mdtraj_Trajectory(item, molecular_system, atom_indices='all', frame_indices='all'):

    from .mdtraj_Topology import from_mdtraj_Topology

    tmp_item = item.topology
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    tmp_item, tmp_molecular_system = from_mdtraj_Topology(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

