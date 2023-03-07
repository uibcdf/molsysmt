from molsysmt._private.digestion import digest

@digest(form='string:pdb_id')
def to_molsysmt_Topology(item, atom_indices='all', structure_indices='all'):

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import to_molsysmt_Topology as mmtf_MMTFDecoder_to_molsysmt_Topology

    tmp_item = to_mmtf_MMTFDecoder(item)
    tmp_item = mmtf_MMTFDecoder_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

def _to_molsysmt_Topology(item, atom_indices='all', structure_indices='all'):

    return to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)

