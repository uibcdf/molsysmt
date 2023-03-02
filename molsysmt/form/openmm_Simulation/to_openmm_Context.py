from molsysmt._private.digestion import digest

@digest(form='openmm.Simulation')
def to_openmm_Context(item, atom_indices='all', structure_indices='all'):

    tmp_item = item.context

    return tmp_item

def _to_openmm_Context(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_openmm_Context(item, atom_indices=atom_indices, structure_indices=structure_indices)

