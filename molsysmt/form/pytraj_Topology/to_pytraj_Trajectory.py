from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import LibraryNotFoundError
import numpy as np

@arg_digest(form='pytraj.Topology')
def to_pytraj_Trajectory(item, atom_indices='all', coordinates=None, box=None, skip_digestion=False):
    """
    Converting from pytraj.Topology to pytraj.Trajectory.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    coordinates : object, default=None
        Argument coordinates.
    box : object, default=None
        Argument box.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    pytraj.Trajectory
        Resulting object in pytraj.Trajectory form.


    .. versionadded:: 1.0.0
    """

    try:
        import pytraj as pt
    except Exception:
        raise LibraryNotFoundError('pytraj')

    from molsysmt.form.pytraj_Trajectory._runtime import ensure_safe_runtime
    from . import extract
    from molsysmt import pyunitwizard as puw

    ensure_safe_runtime()

    tmp_item = extract(item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)

    coordinates = puw.get_value(coordinates, to_unit='angstroms')
    tmp_item = pt.Trajectory(xyz=coordinates.astype('float64'), top=tmp_item)

    if box is not None:
        from molsysmt.pbc import get_lengths_and_angles_from_box

        box_lengths, box_angles = get_lengths_and_angles_from_box(
            box,
            skip_digestion=True,
        )

        box_lengths = puw.get_value(box_lengths, to_unit='angstroms')
        box_angles = puw.get_value(box_angles, to_unit='degrees')

        tmp_item.unitcells = np.hstack([box_lengths, box_angles])
        tmp_item.unitcells = tmp_item.unitcells.astype('float64')

    return tmp_item
