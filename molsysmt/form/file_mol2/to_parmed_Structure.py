from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_parmed_Structure(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'file:mol2')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    try:
        from parmed import load_file
    except:
        raise LibraryNotFound('parmed')

    from molsysmt.form.parmed_Structure import extract

    tmp_item = load_file(item)
    tmp_item = tmp_item.to_structure()
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item

