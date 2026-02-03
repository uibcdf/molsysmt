from molsysmt._private.exceptions import ArgumentError

def digest_viewer(viewer, caller=None):
    """ Check if the given viewer is supported by MolSysMT.

    Parameters
    ----------
    viewer : str
        The name of the viewer in lowercase.

    Returns
    -------

    Raises
    -------

    """

    from molsysmt.supported.viewers import lowercase_viewers

    try:
        tmp_viewer = lowercase_viewers[viewer.lower()]
        return tmp_viewer
    except KeyError:
        raise ArgumentError('viewer', value=viewer, caller=caller, message=None)

