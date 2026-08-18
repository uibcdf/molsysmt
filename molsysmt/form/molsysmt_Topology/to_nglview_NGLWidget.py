from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest


@arg_digest(form="molsysmt.Topology")
@dep_digest("nglview")
def to_nglview_NGLWidget(
    item,
    coordinates=None,
    box=None,
    atom_indices="all",
    skip_digestion=False,
):
    """
    Converting from molsysmt.Topology to nglview.NGLWidget.


    Parameters
    ----------
    item : molecular system
        Argument item.
    coordinates : object, default=None
        Argument coordinates.
    box : object, default=None
        Argument box.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    nglview.NGLWidget
        Resulting object in nglview.NGLWidget form.


    .. versionadded:: 1.0.0
    """

    if coordinates is None:
        from molsysmt._private.smonitor import NotCompatibleConversionError

        raise NotCompatibleConversionError(
            "molsysmt.Topology",
            "nglview.NGLWidget",
            {"coordinates"},
            caller="molsysmt.form.molsysmt_Topology.to_nglview_NGLWidget",
        )

    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys.to_nglview_NGLWidget import (
        to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget,
    )

    molsys = to_molsysmt_MolSys(
        item,
        coordinates=coordinates,
        box=box,
        atom_indices=atom_indices,
        skip_digestion=True,
    )

    return molsysmt_MolSys_to_nglview_NGLWidget(molsys, skip_digestion=True)
