def append_structures(item, step=None, time=None, coordinates=None, box=None, check=True):

    if check:
        from molsysmt.tools.string_pdb_id.is_string_pdb_id import _checking_form
        _checking_form(item, check=check)

    raise NotImplementedError()

