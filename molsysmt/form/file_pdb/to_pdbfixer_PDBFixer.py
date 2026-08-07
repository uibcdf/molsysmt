from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pdb')
def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from pdbfixer.pdbfixer import PDBFixer
    from ..pdbfixer_PDBFixer.extract import extract as extract_pdbfixer_PDBFixer

    tmp_item = PDBFixer(item)
    tmp_item = extract_pdbfixer_PDBFixer(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, skip_digestion=True)

    return tmp_item

