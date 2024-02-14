from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    tmp_item = item.structures.extract(atom_indices=atom_indices, structure_indices=structure_indices,
                                       skip_digestion=True)

    return tmp_item

