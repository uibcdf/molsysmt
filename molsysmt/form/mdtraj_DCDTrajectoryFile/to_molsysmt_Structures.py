from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np

@arg_digest(form='mdtraj.DCDTrajectoryFile')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.DCDTrajectoryFile to molsysmt.Structures.

    Parameters
    ----------
    item : mdtraj.DCDTrajectoryFile
        Source item in mdtraj.DCDTrajectoryFile form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Structures
        Resulting object in molsysmt.Structures form.

    .. versionadded:: 1.0.0
    """

    from .iterators import StructuresIterator
    from molsysmt.native import Structures

    iterator = StructuresIterator(item, atom_indices=atom_indices, structure_indices=structure_indices,
            coordinates=True, box=True, structure_id=True, skip_digestion=True)

    coordinates = []
    box = []
    box_is_available = True
    structure_id = []

    position = item.tell()
    try:
        for ii, jj, kk in iterator:
            coordinates.append(ii[0])
            if jj is None:
                box_is_available = False
            elif box_is_available:
                box.append(jj[0])
            structure_id.extend(np.atleast_1d(kk).tolist())
    finally:
        item.seek(position)

    coordinates = puw.utils.sequences.concatenate(coordinates, value_type='numpy.ndarray')
    if box_is_available:
        box = puw.utils.sequences.concatenate(box, value_type='numpy.ndarray')
    else:
        box = None
    structure_id = np.array(structure_id)

    tmp_item = Structures()
    tmp_item.append(structure_id=structure_id, box=box, coordinates=coordinates)

    return tmp_item
