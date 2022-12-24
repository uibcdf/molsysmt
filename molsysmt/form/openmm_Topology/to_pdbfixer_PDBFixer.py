from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_pdbfixer_PDBFixer(item, atom_indices='all', coordinates=None, digest=True):

    from . import to_string_pdb_text as to_string_pdb_text
    from ..string_pdb_text import to_pdbfixer_PDBFixer as string_pdb_text_to_pdbfixer_PDBFixer

    tmp_item = to_string_pdb_text(item, atom_indices=atom_indices, coordinates=coordinates, digest=False)
    tmp_item = string_pdb_text_to_pdbfixer_PDBFixer(tmp_item, digest=False)

    return tmp_item

