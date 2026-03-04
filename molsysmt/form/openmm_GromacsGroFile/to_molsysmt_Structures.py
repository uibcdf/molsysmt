from .get_structural_attributes import *
from .get_topological_attributes import *

from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openmm.GromacsGroFile')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native.structures import Structures

    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                            skip_digestion=True)
    box = get_box_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    structure_id = get_structure_id_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    time = get_time_from_system(item, structure_indices=structure_indices, skip_digestion=True)

    tmp_item = Structures()
    tmp_item.append(coordinates=coordinates, structure_id=structure_id, time=time, box=box,
                               skip_digestion=True)

    return tmp_item

