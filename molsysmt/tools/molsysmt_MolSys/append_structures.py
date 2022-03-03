def append_structures(item, step=None, time=None, coordinates=None, box=None, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_MolSys.is_molsysmt_MolSys import _checking_form
        _checking_form(item, check_form=check_form)

    item.trajectory.append_structures(step=step, time=time, coordinates=coordinates, box=box)

    pass

