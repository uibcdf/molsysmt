from molsysmt._private.digestion import digest

@digest(form='file:mmtf')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import to_file_pdb as mmtf_MMTFDecoder_to_file_pdb

    tmp_item = to_mmtf_MMTFDecoder(item)
    tmp_item = mmtf_MMTFDecoder_to_pdb(tmp_item, atom_indices=atom_indices,
                                       structure_indices=structure_indices,
                                       output_filename=output_filename)

    return tmp_item

