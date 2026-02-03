from molsysmt._private.digestion import arg_digest
from molsysmt.dependencies import dep_digest

@arg_digest(form='openmm.AmberPrmtopFile')
@dep_digest('openmm')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    tmp_item = item.topology

    return tmp_item
