from molsysmt._private.digestion import digest

@digest(form='parmed.Structure')
def to_openmm_Topology(item, atom_indices='all', digest=True):

    from ..openmm_Topology import extract as extract_openmm_Topology

    tmp_item = tmp_item.topology
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices, copy_if_all=False, digest=False)

    return tmp_item

