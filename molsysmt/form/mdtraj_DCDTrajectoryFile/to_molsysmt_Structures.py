from molsysmt._private.arg_digestion import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np

@arg_digest(form='mdtraj.DCDTrajectoryFile')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

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
