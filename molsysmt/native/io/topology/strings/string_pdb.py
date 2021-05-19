def to_string_pdb(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology
    from molsysmt.forms.classes.api_openmm_Topology import to_string_pdb as openmm_Topology_to_string_pdb

    tmp_item, tmp_molecular_system =  molsysmt_Topology_to_openmm_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system =  openmm_Topology_to_string_pdb(tmp_item, tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def from_string_pdb(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.strings.api_string_pdb import to_openmm_PDBFile as string_pdb_to_openmm_PDBFile
    from molsysmt.native.io.topology.classes import from_openmm_PDBFile as openmm_PDBFile_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = string_pdb_to_openmm_PDBFile(item, molecular_system)
    tmp_item, tmp_molecular_system = openmm_PDBFile_to_molsysmt_Topology(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

