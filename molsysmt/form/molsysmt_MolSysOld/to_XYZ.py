from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSysOld')
def to_XYZ(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from . import get_coordinates_from_atom

    tmp_item = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

