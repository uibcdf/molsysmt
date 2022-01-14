def set_atom_name_to_atom(item, indices='all', frame_indices='all', value=None, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Topology import is_molsymst_Topology
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_Topology(item):
            raise ItemWithWrongForm('molsysmt.Topology')

    from .api_molsysmt_Topology import set_atom_name_to_atom as _set

    item.atoms_dataframe.loc[indices, 'atom_name']=value

    pass


