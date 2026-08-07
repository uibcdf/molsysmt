from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.Structures', to_form='molsysmt.Structures')
def add(to_item, item, atom_indices='all', structure_indices='all',
        attribute_policy='intersection', skip_digestion=False):

    to_item.add(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        attribute_policy=attribute_policy,
        skip_digestion=True,
    )
