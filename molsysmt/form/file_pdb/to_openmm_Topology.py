from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:pdb')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.form.file_pdb.to_openmm_PDBFile import to_openmm_PDBFile as file_pdb_to_openmm_PDBFile
    from molsysmt.form.openmm_PDBFile.to_openmm_Topology import to_openmm_Topology as openmm_PDBFile_to_openmm_Topology

    # Step 1: Open file using OpenMM PDB parser
    tmp_item = file_pdb_to_openmm_PDBFile(item, skip_digestion=True)
    
    # Step 2: Extract topology from the PDB object
    tmp_item = openmm_PDBFile_to_openmm_Topology(tmp_item, atom_indices=atom_indices, 
                                                 structure_indices=structure_indices, skip_digestion=True)

    return tmp_item
