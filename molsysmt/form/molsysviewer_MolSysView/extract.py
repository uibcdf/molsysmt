from molsysmt._private.argdigest import arg_digest

form = 'molsysviewer.MolSysView'


@arg_digest(form=form)
def extract(item, selection='all', structure_indices='all', syntax='MolSysMT', skip_digestion=False):
    """
    Extracting a subset of elements or structures from form molsysviewer.MolSysView.

    Parameters
    ----------
    item : molsysviewer.MolSysView
        Source item in molsysviewer.MolSysView form.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection of atoms or elements (0-based indices or query string).
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection`.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysviewer.MolSysView
        Resulting object in molsysviewer.MolSysView form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import extract as molsys_extract, convert
    from molsysmt.form.molsysmt_MolSys.to_molsysmt_MolSys import to_molsysmt_MolSys

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    if tmp_item is None:
        return None

    tmp_item = molsys_extract(tmp_item, selection=selection, structure_indices=structure_indices,
                              syntax=syntax, skip_digestion=True)
    return convert(tmp_item, to_form='molsysviewer.MolSysView', skip_digestion=True)
