from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:mmtf')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from .to_mmtf_MMTFDecoder import to_mmtf_MMTFDecoder
    from molsysmt.form.mmtf_MMTFDecoder.to_openmm_Topology import to_openmm_Topology as mmtf_MMTFDecoder_to_openmm_Topology

    tmp_item = to_mmtf_MMTFDecoder(item, skip_digestion=True)
    tmp_item = mmtf_MMTFDecoder_to_openmm_Topology(tmp_item, atom_indices=atom_indices,
                                                   structure_indices=structure_indices, skip_digestion=True)

    return tmp_item
