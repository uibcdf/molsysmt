from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form='molsysmt.MolSys')
def to_molsysviewer_MolSysView(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.MolSys to molsysviewer.MolSysView.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysviewer.MolSysView
        Converted molecular system representation.
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
