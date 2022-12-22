from molsysmt._private.digestion import digest

@digest(form='file:pdb')
def to_molsysmt_Topology(item, atom_indices='all', digest=True):

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import to_molsysmt_Topology as openmm_PDBFile_to_molsysmt_Topology

    tmp_item = to_openmm_PDBFile(item, digest=False)
    tmp_item = openmm_PDBFile_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, digest=False)

    return tmp_item

