from molsysmt._private.digestion import digest

@digest(form='file:inpcrd')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    from molsysmt.native import Structures

    tmp_item = Structures(filepath=item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

def _to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)
