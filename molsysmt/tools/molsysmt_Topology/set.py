def set_atom_name_to_atom(item, indices='all', structure_indices='all', value=None, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Topology.is_molsysmt_Topology import _checking_form
        _checking_form(item, check_form=check_form)

    from .api_molsysmt_Topology import set_atom_name_to_atom as _set

    item.atoms_dataframe.loc[indices, 'atom_name']=value

    pass


