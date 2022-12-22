from molsysmt._private.digestion import digest

@digest(form='string:pdb_text')
def to_XYZ(item, atom_indices='all', structure_indices='all', digest=True):

    from . import get_coordinates_from_atom

    tmp_item = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, digest=False)

    return tmp_item

