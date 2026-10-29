from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.ChemicalStatesDict")
def has_attribute(
    molecular_system, attribute, include_none=False, skip_digestion=False
):
    """Checking whether a typed chemical-state attribute is available."""

    from .attributes import attributes

    if not attributes[attribute]:
        return False
    from molsysmt.native._chemical_dict_queries import has_attribute as available

    return bool(available(molecular_system, attribute, include_none))
