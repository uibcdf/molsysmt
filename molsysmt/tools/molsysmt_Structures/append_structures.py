def append_structures(item, step=None, time=None, coordinates=None, box=None, check=True):

    if check:
        from molsysmt.tools.molsysmt_Structures.is_molsysmt_Structures import _checking_form
        _checking_form(item, check=check)

    raise NotImplementedError

