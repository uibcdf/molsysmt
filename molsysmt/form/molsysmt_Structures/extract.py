from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.Structures')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    from molsysmt.native import Structures
    if not isinstance(item, Structures):
        from molsysmt.basic import convert
        item = convert(item, to_form='molsysmt.Structures', skip_digestion=True)

    if is_all(atom_indices) and is_all(structure_indices):
        tmp_item = item.copy()
    else:
        tmp_item = item.extract(atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

