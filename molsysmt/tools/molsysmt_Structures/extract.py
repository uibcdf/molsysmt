def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, check=True):

    if check:
        from molsysmt.tools.molsysmt_Structures.is_molsysmt_Structures import _checking_form
        _checking_form(item, check=check)

    if (atom_indices is 'all') and (structure_indices is 'all'):
        tmp_item = item.copy()
    else:
        tmp_item = item.extract(atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

