from molsysmt._private.digestion import digest

@digest(form='file:prmtop')
def to_openmm_Modeller(item, atom_indices='all', coordinates=None, digest=True):

    from . import to_openmm_Topology
    from ..openmm_Topology import to_openmm_Modeller as openmm_Topology_to_openmm_Modeller

    tmp_item = to_openmm_Topology(item, digest=False)
    tmp_item = openmm_Topology_to_openmm_Modeller(tmp_item, atom_indices=atom_indices, digest=False)

    return tmp_item


