from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.ChemicalStatesDict")
def has_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    """Checking whether a typed chemical-state attribute is available."""

    from .attributes import attributes

    if not attributes[attribute]:
        return False
    if attribute == "reference_chemical_state_index":
        data = molecular_system.data
        return include_none or data["reference_chemical_state_index"] is not None or len(data["states"]) == 1
    return True
