
def from_mdtraj_Trajectory(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.molsys import MolSys
    #from molsysmt.native.io.card import from_mmtf_mdtraj_Trajectory as to_card
    from molsysmt.native.io.topology import from_mdtraj_Topology as to_topology
    from molsysmt.native.io.trajectory import from_mdtraj_Trajectory as to_trajectory

    tmp_item = MolSys()
    tmp_item.topology = to_topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = to_trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.card = None
    tmp_item.topography = None
    return tmp_item

def to_mdtraj_Trajectory(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from simtk.unit import nanometers, degrees, picoseconds
    from mdtraj.core.trajectory import Trajectory as mdtraj_Trajectory
    from molsysmt.forms.classes.api_molsysmt_MolSys import get_box_lengths_from_system
    from molsysmt.forms.classes.api_molsysmt_MolSys import get_box_angles_from_system
    from molsysmt.forms.classes.api_molsysmt_MolSys import get_coordinates_from_atom
    from molsysmt.forms.classes.api_molsysmt_MolSys import get_time_from_system

    from .mdtraj_Topology import to_mdtraj_Topology as molsysmt_MolSys_to_mdtraj_Topology

    tmp_item_topology = molsysmt_MolSys_to_mdtraj_Topology(item, atom_indices=atom_indices)
    tmp_box_lengths = get_box_lengths_from_system(item, frame_indices=frame_indices)
    tmp_box_lengths = tmp_box_lengths.in_units_of(nanometers)._value
    tmp_box_angles = get_box_angles_from_system(item, frame_indices=frame_indices)
    tmp_box_angles = tmp_box_angles.in_units_of(degrees)._value
    tmp_coordinates = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    tmp_coordinates = tmp_coordinates.in_units_of(nanometers)._value
    tmp_time = get_time_from_system(item, frame_indices=frame_indices)
    tmp_time = tmp_time.in_units_of(picoseconds)._value
    tmp_item = mdtraj_Trajectory(tmp_coordinates,tmp_item_topology, tmp_time,
                                 unitcell_lengths=tmp_box_lengths, unitcell_angles=tmp_box_angles)

    return tmp_item




