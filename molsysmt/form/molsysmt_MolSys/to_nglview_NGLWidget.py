from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form='molsysmt.MolSys')
def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.MolSys to nglview.NGLWidget.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    nglview.NGLWidget
        Resulting object in nglview.NGLWidget form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import extract
    try:
        from nglview import show_molsysmt
    except ImportError:
        from molsysmt.third_party.nglview.molsysmt_trajectory import show_molsysmt

    if not (is_all(atom_indices) and is_all(structure_indices)):
        tmp_item = extract(item, selection=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    else:
        tmp_item = item

    tmp_item = show_molsysmt(tmp_item, skip_digestion=True)

    return tmp_item
