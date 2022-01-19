def concatenate_frames(item, step=None, time=None, coordinates=None, box=None, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Trajectory.is_molsysmt_Trajectory import _checking_form
        _checking_form(item, check_form=check_form)

    raise NotImplementedError

