from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_mmtf_MMTFDecoder(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'file:mmtf')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from mmtf import parse
    from ..mmtf_MMTFDecoder import extract as extract_mmtf_MMTFDecoder

    tmp_item = parse(item)
    tmp_item = extract_mmtf_MMTFDecoder(tmp_item, atom_indices=atom_indices,
                                        structure_indices=structure_indices, copy_if_all=False,
                                        check=False)

    return tmp_item

