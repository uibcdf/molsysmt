def is_form(item):
    """Checking whether an item is a native ChemicalStates collection."""

    from molsysmt.native import ChemicalStates

    return isinstance(item, ChemicalStates)
