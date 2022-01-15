def merge(item_1, item_2):

    if check_form:
        from molsysmt.tools.molsysmt_Topology import is_molsymst_Topology
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_Topology(item_1):
            raise ItemWithWrongForm('molsysmt.Topology')
        if not is_molsysmt_Topology(item_2):
            raise ItemWithWrongForm('molsysmt.Topology')

    raise NotImplementedError

