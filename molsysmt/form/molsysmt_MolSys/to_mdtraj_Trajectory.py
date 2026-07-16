from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

from smonitor import signal

@signal(tags=['conversion'])
@arg_digest(form='molsysmt.MolSys')
@dep_digest('mdtraj')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt import pyunitwizard as puw
    from .extract import extract
    from .to_mdtraj_Topology import to_mdtraj_Topology
    from . import get_box_lengths_from_system, get_box_angles_from_system, get_coordinates_from_atom, get_time_from_system

    from mdtraj.core.trajectory import Trajectory as mdtraj_Trajectory

    item = extract(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        copy_if_all=False,
        skip_digestion=True,
    )

    tmp_item_topology = to_mdtraj_Topology(item, atom_indices='all', skip_digestion=True)

    tmp_box_lengths = get_box_lengths_from_system(item, structure_indices='all', skip_digestion=True)
    if tmp_box_lengths is not None:
        tmp_box_lengths = puw.get_value(tmp_box_lengths, to_unit='nm')

    tmp_box_angles = get_box_angles_from_system(item, structure_indices='all', skip_digestion=True)
    if tmp_box_angles is not None:
        tmp_box_angles = puw.get_value(tmp_box_angles, to_unit='degrees')

    tmp_coordinates = get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=True)
    tmp_coordinates = puw.get_value(tmp_coordinates, to_unit='nm')

    tmp_time = get_time_from_system(item, structure_indices='all', skip_digestion=True)
    if tmp_time is not None:
        tmp_time = puw.get_value(tmp_time, to_unit='ps')

    tmp_item = mdtraj_Trajectory(tmp_coordinates, tmp_item_topology, tmp_time,
                                 unitcell_lengths=tmp_box_lengths, unitcell_angles=tmp_box_angles)

    return tmp_item
