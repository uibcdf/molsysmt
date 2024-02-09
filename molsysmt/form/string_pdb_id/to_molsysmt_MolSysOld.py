from molsysmt._private.digestion import digest

@digest(form='string:pdb_id')
def to_molsysmt_MolSysOld(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import to_molsysmt_MolSysOld as mmtf_MMTFDecoder_to_molsysmt_MolSysOld

    tmp_item = to_mmtf_MMTFDecoder(item, skip_digestion=True)
    tmp_item = mmtf_MMTFDecoder_to_molsysmt_MolSysOld(tmp_item, atom_indices=atom_indices,
                                                      structure_indices=structure_indices, skip_digestion=True)
    return tmp_item

