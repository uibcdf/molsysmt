from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_openmm_PDBFile(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'file:pdb')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from openmm.app.pdbfile import PDBFile
    from ..openmm_PDBFile import extract as extract_openmm_PDBFile

    tmp_item = PDBFile(item)
    tmp_item = extract_openmm_PDBFile(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False, check=False)

    return tmp_item

