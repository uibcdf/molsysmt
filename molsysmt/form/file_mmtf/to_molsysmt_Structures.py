from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'file:mmtf')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import to_molsysmt_Structures as mmtf_MMTFDecoder_to_molsysmt_Structures

    tmp_item = to_mmtf_MMTFDecoder(item, check=False)
    tmp_item = mmtf_MMTFDecoder_to_molsysmt_Structures(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

