from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSysOld')
def to_molsysmt_StructuresOld(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    tmp_item = item.structures.copy()

    return tmp_item

