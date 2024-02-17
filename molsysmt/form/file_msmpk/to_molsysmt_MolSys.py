from molsysmt._private.digestion import digest

@digest(form='file:msmpk')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from .to_molsysmt_MolSysOld import to_molsysmt_MolSysOld
    from ..molsysmt_MolSysOld import to_molsysmt_MolSys as molsysmt_MolSysOld_to_molsysmt_MolSys

    tmp_item = to_molsysmt_MolSysOld(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                     skip_digestion=True)
    tmp_item = molsysmt_MolSysOld_to_molsysmt_MolSys(tmp_item)

    return tmp_item

