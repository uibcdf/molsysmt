from molsysmt._private.digestion import digest

@digest(form='openmm.GromacsTopFile')
def to_openmm_Topology(item, atom_indices='all'):

    tmp_item = item.topology

    return tmp_item

def _to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_openmm_Topology(item, atom_indices=atom_indices)

