from molsysmt.tools.string_pdb_id.is_string_pdb_id import is_string_pdb_id
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private_tools.atom_indices import digest_atom_indices
from molsysmt._private_tools.structure_indices import digest_structure_indices

def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all', check=True):

    if check:
        from molsysmt.tools.string_pdb_id.is_string_pdb_id import _checking_form
        _checking_form(item, check=check)

    from molsysmt.tools.string_pdb_id import to_string_pdb_text as string_pdb_id_to_string_pdb_text
    from molsysmt.tools.string_pdb_text import to_pdbfixer_PDBFixer as string_pdb_text_to_pdbfixer_PDBFixer

    tmp_item = string_pdb_id_to_string_pdb_text(item, check=False)
    tmp_item = string_pdb_text_to_pdbfixer_PDBFixer(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, check=True)

    return tmp_item

