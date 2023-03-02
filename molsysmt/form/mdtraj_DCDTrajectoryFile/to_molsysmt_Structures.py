from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='mdtraj.DCDTrajectoryFile')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    from .iterators import StructuresIterator
    from molsysmt.native.structures import Structures

    iterator = StructuresIterator(item, atom_indices=atom_indices, structure_indices=structure_indices,
            coordinates=True, box=True, structure_id=True)

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
    tmp_item.append_structures(structure_id=structure_id, box=box, coordinates=coordinates)


    #from molsysmt.native.structures import Structures
    #from . import get_coordinates_from_atom, get_structure_id_from_system, get_time_from_system, get_box_from_system

    #tmp_item = Structures()

    #coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices)
    #structure_id = get_structure_id_from_system(item, structure_indices=structure_indices)
    #time = get_time_from_system(item, structure_indices=structure_indices)
    #box = get_box_from_system(item, structure_indices=structure_indices)

    #tmp_item.append_structures(structure_id=structure_id, time=time, box=box, coordinates=coordinates)

    return tmp_item

def _to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)

