def add(to_item, item, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Trajectory import is_molsymst_Trajectory
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_Trajectory(item):
            raise ItemWithWrongForm('molsysmt.Trajectory')
        if not is_molsysmt_Trajectory(to_item):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    raise NotImplementedError

