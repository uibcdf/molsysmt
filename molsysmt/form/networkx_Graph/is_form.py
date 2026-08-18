def is_form(item):
    """
    Checking whether an item is an instance of form networkx.Graph.

    Parameters
    ----------
    item : networkx.Graph
        Source item in networkx.Graph form.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.

    .. versionadded:: 1.0.0
    """
    import networkx as nx

    return isinstance(item, nx.Graph)
