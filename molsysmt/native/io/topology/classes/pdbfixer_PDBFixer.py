def from_pdbfixer_PDBFixer(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from .openmm_Topology import from_openmm_Topology as openmm_Topology_to_molsysmt_Topology
    from molsysmt.forms.classes.api_pdbfixer_PDBFixer import to_openmm_Topology as pdbfixer_PDBFixer_to_molsysmt_Topology

    tmp_item = pdbfixer_PDBFixer_to_molsysmt_Topology(item)
    tmp_item = openmm_Topology_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

def to_pdbfixer_PDBFixer(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from .openmm_Topology import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology
    from molsysmt.forms.classes.api_openmm_Topology import to_pdbfixer_PDBFixer as openmm_Topology_to_pdbfixer_PDBFixer

    tmp_item = molsysmt_Topology_to_openmm_Topology
    tmp_item = openmm_Topology_to_pdbfixer_PDBFixer(tmp_item, trajectory_item=trajectory_item,
                                                    atom_indices=atom_indes,
                                                    frame_indices=frame_indices)

    return tmp_item

