from molsysmt._private.digestion import digest

@digest(form='openmm.Context')
def to_openmm_System(item, atom_indices='all', skip_digestion=False):

    tmp_item = item.getSystem()

    return tmp_item

