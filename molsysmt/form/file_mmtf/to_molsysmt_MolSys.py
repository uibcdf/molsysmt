from molsysmt._private.digestion import digest

@digest(form='file:mmtf')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all'):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import to_molsysmt_MolSys as mmtf_MMTFDecoder_to_molsysmt_MolSys

    tmp_item = to_mmtf_MMTFDecoder(item)
    tmp_item = mmtf_MMTFDecoder_to_molsysmt_MolSys(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

def _to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all'):

    return to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)
