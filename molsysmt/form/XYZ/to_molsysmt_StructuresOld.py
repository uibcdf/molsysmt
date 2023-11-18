from molsysmt._private.digestion import digest

@digest(form='XYZ')
def to_molsysmt_StructuresOld(item, atom_indices='all', structure_indices='all'):

    from molsysmt.native.trajectory import StructuresOld
    from . import get_coordinates_from_atom

    tmp_item = StructuresOld()
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices)
    tmp_item.append_structures(coordinates=coordinates)

    return tmp_item

