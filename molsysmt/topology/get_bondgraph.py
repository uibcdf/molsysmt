from molsysmt._private.digestion import arg_digest
from networkx import Graph

@arg_digest()
def get_bondgraph(molecular_system, nodes_name='atom_index', selection='all', syntax='MolSysMT',
              to_form='networkx.Graph'):
    """
    Building a bond graph from a molecular system.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any supported form.
    nodes_name : {'atom_index'}, default 'atom_index'
        Label to use for nodes; currently only atom indices are supported.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atom selection (MolSysMT syntax or indices) used to build the graph.
    syntax : str, default 'MolSysMT'
        Selection syntax when `selection` is a string.
    to_form : {'networkx.Graph'}, default 'networkx.Graph'
        Output graph type.

    Returns
    -------
    networkx.Graph
        Graph where nodes represent atoms and edges represent bonds.

    Raises
    ------
    NotImplementedError
        If `nodes_name` or `to_form` is not supported.

    Notes
    -----
    - Bonds are taken from `inner_bonded_atom_pairs` at the atom level.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> G = msm.topology.get_bondgraph(systems['pentalanine']['pentalanine.prmtop'])
    >>> G.number_of_nodes() > 0
    True

    .. versionadded:: 1.0.0
    """


    # tengo que incluir la forma NetworkX para convertir.
    # en el caso de convert, lo que obtengo es una red con el nombre de los nodos dado por la
    # con el indice de atomo empezando por cero (todavía no lo he decidido)

    # el caso de este método es que nos da un grafo con los nodos nombrados según
    # nodes_name en ['atom_index', 'short_string', 'long_string']

    from molsysmt.basic import get

    output = None

    if to_form == 'networkx.Graph':

        G = Graph()

        if nodes_name == 'atom_index':

            atom_indices, bonded_atoms = get(molecular_system, element='atom', selection=selection, syntax=syntax,
                                             atom_index=True, inner_bonded_atom_pairs=True)

            G.add_nodes_from(atom_indices)
            G.add_edges_from(bonded_atoms)

        else:

            raise NotImplementedError

        output = G

    else:

        raise NotImplementedError

    return output
