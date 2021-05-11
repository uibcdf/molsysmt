def from_mdtraj_Trajectory(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.io.topology import from_mdtraj_Topology as to_topology
    from molsysmt.native.io.trajectory import from_mdtraj_Trajectory as to_trajectory

    tmp_item = MolSys()
    tmp_item.topology, _ = to_topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory, _ = to_trajectory(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item, tmp_molecular_system

def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt import puw
    from mdtraj.core.trajectory import Trajectory as mdtraj_Trajectory
    from molsysmt.forms.classes.api_molsysmt_MolSys import get_box_lengths_from_system
    from molsysmt.forms.classes.api_molsysmt_MolSys import get_box_angles_from_system
    from molsysmt.forms.classes.api_molsysmt_MolSys import get_coordinates_from_atom
    from molsysmt.forms.classes.api_molsysmt_MolSys import get_time_from_system

    from .mdtraj_Topology import to_mdtraj_Topology as molsysmt_MolSys_to_mdtraj_Topology

    tmp_item_topology, _ = molsysmt_MolSys_to_mdtraj_Topology(item, molecular_system, atom_indices=atom_indices)
    tmp_box_lengths = get_box_lengths_from_system(item, frame_indices=frame_indices)
    if tmp_box_lengths is not None:
        tmp_box_lengths = puw.get_value(tmp_box_lengths, in_units='nm')
    tmp_box_angles = get_box_angles_from_system(item, frame_indices=frame_indices)
    if tmp_box_angles is not None:
        tmp_box_angles = puw.get_value(tmp_box_angles, in_units='degrees')
    tmp_coordinates = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    tmp_coordinates = puw.get_value(tmp_coordinates, in_units='nm')
    tmp_time = get_time_from_system(item, frame_indices=frame_indices)
    if tmp_time is not None:
        tmp_time = puw.get_value(tmp_time, in_units='ps')
    tmp_item = mdtraj_Trajectory(tmp_coordinates,tmp_item_topology, tmp_time,
                                 unitcell_lengths=tmp_box_lengths, unitcell_angles=tmp_box_angles)
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

