from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='mdtraj.DCDTrajectoryFile')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from .iterators import StructuresIterator
    from molsysmt.native import Structures

    iterator = StructuresIterator(item, atom_indices=atom_indices, structure_indices=structure_indices,
            coordinates=True, box=True, structure_id=True, skip_digestion=True)

    coordinates = []
    box = []
    structure_id = []

    for ii, jj, kk in iterator:
        coordinates.append(ii[0])
        box.append(jj[0])
        structure_id.append(kk)

    coordinates = puw.concatenate(coordinates, type_value='numpy.ndarray')
    box = puw.concatenate(box, type_value='numpy.ndarray')
    structure_id = np.array(structure_id)

    tmp_item = Structures()
    tmp_item.append(structure_id=structure_id, box=box, coordinates=coordinates)

    return tmp_item

