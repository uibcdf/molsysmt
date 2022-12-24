from molsysmt._private.digestion import digest

@digest(form='openmm.GromacsTopFile')
def to_openmm_Topology(item, atom_indices='all', digest=True):

    tmp_item = item.topology

    return tmp_item

