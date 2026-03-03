from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='string:pdb_id')
def to_openmm_PDBFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from .to_string_pdb_text import to_string_pdb_text
    from ..string_pdb_text.to_openmm_PDBFile import to_openmm_PDBFile as string_pdb_text_to_openmm_PDBFile

    tmp_item = to_string_pdb_text(item, skip_digestion=True)
    tmp_item = string_pdb_text_to_openmm_PDBFile(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

