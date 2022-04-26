def to_pdbfixer_PDBFixer(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from .openmm_Topology import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology
    from molsysmt.api_forms.api_openmm_Topology import to_pdbfixer_PDBFixer as openmm_Topology_to_pdbfixer_PDBFixer

    tmp_item, tmp_molecular_system = molsysmt_Topology_to_openmm_Topology(item,
            molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item, tmp_molecular_system = openmm_Topology_to_pdbfixer_PDBFixer(tmp_item,
            molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

