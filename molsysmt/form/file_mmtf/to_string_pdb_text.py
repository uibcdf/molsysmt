from molsysmt._private.digestion import digest

@digest(form='file:mmtf')
def to_string_pdb_text(item, atom_indices='all', structure_indices='all'):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import to_string_pdb_text as mmtf_MMTFDecoder_to_string_pdb_text

    tmp_item = to_mmtf_MMTFDecoder(item)
    tmp_item = mmtf_MMTFDecoder_to_string_pdb_text(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices)

    return tmp_item

def _to_string_pdb_text(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    return to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices)

