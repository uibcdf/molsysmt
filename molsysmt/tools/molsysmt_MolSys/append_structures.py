def append_structures(item, step=None, time=None, coordinates=None, box=None, check=True):

    if check:
        from molsysmt.tools.molsysmt_MolSys.is_molsysmt_MolSys import _checking_form
        _checking_form(item, check=check)

    item.trajectory.append_structures(step=step, time=time, coordinates=coordinates, box=box)

    pass

