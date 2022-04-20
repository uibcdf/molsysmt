from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'XYZ')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from molsysmt.native.trajectory import Structures
    from . import get_coordinates_from_atom

    tmp_item = Structures()
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices)
    tmp_item.append_structures(coordinates=coordinates)

    return tmp_item

