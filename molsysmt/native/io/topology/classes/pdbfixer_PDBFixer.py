def from_pdbfixer_PDBFixer(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from .openmm_Topology import from_openmm_Topology as openmm_Topology_to_molsysmt_Topology
    from molsysmt.forms.classes.api_pdbfixer_PDBFixer import to_openmm_Topology as pdbfixer_PDBFixer_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = pdbfixer_PDBFixer_to_molsysmt_Topology(item, molecular_system=molecular_system)
    tmp_item, tmp_molecular_system = openmm_Topology_to_molsysmt_Topology(tmp_item,
            molecular_system=tmp_molecular_system, atom_indices=atom_indices)

    return tmp_item, tmp_molecular_system

def to_pdbfixer_PDBFixer(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from .openmm_Topology import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology
    from molsysmt.forms.classes.api_openmm_Topology import to_pdbfixer_PDBFixer as openmm_Topology_to_pdbfixer_PDBFixer

    tmp_item, tmp_molecular_system = molsysmt_Topology_to_openmm_Topology(item,
            molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = openmm_Topology_to_pdbfixer_PDBFixer(tmp_item,
            molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

