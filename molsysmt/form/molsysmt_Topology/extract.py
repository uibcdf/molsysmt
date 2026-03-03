from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.Topology')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    from molsysmt.native import Topology
    if not isinstance(item, Topology):
        from molsysmt.basic import convert
        item = convert(item, to_form='molsysmt.Topology', skip_digestion=True)

    if is_all(atom_indices):
        if copy_if_all:
            tmp_item = item.copy()
        else:
            tmp_item = item
    else:
        tmp_item = item.extract(atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

