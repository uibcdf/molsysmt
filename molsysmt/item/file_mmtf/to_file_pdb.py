from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None, check=True):

    if check:

        digest_item(item, 'file:mmtf')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import to_file_pdb as mmtf_MMTFDecoder_to_file_pdb

    tmp_item = to_mmtf_MMTFDecoder(item, check=False)
    tmp_item = mmtf_MMTFDecoder_to_pdb(tmp_item, atom_indices=atom_indices,
                                       structure_indices=structure_indices,
                                       output_filename=output_filename, check=False)

    return tmp_item

