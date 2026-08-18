from .water_names import water_names

def is_water(name):
    """
    Check whether a group name corresponds to a water molecule.


    Parameters
    ----------
    name : object
        Argument name.

    Returns
    -------
    bool
        True if ``name`` belongs to the set of known water group names, False
        otherwise.


    Notes
    -----
    The recognised names are defined in
    ``molsysmt.element.group.water.water_names``.


    .. versionadded:: 1.0.0
    """

    return (name in water_names)

