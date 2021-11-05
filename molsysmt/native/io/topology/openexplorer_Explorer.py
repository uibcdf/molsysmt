def from_openexplorer_Explorer(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.openmm_Topology import from_openmm_Topology
    from molsysmt.forms.api_openexplorer_Explorer import to_openmm_Topology as openexplorer_Explorer_to_openmm_Topology

    tmp_item, tmp_molecular_system = openexplorer_Explorer_to_openmm_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = from_openmm_Topology(tmp_item, tmp_molecular_system)

    return tmp_item, tmp_molecular_system

