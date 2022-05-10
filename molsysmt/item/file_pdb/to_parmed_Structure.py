from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_parmed_Structure(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'file:pdb')
        atom_indices = digest_atom_indices(atom_indices)

    try:
        from parmed import load_file
    except:
        raise LibraryNotFound('parmed')

    from molsysmt.item.parmed_Structure import extract

    tmp_item = load_file(item)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item

