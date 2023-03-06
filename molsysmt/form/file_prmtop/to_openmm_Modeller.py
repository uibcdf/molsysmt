from molsysmt._private.digestion import digest

@digest(form='file:prmtop')
def to_openmm_Modeller(item, atom_indices='all', coordinates=None):

    from . import to_openmm_Topology
    from ..openmm_Topology import to_openmm_Modeller as openmm_Topology_to_openmm_Modeller

    tmp_item = to_openmm_Topology(item)
    tmp_item = openmm_Topology_to_openmm_Modeller(tmp_item, atom_indices=atom_indices)

    return tmp_item

def _to_openmm_Modeller(item, atom_indices='all', structure_indices='all'):

    return to_openmm_Modeller(item, atom_indices=atom_indices, coordinates=coordinates)

