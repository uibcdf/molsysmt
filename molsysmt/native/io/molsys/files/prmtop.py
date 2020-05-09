def from_prmtop(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt import convert
    from molsysmt.native import MolSys
    from molsysmt.native.io.topology.files import from_prmtop as prmtop_to_molsysmt_Topology

    tmp_item = MolSys()
    tmp_item.topology = prmtop_to_molsysmt_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = convert(trajectory_item, to_form='molsysmt.Trajectory', selection=atom_indices, frame_indices=frame_indices)

    return tmp_item

