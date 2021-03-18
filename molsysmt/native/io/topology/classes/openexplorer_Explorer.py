def from_openexplorer_Explorer(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes.openmm_Topology import from_openmm_Topology
    from molsysmt.forms.classes.api_openexplorer_Explorer import to_openmm_Topology as openexplorer_Explorer_to_openmm_Topology

    tmp_item = openexplorer_Explorer_to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = from_openmm_Topology(tmp_item)

    return tmp_item

