from molsysmt._private.digestion import digest

@digest(form='openmm.PDBFile')
def to_molsysmt_TopologyOld(item, atom_indices='all'):

    from .to_openmm_TopologyOld import to_openmm_Topology
    from ..openmm_TopologyOld import to_molsysmt_Topology as openmm_Topology_to_molsysmt_TopologyOld

    tmp_item = to_openmm_Topology(item)
    tmp_item = openmm_Topology_to_molsysmt_TopologyOld(tmp_item, atom_indices=atom_indices)

    return tmp_item

