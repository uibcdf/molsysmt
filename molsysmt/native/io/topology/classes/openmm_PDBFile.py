def from_openmm_PDBFile(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_PDBFile import to_openmm_Topology as openmm_PDBFile_to_openmm_Topology
    from .openmm_Topology import from_openmm_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = openmm_PDBFile_to_openmm_Topology(item, molecular_system=molecular_system)
    tmp_item, tmp_molecular_system = openmm_Topology_to_molsysmt_Topology(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices)

    return tmp_item, tmp_molecular_system

