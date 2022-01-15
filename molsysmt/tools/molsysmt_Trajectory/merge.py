def merge(item_1, item_2, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Trajectory import is_molsymst_Trajectory
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_Trajectory(item_1):
            raise ItemWithWrongForm('molsysmt.Trajectory')
        if not is_molsysmt_Trajectory(item_2):
            raise ItemWithWrongForm('molsysmt.Trajectory')

    raise NotImplementedError

