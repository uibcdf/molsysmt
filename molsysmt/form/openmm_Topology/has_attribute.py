from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Topology')
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    """
    Checking if form openmm.Topology supports a specific attribute.

    Parameters
    ----------
    attribute : str
        Attribute name to query.

    Returns
    -------
    bool
        True if attribute is supported, False otherwise.
    """

    from . import attributes

    output = attributes[attribute]

    if not include_none:

        if attribute in ['box', 'box_shape', 'box_angles', 'box_lengths', 'box_volume']:
            if molecular_system.getPeriodicBoxVectors() is None:
                output = False

    return output

