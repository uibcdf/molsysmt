from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='nglview.NGLWidget')
def merge(items, atom_indices='all', structure_indices='all', keep_ids=True, skip_digestion=False):
    """
    Merging multiple items into a single item of form nglview.NGLWidget.


    Parameters
    ----------
    items : object
        Argument items.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    keep_ids : object, default=True
        Argument keep_ids.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    nglview.NGLWidget
        Resulting object in nglview.NGLWidget form.


    .. versionadded:: 1.0.0
    """

    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from ..molsysmt_MolSys.merge import merge as merge_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys.to_nglview_NGLWidget import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget

    if is_all(atom_indices):
        atom_indices = ['all' for ii in range(len(items))]

    if is_all(structure_indices):
        structure_indices = ['all' for ii in range(len(items))]

    items_molsysmt_MolSys = [to_molsysmt_MolSys(item, skip_digestion=True) for item, ii, jj in zip(items, atom_indices, structure_indices)]
    merged_items_molsysmt_MolSys = merge_molsysmt_MolSys(items_molsysmt_MolSys, keep_ids=keep_ids, skip_digestion=True)
    merged_nglview_NGLWidget = molsysmt_MolSys_to_nglview_NGLWidget(merged_items_molsysmt_MolSys, skip_digestion=True)

    return merged_nglview_NGLWidget

