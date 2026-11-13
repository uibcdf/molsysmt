from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.variables import is_all


@arg_digest(form="networkx.Graph")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
):
    """Copying or explicitly reusing an unrestricted molecular graph.

    Parameters
    ----------
    item : molecular system
        NetworkX graph with the supported scalar molecular metadata.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Only the unrestricted atom axis is supported by this adapter.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Only 'all' is accepted; the graph has no coordinate structure axis.
    copy_if_all : bool, default=True
        Return a NetworkX graph copy. False reuses the unrestricted source.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    networkx.Graph
        Complete graph with unchanged node keys, edges and supported metadata.
        A graph copy owns its structure and attribute dictionaries; arbitrary
        nested extension values retain NetworkX's ordinary shallow-copy rules.

    Raises
    ------
    NotImplementedMethodError
        If explicit atom or structure selection is requested. No partial result
        is constructed or source data modified by this refusal.

    Notes
    -----
    Passing the 'all' sentinel to Graph.subgraph would interpret it as node
    labels. Unrestricted reuse returns the existing graph instead. Selected
    molecular subgraphs need an explicit node-index and chemical-reference
    remapping contract; this adapter does not invent one.

    Examples
    --------
    >>> import networkx as nx
    >>> graph = nx.path_graph(3)
    >>> extract(graph, copy_if_all=False) is graph
    True
    >>> copied = extract(graph)
    >>> copied is graph, list(copied.edges)
    (False, [(0, 1), (1, 2)])

    .. versionadded:: 1.0.0
    """

    if not (is_all(atom_indices) and is_all(structure_indices)):
        raise NotImplementedMethodError(
            "Selected molecular extraction from networkx.Graph is unavailable."
        )
    return item.copy() if copy_if_all else item
