def is_form(item):
    """Checking whether an item is a typed InteractionsDict payload."""

    from molsysmt.native import InteractionsDict

    return isinstance(item, InteractionsDict)
