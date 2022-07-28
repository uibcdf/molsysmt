from molsysmt._private.digestion import digest

@digest(form='string:pdb_id')
def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all'):

    from . import to_string_pdb_text as to_string_pdb_text
    from ..string_pdb_text import to_pdbfixer_PDBFixer as string_pdb_text_to_pdbfixer_PDBFixer

    tmp_item = to_string_pdb_text(item)
    tmp_item = string_pdb_text_to_pdbfixer_PDBFixer(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

