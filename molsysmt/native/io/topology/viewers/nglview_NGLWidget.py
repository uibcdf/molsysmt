def from_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import from_openmm_PDBFile as openmm_PDBFile_to_molsysmt_Topology
    from molsysmt.forms.viewers.api_nglview_NGLWidget import to_openmm_PDBFile as nglview_NGLWidget_to_openmm_PDBFile

    tmp_item, tmp_molecular_system = nglview_NGLWidget_to_openmm_PDBFile(item, molecular_system=molecular_system)
    tmp_item, tmp_molecular_system = openmm_PDBFile_to_molsysmt_Topology(tmp_item,
            molecular_system=tmp_molecular_system, atom_indices=atom_indices)

    return tmp_item, tmp_molecular_system

