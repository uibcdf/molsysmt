def to_string_pdb_text(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.native.io.molsys import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.api_forms.api_openmm_Topology import to_string_pdb_text as openmm_Topology_to_string_pdb_text

    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_openmm_Topology(item, molecular_system=molecular_system)
    tmp_item, tmp_molecular_system = openmm_Topology_to_string_pdb_text(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item, tmp_molecular_system

