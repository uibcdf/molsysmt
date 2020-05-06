def from_pdb(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native import MolSys
    from molsysmt import convert

    tmp_item = MolSys()
    tmp_item.topology = convert(item, to_form='molsysmt.Topology', selection=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = convert(item, to_form='molsysmt.Trajectory', selection=atom_indices, frame_indices=frame_indices)
    #tmp_item.topography = None
    #tmp_item.structure = None

    return tmp_item

