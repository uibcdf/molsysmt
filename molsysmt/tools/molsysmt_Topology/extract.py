def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Topology.is_molsysmt_Topology import _checking_form
        _checking_form(item, check_form=check_form)

    if (atom_indices is 'all'):
        tmp_item = item.copy()
    elif atom_indices is not 'all':
        tmp_item = item.extract(atom_indices=atom_indices)

    return tmp_item

