from molsysmt._private.digestion import digest

@digest(form='string:pdb_text')
def to_openmm_Modeller(item, atom_indices='all', structure_indices='all'):

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import to_openmm_Modeller as openmm_PDBFile_to_openmm_Modeller

    tmp_item = to_openmm_PDBFile(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = openmm_PDBFile_to_openmm_Modeller(tmp_item)

    return tmp_item

def _to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)

