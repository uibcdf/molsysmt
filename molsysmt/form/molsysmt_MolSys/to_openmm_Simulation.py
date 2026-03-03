from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_openmm_Simulation(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.to_openmm_Simulation import to_openmm_Simulation as openmm_Topology_to_openmm_Simulation

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_item = openmm_Topology_to_openmm_Simulation(tmp_item, skip_digestion=True)

    return tmp_item

