from molsysmt._private.digestion import digest

@digest(form='openmm.Simulation')
def to_openmm_Context(item, atom_indices='all', structure_indices='all', digest=True):

    tmp_item = item.context

    return tmp_item

