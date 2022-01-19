def add(to_item, item, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Trajectory.is_molsysmt_Trajectory import _checking_form
        _checking_form(to_item, check_form=check_form)
        _checking_form(item, check_form=check_form)

    raise NotImplementedError

