"""Private helpers for topology snapshots attached to MolSysMT NGL trajectories."""


SIDECAR_ATTRIBUTE = "_molsysmt_topology"


def get_topology_sidecar(widget):
    """
    Getting topology sidecar from form nglview.NGLWidget.


    Parameters
    ----------
    widget : object
        Argument widget.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """

    trajectories = getattr(widget, "_trajlist", ())
    component_ids = getattr(widget, "_ngl_component_ids", ())
    if len(trajectories) != 1 or len(component_ids) != 1:
        return None
    return getattr(trajectories[0], SIDECAR_ATTRIBUTE, None)
