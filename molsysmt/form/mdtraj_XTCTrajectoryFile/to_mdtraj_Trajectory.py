import numpy as np

from molsysmt._private.arg_digestion import arg_digest
from molsysmt import pyunitwizard as puw


@arg_digest(form='mdtraj.XTCTrajectoryFile')
def to_mdtraj_Trajectory(
    item,
    atom_indices='all',
    structure_indices='all',
    skip_digestion=False,
):
    """Converting an XTC reader to a topology-free MDTraj trajectory."""

    import mdtraj as md

    from .to_molsysmt_Structures import to_molsysmt_Structures

    structures = to_molsysmt_Structures(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    coordinates = puw.get_value(structures.coordinates, to_unit='nm')
    time = (
        None
        if structures.time is None
        else puw.get_value(structures.time, to_unit='ps')
    )
    lengths = None
    angles = None
    if structures.box is not None:
        from molsysmt.pbc import get_lengths_and_angles_from_box

        lengths_quantity, angles_quantity = get_lengths_and_angles_from_box(
            structures.box
        )
        lengths = puw.get_value(lengths_quantity, to_unit='nm')
        angles = puw.get_value(angles_quantity, to_unit='degree')

    return md.Trajectory(
        xyz=np.asarray(coordinates),
        topology=None,
        time=None if time is None else np.asarray(time),
        unitcell_lengths=lengths,
        unitcell_angles=angles,
    )
