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
    """Converting a native topology into an NGLView widget.

    A topology carries no geometry, so ``coordinates`` must be supplied explicitly.
    MolSysMT never creates placeholder coordinates for visualization.

    Parameters
    ----------
    item : molsysmt.Topology
        Native topology to display.
    coordinates : quantity
        Coordinates with shape ``(n_structures, n_atoms, 3)`` and length units.
    box : quantity, optional
        Periodic boxes with shape ``(n_structures, 3, 3)`` and length units.
    atom_indices : array-like or 'all', default 'all'
        Canonical atom indices to display.
    skip_digestion : bool, default False
        Whether to bypass public argument digestion.

    Returns
    -------
    nglview.NGLWidget
        Widget initialized with the supplied topology and coordinates.

    Raises
    ------
    NotCompatibleConversionError
        If coordinates are not supplied.

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
