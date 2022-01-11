def to_mdtraj_Trajectory(item, atom_indices='all', frame_indices='all'):

    from molsysmt._private_tools.exceptions import LibraryNotFound, ItemWithWrongForm
    from molsysmt import puw
    from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
    from molsysmt.tools.molsysmt_MolSys import to_mdtraj_Topology as molsysmt_MolSys_to_mdtraj_Topology
    from molsysmt.tools.molsysmt_MolSys import get_box_lengths_from_system, get_box_angles_from_system, get_coordinates_from_atom, get_time_from_system
    try:
        from mdtraj.core.trajectory import Trajectory as mdtraj_Trajectory
    except:
        raise LibraryNotFound('mdtraj')

    if not is_molsysmt_MolSys(item):
        raise ItemWithWrongForm('molsysmt.MolSys')

    tmp_item_topology = molsysmt_MolSys_to_mdtraj_Topology(item, atom_indices=atom_indices)

    tmp_box_lengths = get_box_lengths_from_system(item, frame_indices=frame_indices)
    if tmp_box_lengths is not None:
        tmp_box_lengths = puw.get_value(tmp_box_lengths, to_unit='nm')

    tmp_box_angles = get_box_angles_from_system(item, frame_indices=frame_indices)
    if tmp_box_angles is not None:
        tmp_box_angles = puw.get_value(tmp_box_angles, to_unit='degrees')

    tmp_coordinates = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    tmp_coordinates = puw.get_value(tmp_coordinates, to_unit='nm')

    tmp_time = get_time_from_system(item, frame_indices=frame_indices)
    if tmp_time is not None:
        tmp_time = puw.get_value(tmp_time, to_unit='ps')

    tmp_item = mdtraj_Trajectory(tmp_coordinates, tmp_item_topology, tmp_time,
                                 unitcell_lengths=tmp_box_lengths, unitcell_angles=tmp_box_angles)

    return tmp_item

