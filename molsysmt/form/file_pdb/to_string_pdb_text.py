from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pdb')
def to_string_pdb_text(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from ..string_pdb_text.extract import extract as extract_string_pdb_text

    with open(item, 'r') as fff:
        tmp_item = fff.read()

    tmp_item = extract_string_pdb_text(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False, skip_digestion=True)

    return tmp_item
