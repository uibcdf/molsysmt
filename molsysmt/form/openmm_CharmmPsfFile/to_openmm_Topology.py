from molsysmt._private.digestion import digest

@digest(form='openmm.CharmmPsfFile')
def to_openmm_Topology(item, atom_indices='all'):

    tmp_item = item.topology

    return tmp_item

