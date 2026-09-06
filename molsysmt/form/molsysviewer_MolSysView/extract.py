from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

form = 'molsysviewer.MolSysView'


@arg_digest(form=form)
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of elements or structures from form molsysviewer.MolSysView.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    copy_if_all : bool, default=True
        Whether a copy is returned when every atom and every structure is extracted.
        With False the same object is returned.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysviewer.MolSysView
        Resulting object in molsysviewer.MolSysView form.


    .. versionadded:: 1.0.0
    """

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:
            from .copy import copy as copy_molsysviewer_MolSysView
            return copy_molsysviewer_MolSysView(item, skip_digestion=True)

        return item

    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from ..molsysmt_MolSys.to_molsysviewer_MolSysView import to_molsysviewer_MolSysView

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                  structure_indices=structure_indices, skip_digestion=True)
    if tmp_item is None:
        return None

    return to_molsysviewer_MolSysView(tmp_item, skip_digestion=True)
