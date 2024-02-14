from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def write_topology_in_h5msm(item, file, atom_indices='all', skip_digestion=False):

    from . import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology
    from ..molsysmt_Topology import write_topology_in_h5msm as write_molsysmt_Topology_in_h5msm

    molsysmt_Topology = openmm_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    write_molsysmt_Topology_in_h5msm(molsysmt_Topology, file, skip_digestion=True)

    pass

