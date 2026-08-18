from copy import copy
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='nglview.NGLWidget')
@dep_digest('nglview')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of elements or structures from form nglview.NGLWidget.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    copy_if_all : object, default=True
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    nglview.NGLWidget
        Resulting object in nglview.NGLWidget form.


    .. versionadded:: 1.0.0
    """

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:
            tmp_item = copy(item)
        else:
            tmp_item = item
    else:

        from molsysmt.form.nglview_NGLWidget.to_molsysmt_MolSys import to_molsysmt_MolSys as nglview_NGLWidget_to_molsysmt_MolSys
        from molsysmt.form.molsysmt_MolSys.to_nglview_NGLWidget import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget
        
        tmp_item = nglview_NGLWidget_to_molsysmt_MolSys(item, atom_indices=atom_indices, 
                                                        structure_indices=structure_indices, skip_digestion=True)
        tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item, skip_digestion=True)

    return tmp_item

