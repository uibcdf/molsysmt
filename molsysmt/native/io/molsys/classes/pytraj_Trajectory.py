def from_pytraj_Trajectory (item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.io.topology.classes import from_pytraj_Trajectory as pytraj_Trajectory_to_molsysmt_Topology
    from molsysmt.native.io.trajectory.classes import from_pytraj_Trajectory as pytraj_Trajectory_to_molsysmt_Trajectory

    tmp_item = MolSys()
    tmp_item.topology = pytraj_Trajectory_to_molsysmt_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = pytraj_Trajectory_to_molsysmt_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_pytraj_Trajectory (item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    raise NotImplementedError
