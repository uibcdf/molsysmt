from molsysmt._private.digestion import digest

@digest(form='string:pdb_id')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', bioassembly_name=None, digest=True):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import to_molsysmt_MolSys as mmtf_MMTFDecoder_to_molsysmt_MolSys

    tmp_item = to_mmtf_MMTFDecoder(item, digest=False)
    tmp_item = mmtf_MMTFDecoder_to_molsysmt_MolSys(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            bioassembly_name=bioassembly_name, digest=False)
    return tmp_item

