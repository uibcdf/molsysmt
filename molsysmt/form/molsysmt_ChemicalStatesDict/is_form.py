def is_form(item):
    """Checking whether an item is a typed ChemicalStatesDict payload."""

    from molsysmt.native import ChemicalStatesDict

    return isinstance(item, ChemicalStatesDict)
