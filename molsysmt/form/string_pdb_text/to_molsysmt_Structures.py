from molsysmt._private.digestion import digest

@digest(form='string:pdb_text')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', digest=True):

    from molsysmt.native.structures import Structures
    from . import get_time_from_system
    from . import get_box_from_system
    from . import get_coordinates_from_atom

    tmp_item = Structures()
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, digest=False)
    time = get_time_from_system(item, structure_indices=structure_indices, digest=False)
    box = get_box_from_system(item, structure_indices=structure_indices, digest=False)
    tmp_item.append_structures(coordinates=coordinates, box=box, time=time, digest=False)

    return tmp_item

