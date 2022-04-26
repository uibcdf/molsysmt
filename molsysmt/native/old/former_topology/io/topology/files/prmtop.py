def from_prmtop(item, trajectory_item=None, atom_indices='all', structure_indices='all'):

    from molsysmt.api_forms.api_prmtop import to_openmm_Topology as prmtop_to_openmm_Topology
    from molsysmt.native.io.topology import from_openmm_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item = prmtop_to_openmm_Topology(item)
    tmp_item = openmm_Topology_to_molsysmt_Topology(tmp_item)

    return tmp_item

