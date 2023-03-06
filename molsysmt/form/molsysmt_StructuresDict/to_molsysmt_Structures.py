from molsysmt._private.digestion import digest

@digest(form='molsysmt.StructuresDict')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    from molsysmt.native.structures import Structures
    from . import get_coordinates_from_atom, get_structure_id_from_system, get_time_from_system, get_box_from_system

    tmp_item = Structures()

    structure_id = get_structure_id_from_system(item, structure_indices=structure_indices)
    time = get_time_from_system(item, structure_indices=structure_indices)
    box = get_box_from_system(item, structure_indices=structure_indices)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices)
    tmp_item.append_structures(structure_id=structure_id, time=time, coordinates=coordinates, box=box)

    return tmp_item, tmp_molecular_system

def _to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    return to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)

