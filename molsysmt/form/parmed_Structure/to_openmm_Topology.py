from molsysmt._private.digestion import digest

@digest(form='parmed.Structure')
def to_openmm_Topology(item, atom_indices='all'):

    from ..openmm_Topology import extract as extract_openmm_Topology

    tmp_item = tmp_item.topology
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices, copy_if_all=False)

    return tmp_item

def _to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_openmm_Topology(item, atom_indices=atom_indices)

