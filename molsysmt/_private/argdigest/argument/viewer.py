from molsysmt._private.smonitor import ArgumentError


def digest_viewer(viewer, caller=None):
    """Check if the given viewer is supported by MolSysMT.

    Parameters
    ----------
    viewer : str or None
        The name of the viewer in lowercase, or None to use default.

    Returns
    -------
    str

    Raises
    -------
    ArgumentError
    """
    if viewer is None:
        from molsysmt import configure

        viewer = getattr(configure, "default_viewer", "MolSysViewer")

    from molsysmt.supported.viewers import lowercase_viewers

    if isinstance(viewer, str) and viewer.lower() in lowercase_viewers:
        return lowercase_viewers[viewer.lower()]
    raise ArgumentError("viewer", value=viewer, caller=caller, message=None)
