def from_pdb(item, topology=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native import MolSys
    from molsysmt import convert

    if topology is None:
        topology = item

    tmp_item = MolSys()
    tmp_item.composition = convert(topology, to_form='molsysmt.Composition', selection=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = convert(item, to_form='molsysmt.Trajectory', selection=atom_indices, frame_indices=frame_indices)
    #tmp_item.topography = None
    #tmp_item.structure = None

    return tmp_item

