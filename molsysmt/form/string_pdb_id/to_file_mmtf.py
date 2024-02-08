from molsysmt._private.digestion import digest

@digest(form='string:pdb_id')
def to_file_mmtf(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import to_file_mmtf

    tmp_item = to_mmtf_MMTFDecoder(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                   skip_digestion=True)
    tmp_item = to_file_mmtf(tmp_item, output_filename=output_filename, skip_digestion=True)

    return tmp_item

