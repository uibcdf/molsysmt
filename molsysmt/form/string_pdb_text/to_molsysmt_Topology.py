from molsysmt._private.digestion import digest

@digest(form='string:pdb_text')
def to_molsysmt_Topology(item, atom_indices='all', structure_indices='all'):

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import to_molsysmt_Topology as openmm_PDBFile_to_molsysmt_Topology

    tmp_item = to_openmm_PDBFile(item)
    tmp_item = openmm_PDBFile_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

def _to_molsysmt_Topology(item, atom_indices='all', structure_indices='all'):

    return to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


