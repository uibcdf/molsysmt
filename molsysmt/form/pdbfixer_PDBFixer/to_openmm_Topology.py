from molsysmt._private.digestion import digest

@digest(form='pdbfixer.PDBFixer')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all'):

    from ..openmm_Topology import extract as extract_openmm_Topology

    tmp_item = item.topology
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

def _to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)

