from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.HDF5TrajectoryFile')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    """
    Checking if form mdtraj.HDF5TrajectoryFile supports a specific attribute.

    Parameters
    ----------
    molecular_system : object
        Argument molecular_system.
    attribute : str
        Attribute name to query.
    include_none : object
        Argument include_none.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """

    from . import attributes

    output = attributes[attribute]

    if not include_none:
        pass

    return output

