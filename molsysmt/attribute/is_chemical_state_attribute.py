from molsysmt._private.argdigest import arg_digest


@arg_digest()
def is_chemical_state_attribute(attribute, skip_digestion=False):
    """
    Return whether an attribute requires a resolved chemical state.

    Parameters
    ----------
    attribute : object
        Argument attribute.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    """

    from . import attributes

    return attributes[attribute]['chemical_state']
