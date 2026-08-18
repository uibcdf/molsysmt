def is_form(item):
    """
    Checking whether an item is an instance of form networkx.Graph.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form networkx.Graph, False otherwise.
    """
    import networkx as nx

    return isinstance(item, nx.Graph)
