from molsysmt._private.digestion import digest

@digest(form='file:msmpk')
def to_molsysmt_StructuresOld(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from . import to_molsysmt_MolSysOld
    from ..molsysmt_MolSysOld import to_molsysmt_StructuresOld as molsysmt_MolSysOld_to_molsysmt_StructuresOld

    tmp_item = to_molsysmt_MolSysOld(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                     skip_digestion=True)
    tmp_item = molsysmt_MolSysOld_to_molsysmt_StructuresOld(tmp_item, skip_digestion=True)

    return tmp_item

