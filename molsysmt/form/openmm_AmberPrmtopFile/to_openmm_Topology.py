from molsysmt._private.digestion import digest
from molsysmt.dependencies import requires

@digest(form='openmm.AmberPrmtopFile')
@requires('openmm')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    tmp_item = item.topology

    return tmp_item
