def from_crd(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.files.api_crd import to_openmm_Topology as prmtop_to_openmm_Topology
    from molsysmt.native.io.topology.classes import from_openmm_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item = prmtop_to_openmm_Topology(item, atom_indices=atom_indices)
    tmp_item = openmm_Topology_to_molsysmt_Topology(tmp_item)

    return tmp_item

