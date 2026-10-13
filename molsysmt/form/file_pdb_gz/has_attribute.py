from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:pdb.gz")
def has_attribute(
    molecular_system, attribute, include_none=False, skip_digestion=False
):
    """Checking attribute delivery from compressed PDB inputs.

    Parameters
    ----------
    molecular_system : molecular system
        Gzip PDB path to inspect.
    attribute : str
        Registered attribute whose native PDB delivery is requested.
    include_none : bool, default=False
        Retained form-dispatch option; this reports delivery capability.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    bool
        Whether the native PDB handler can deliver the requested attribute.
    """
    from .attributes import attributes

    return attributes[attribute]
