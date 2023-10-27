from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def write_topology_in_msmh5(item, file, atom_indices='all'):

    from . import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology
    from ..molsysmt_Topology import write_topology_in_msmh5 as write_molsysmt_Topology_in_msmh5

    molsysmt_Topology = openmm_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices)
    write_molsysmt_Topology_in_msmh5(molsysmt_Topology, file)

    pass

