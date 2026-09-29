from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.InteractionsDict")
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    """Reporting supported molecular attributes for a columnar result."""

    from .attributes import attributes

    return attributes[attribute]
