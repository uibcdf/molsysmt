def to_string_aminoacids3(item, atom_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Topology import is_molsymst_Topology
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_Topology(item):
            raise ItemWithWrongForm('molsysmt.Topology')

    from molsysmt.tools.molsysmt_Topology import get_group_name_from_atom

    group_names = get_group_name_from_atom(item, atom_indices='all')
    tmp_item = ''.join([ii.title() for ii in group_names])

    return tmp_item

