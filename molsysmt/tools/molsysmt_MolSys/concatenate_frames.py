def concatenate_frames(item, step=None, time=None, coordinates=None, box=None, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_MolSys.is_molsysmt_MolSys import _checking_form
        _checking_form(item, check_form=check_form)

    tmp_item = extract(item)
    tmp_item.append_frames(step=step, time=time, coordinates=coordinates, box=box)

    return tmp_item

