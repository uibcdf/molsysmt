from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='openmm.AmberPrmtopFile')
@dep_digest('openmm')
def to_openmm_System(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    tmp_item = item.createSystem()

    return tmp_item
