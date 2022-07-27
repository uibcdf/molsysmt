from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    if check:

        digest_item(item, 'nglview.NGLWidget')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from molsysmt.native.structures import Structures
    from . import get_coordinates_from_atom, get_box_from_system, get_step_from_system, get_time_from_system

    tmp_item = Structures()
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices)
    box = get_box_from_system(item, structure_indices=structure_indices)
    step = get_step_from_system(item, structure_indices=structure_indices)
    time = get_time_from_system(item, structure_indices=structure_indices)
    tmp_item.append_structures(coordinates=coordinates, box=box, step=step, time=time)

    return tmp_item

