
def from_mdtraj_Trajectory(item, atom_indices='all', frame_indices='all'):

    from .mdtraj_Topology import from_mdtraj_Topology

    return from_mdtraj_Topology(item.topology, atom_indices=atom_indices, frame_indices=frame_indices)


