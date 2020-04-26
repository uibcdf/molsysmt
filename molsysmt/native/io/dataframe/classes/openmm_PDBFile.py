def from_openmm_PDBFile(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import to_openmm_Topology as openmm_PDBFile_to_openmm_Topology
    from .openmm_Topology import from_openmm_Topology as openmm_Topology_to_molsysmt_DataFrame

    tmp_item = openmm_PDBFile_to_openmm_Topology(item)
    tmp_item = openmm_Topology_to_molsysmt_DataFrame(tmp_item)

    return tmp_item

