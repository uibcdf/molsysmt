from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.ChemicalStates")
def has_attribute(
    molecular_system, attribute, include_none=False, skip_digestion=False
):
    """Checking whether a chemical-state attribute is available."""

    from .attributes import attributes

    if not attributes[attribute]:
        return False
    if attribute == "reference_chemical_state_index":
        return (
            include_none or molecular_system.reference_chemical_state_index is not None
        )
    return True
