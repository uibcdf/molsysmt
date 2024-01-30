from molsysmt._private.digestion import digest

@digest(form='file:msmpk')
def to_molsysmt_TopologyOld(item, atom_indices='all', skip_digestion=False):

    from . import to_molsysmt_MolSysOld
    from ..molsysmt_MolSysOld import to_molsysmt_TopologyOld as molsysmt_MolSysOld_to_molsysmt_TopologyOld

    tmp_item = to_molsysmt_MolSysOld(item, skip_digestion=True)
    tmp_item = molsysmt_MolSysOld_to_molsysmt_TopologyOld(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

