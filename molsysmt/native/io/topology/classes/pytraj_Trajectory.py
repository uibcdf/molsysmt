def to_pytraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def from_pytraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from .pytraj_Topology import from_pytraj_Topology as molsysmt_Topology_from_pytraj_Topology
    tmp_item = item.topology
    tmp_item = molsysmt_Topology_from_pytraj_Topology(tmp_item)
    return tmp_item

