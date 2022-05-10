from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'file:pdb')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from pdbfixer.pdbfixer import PDBFixer
    from ..pdbfixer_PDBFixer import extract as extract_pdbfixer_PDBFixer

    tmp_item = PDBFixer(item)
    tmp_item = extract_pdbfixer_PDBFixer(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, check=False)

    return tmp_item

