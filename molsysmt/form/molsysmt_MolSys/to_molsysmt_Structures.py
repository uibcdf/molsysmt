from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    tmp_item = item.structures.copy()

    return tmp_item

