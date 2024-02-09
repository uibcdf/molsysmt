from molsysmt._private.digestion import digest

@digest(form='string:pdb_text')
def to_molsysmt_TopologyOld(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from . import to_openmm_PDBFile
    from ..openmm_PDBFile import to_molsysmt_Topology as openmm_PDBFile_to_molsysmt_TopologyOld

    tmp_item = to_openmm_PDBFile(item, skip_digestion=True)
    tmp_item = openmm_PDBFile_to_molsysmt_TopologyOld(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

