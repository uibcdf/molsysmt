from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form='molsysviewer.MolSysView')
def to_molsysviewer_MolSysView(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from molsysviewer.MolSysView to molsysviewer.MolSysView.

    Parameters
    ----------
    item : molsysviewer.MolSysView
        Source item in molsysviewer.MolSysView form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysviewer.MolSysView
        Resulting object in molsysviewer.MolSysView form.

    .. versionadded:: 1.0.0
    """

    from molsysviewer import MolSysView
    from molsysmt.basic import extract
    from molsysmt.form.molsysmt_MolSys.to_molsysmt_MolSys import to_molsysmt_MolSys

    if is_all(atom_indices) and is_all(structure_indices):
        return item

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    if tmp_item is None:
        return None

    tmp_item = extract(tmp_item, selection=atom_indices, structure_indices=structure_indices, skip_digestion=True)

    view = MolSysView()
    view.load(tmp_item, selection='all', structure_indices='all', syntax='MolSysMT')

    return view
