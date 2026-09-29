def is_form(item):
    """Checking whether an item is a sparse Interactions result."""

    from molsysmt.interactions.result import Interactions

    return isinstance(item, Interactions)
