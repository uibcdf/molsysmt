def concatenate_frames(item, step=None, time=None, coordinates=None, box=None, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_MolSys(item):
            raise ItemWithWrongForm('molsysmt.MolSys')

    tmp_item = extract(item)
    tmp_item.append_frames(step=step, time=time, coordinates=coordinates, box=box)

    return tmp_item

