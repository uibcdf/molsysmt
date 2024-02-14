from molsysmt._private.digestion import digest

@digest(form='file:prmtop')
def to_openmm_Modeller(item, atom_indices='all', coordinates=None, skip_digestion=False):

    from . import to_openmm_Topology
    from ..openmm_Topology import to_openmm_Modeller as openmm_Topology_to_openmm_Modeller

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    tmp_item = openmm_Topology_to_openmm_Modeller(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

