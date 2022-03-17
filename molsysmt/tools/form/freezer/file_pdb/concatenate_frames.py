def concatenate_structures(item, step=None, time=None, coordinates=None, box=None, check=True):

    if check:
        from molsysmt.tools.file_pdb.is_file_pdb import _checking_form
        _checking_form(item, check=check)

    raise NotImplementedError

