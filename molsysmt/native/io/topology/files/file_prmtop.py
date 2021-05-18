def from_file_prmtop(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.files.api_file_prmtop import to_openmm_Topology as file_prmtop_to_openmm_Topology
    from molsysmt.native.io.topology.classes import from_openmm_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = file_prmtop_to_openmm_Topology(item, molecular_system)
    tmp_item, tmp_molecular_system = openmm_Topology_to_molsysmt_Topology(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

