from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="nglview.NGLWidget")
@dep_digest("nglview")
def copy(item, skip_digestion=False):
    """Creating an independent widget from the represented molecular data.

    Parameters
    ----------
    item : molecular system
        Source NGL widget with one represented molecular-system component.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    nglview.NGLWidget
        New widget with independent communication, molecular topology and
        coordinate storage for the supported native conversion profile.

    Raises
    ------
    ValueError
        If multiple graphical components have no declared shared molecular axis.
    LibraryNotFoundError
        If the optional NGLView provider is unavailable.

    Notes
    -----
    Reuses native conversion and widget construction instead of Python's
    unsupported widget-copy protocol. Declared topology/chemical sidecars are
    retained by those routes. Missing bonds are not inferred. Coordinates are
    materialized with their physical units; the NGL bridge publishes angstrom
    magnitudes independently of the application's standard length unit.

    This copies the supported molecular payload. Camera, representations,
    browser state and other graphical session settings are not cloned.
    Memory use includes the materialized native coordinates and the new widget
    payload; this is not a streaming or copy-on-write operation.

    See Also
    --------
    molsysmt.basic.copy : Copying a molecular system through its form adapter.
    molsysmt.basic.extract : Extracting selected molecular data.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['Met-enkephalin']['met_enkephalin.pdb'],
    ...                      to_form='molsysmt.MolSys')
    >>> widget = msm.convert(molsys, to_form='nglview.NGLWidget')
    >>> copied = copy(widget)
    >>> copied is widget, copied.comm is widget.comm
    (False, False)
    >>> copied.close()
    >>> widget.close()

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolSys.to_nglview_NGLWidget import (
        to_nglview_NGLWidget,
    )

    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    molsys = to_molsysmt_MolSys(item, get_missing_bonds=False, skip_digestion=True)
    return to_nglview_NGLWidget(molsys, skip_digestion=True)
