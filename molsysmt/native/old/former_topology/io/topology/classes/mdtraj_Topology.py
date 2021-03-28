def from_mdtraj_Topology(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdtraj_Topology import to_openmm_Topology as mdtraj_Topology_to_openmm_Topology
    from .openmm_Topology import from_openmm_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item = mdtraj_Topology_to_openmm_Topology(item)
    tmp_item = openmm_Topology_to_molsysmt_Topology(tmp_item)

    return tmp_item

