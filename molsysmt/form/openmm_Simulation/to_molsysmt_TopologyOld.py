from molsysmt._private.digestion import digest

@digest(form='openmm.Simulation')
def to_molsysmt_TopologyOld(item, atom_indices='all'):

    from . import to_openmm_Topology as openmm_Simulation_to_openmm_Topology
    from molsysmt.form.openmm_Topology import to_molsysmt_TopologyOld as openmm_Topology_to_molsysmt_TopologyOld

    tmp_item = openmm_Simulation_to_openmm_Topology(item)
    tmp_item = openmm_Topology_to_molsysmt_TopologyOld(tmp_item, atom_indices=atom_indices)

    return tmp_item

