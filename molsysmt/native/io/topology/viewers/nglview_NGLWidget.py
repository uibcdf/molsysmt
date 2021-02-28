def from_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import from_openmm_PDBFile as openmm_PDBFile_to_molsysmt_Topology
    from molsysmt.forms.viewers.api_nglview_NGLWidget import to_openmm_PDBFile as nglview_NGLWidget_to_openmm_PDBFile

    tmp_item = nglview_NGLWidget_to_openmm_PDBFile(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_PDBFile_to_molsysmt_Topology(tmp_item)

    return tmp_item

