def from_string_smiles (item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.api_string_smiles import to_rdkit_Mol as string_smiles_to_rdkit_Mol
    from molsysmt.native.io.topology.rdkit_Mol import from_rdkit_Mol as rdkit_Mol_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = string_smiles_to_rdkit_Mol(item,
            molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = rdkit_Mol_to_molsysmt_Topology(tmp_item,
            molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

