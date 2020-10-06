def from_crd(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native import MolSys
    from molsysmt.native.io.topology.files import from_inpcrd as inpcrd_to_molsysmt_Topology
    from molsysmt.native.io.trajectory.files import from_inpcrd as inpcrd_to_molsysmt_Trajectory

    tmp_item = MolSys()
    tmp_item.topology = inpcrd_to_molsysmt_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = inpcrd_to_molsysmt_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_crd(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError
