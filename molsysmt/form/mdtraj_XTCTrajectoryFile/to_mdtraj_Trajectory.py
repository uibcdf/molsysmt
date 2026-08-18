import numpy as np

from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw


@arg_digest(form='mdtraj.XTCTrajectoryFile')
def to_mdtraj_Trajectory(
    item,
    atom_indices='all',
    structure_indices='all',
    skip_digestion=False,
):
    """
    Converting from mdtraj.XTCTrajectoryFile to mdtraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Trajectory
        Resulting object in mdtraj.Trajectory form.


    .. versionadded:: 1.0.0
    """

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
