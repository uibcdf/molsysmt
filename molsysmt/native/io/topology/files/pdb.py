def to_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt.native.io.topology.classes import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology
    from molsysmt.forms.classes.api_openmm_Topology import to_pdb as openmm_Topology_to_pdb

    tmp_item = molsysmt_Topology_to_openmm_Topology(item)
    tmp_item =  openmm_Topology_to_pdb(tmp_item, molecular_system=molecular_system,
                                       atom_indices=atom_indices, frame_indices=frame_indices,
                                       output_filename=output_filename)

    return tmp_item

def from_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.files.api_pdb import to_openmm_PDBFile as pdb_to_openmm_PDBFile
    from molsysmt.native.io.topology.classes import from_openmm_PDBFile as openmm_PDBFile_to_molsysmt_Topology

    tmp_item = pdb_to_openmm_PDBFile(item)
    tmp_item = openmm_PDBFile_to_molsysmt_Topology(tmp_item)

    return tmp_item

