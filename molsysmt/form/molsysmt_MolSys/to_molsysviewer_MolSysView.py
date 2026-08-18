from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form='molsysmt.MolSys')
def to_molsysviewer_MolSysView(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.MolSys to molsysviewer.MolSysView.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
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

    if not (is_all(atom_indices) and is_all(structure_indices)):
        tmp_item = extract(item, selection=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    else:
        tmp_item = item

    view = MolSysView()
    view.load(tmp_item, selection='all', structure_indices='all', syntax='MolSysMT')

    return view
