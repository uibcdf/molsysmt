from molsysmt._private.digestion import digest

@digest(form='file:inpcrd')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', digest=True):

    from molsysmt.native import Structures

    tmp_item = Structures(filepath=item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)

    return tmp_item

