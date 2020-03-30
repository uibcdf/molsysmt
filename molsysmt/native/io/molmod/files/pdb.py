def from_pdb(item, topology=None, atom_indices='all', frame_indices='all'):

    from molsysmt import convert
    from .io_trajectory import from_pdb as pdb_to_Trajectory
    from .molsys import MolSys

    if topology is None:
        topology = item

    tmp_item = MolSys()
    tmp_item.topology = convert(topology, to_form='molsysmt.Topology', selection=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = pdb_to_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.topography = None
    tmp_item.structure = None

    return tmp_item

