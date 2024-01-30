from molsysmt._private.digestion import digest
from molsysmt._private.exceptions import LibraryNotFoundError

@digest(form='file:mol2')
def to_parmed_Structure(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    try:
        from parmed import load_file
    except:
        raise LibraryNotFoundError('parmed')

    from molsysmt.form.parmed_Structure import extract

    tmp_item = load_file(item)
    tmp_item = tmp_item.to_structure()
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False,
                       skip_digestion=True)

    return tmp_item

