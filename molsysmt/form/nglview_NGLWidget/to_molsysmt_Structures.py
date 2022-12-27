from molsysmt._private.digestion import digest

@digest(form='nglview.NGLWidget')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', digest=True):

    from molsysmt.native.structures import Structures
    from . import get_coordinates_from_atom, get_box_from_system, get_structure_id_from_system, get_time_from_system

    tmp_item = Structures()
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, digest=False)
    box = get_box_from_system(item, structure_indices=structure_indices, digest=False)
    structure_id = get_structure_id_from_system(item, structure_indices=structure_indices, digest=False)
    time = get_time_from_system(item, structure_indices=structure_indices, digest=False)
    tmp_item.append_structures(coordinates=coordinates, box=box, structure_id=structure_id, time=time, digest=False)

    return tmp_item

