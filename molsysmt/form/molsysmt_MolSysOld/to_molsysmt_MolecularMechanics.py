from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSysOld')
def to_molsysmt_MolecularMechanics(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    tmp_item = item.molecular_mechanics.copy()

    return tmp_item


