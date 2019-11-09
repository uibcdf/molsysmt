def from_xtc(item, topology=None, atom_indices='all', frame_indices='all'):

    from molmodmt import convert
    from .io_trajectory import from_xtc as xtc_to_Trajectory
    from .molmod import MolMod

    tmp_item = MolMod()
    tmp_item.topology = convert(topology, to_form='molmodmt.Topology', selection=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = xtc_to_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.topography = None
    tmp_item.structure = None

    return tmp_item

