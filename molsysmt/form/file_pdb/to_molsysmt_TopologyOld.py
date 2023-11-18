from molsysmt._private.digestion import digest

@digest(form='file:pdb')
def to_molsysmt_TopologyOld(item, atom_indices='all'):

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import to_molsysmt_TopologyOld as openmm_PDBFile_to_molsysmt_TopologyOld

    tmp_item = to_openmm_PDBFile(item)
    tmp_item = openmm_PDBFile_to_molsysmt_TopologyOld(tmp_item, atom_indices=atom_indices)

    return tmp_item

