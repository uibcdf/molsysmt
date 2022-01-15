def add(to_item, item, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Topology import is_molsymst_Topology
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_Topology(item):
            raise ItemWithWrongForm('molsysmt.Topology')
        if not is_molsysmt_Topology(to_item):
            raise ItemWithWrongForm('molsysmt.Topology')

    raise NotImplementedError

