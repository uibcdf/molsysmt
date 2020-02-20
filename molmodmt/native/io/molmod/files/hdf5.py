def from_hdf5 (item, topology=None, atom_indices='all', frame_indices='all'):

    from molmodmt import convert
    from .io_trajectory import from_h5 as h5_to_Trajectory
    from .molmod import MolMod

    if topology is None:
        topology = item

    tmp_item = MolMod()
    tmp_item.topology = convert(topology, to_form='molmodmt.Topology', selection=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = h5_to_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.topography = None
    tmp_item.structure = None

    return tmp_item

