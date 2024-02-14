from molsysmt._private.digestion import digest

@digest(form='file:pdb')
def to_openmm_PDBFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from openmm.app.pdbfile import PDBFile
    from ..openmm_PDBFile import extract as extract_openmm_PDBFile

    tmp_item = PDBFile(item)
    tmp_item = extract_openmm_PDBFile(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
                                      copy_if_all=False, skip_digestion=True)

    return tmp_item

