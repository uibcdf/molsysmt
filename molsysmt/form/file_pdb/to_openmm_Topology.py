from molsysmt._private.digestion import digest

@digest(form='file:pdb')
def to_openmm_Topology(item, atom_indices='all'):

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import to_openmm_Topology as openmm_PDBFile_to_openmm_Topology

    tmp_item = to_openmm_PDBFile(item)
    tmp_item = openmm_PDBFile_to_openmm_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

def _to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_openmm_Topology(item, atom_indices=atom_indices)

