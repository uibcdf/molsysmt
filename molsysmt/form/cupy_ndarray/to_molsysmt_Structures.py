from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='cupy_ndarray')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    from molsysmt.native.structures import Structures
    from .to_XYZ import to_XYZ

    tmp_item = Structures()
    coordinates = to_XYZ(item, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.append(coordinates=coordinates, skip_digestion=True)

    return tmp_item
