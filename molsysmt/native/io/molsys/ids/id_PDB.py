def from_id_PDB(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.ids.api_id_PDB import to_mmtf_MMTFDecoder as id_PDB_to_mmtf_MMTFDecoder
    from molsysmt.native.io.molsys.classes import from_mmtf_MMTFDecoder as mmtf_Decoder_to_molsysmt_MolSys

    tmp_item, tmp_molecular_system = id_PDB_to_mmtf_MMTFDecoder(item, molecular_system=molecular_system, atom_indices='all', frame_indices='all')
    tmp_item, tmp_molecular_system = mmtf_Decoder_to_molsysmt_MolSys(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

    #from molsysmt.forms.ids.api_pdb import to_openmm_PDBFile as pdb_to_openmm_PDBFile
    #from molsysmt.native.io.molsys.classes import from_openmm_PDBFile as openmm_PDBFile_to_molsysmt_MolSys

    #tmp_item, tmp_molecular_system = pdb_to_openmm_PDBFile(item, molecular_system, atom_indices='all', frame_indices='all')
    #tmp_item, tmp_molecular_system = openmm_PDBFile_to_molsysmt_MolSys(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    #return tmp_item, tmp_molecular_system

