from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form='molsysviewer.MolSysView')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', get_missing_bonds=True,
                       skip_digestion=False):
    """
    Converting from molsysviewer.MolSysView to molsysmt.MolSys.

    Parameters
    ----------
    item : molsysviewer.MolSysView
        Source item in molsysviewer.MolSysView form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    get_missing_bonds : object
        Argument get_missing_bonds.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import extract

    molsys = getattr(item, '_molsys', None)
    if molsys is None:
        return None

    if not (is_all(atom_indices) and is_all(structure_indices)):
        molsys = extract(molsys, selection=atom_indices, structure_indices=structure_indices, skip_digestion=True)

    return molsys
