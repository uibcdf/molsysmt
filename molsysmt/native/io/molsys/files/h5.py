def from_h5 (item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native import MolSys
    from molsysmt.native.io.topology.files import from_h5 as h5_to_molsysmt_Topology
    from molsysmt.native.io.trajectory.files import from_h5 as h5_to_molsysmt_Trajectory

    tmp_item = MolSys()
    tmp_item.topology = h5_to_molsysmt_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = h5_to_molsysmt_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item


