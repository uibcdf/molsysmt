from molsysmt._private.digestion import arg_digest
from molsysmt.dependencies import requires

@arg_digest(form='openmm.AmberPrmtopFile')
@requires('openmm')
def to_openmm_System(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    tmp_item = item.createSystem()

    return tmp_item
