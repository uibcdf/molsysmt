from molsysmt._private.arg_digestion import arg_digest

@arg_digest(to_form='molsysmt.MolSys', from_form='molsysmt.MolSys')
def add(to_item, from_item, atom_indices='all', structure_indices='all', keep_ids=True,
        attribute_policy='intersection', skip_digestion=False):

    to_item.add(from_item, atom_indices=atom_indices, structure_indices=structure_indices,
                keep_ids=keep_ids, attribute_policy=attribute_policy, skip_digestion=True)
