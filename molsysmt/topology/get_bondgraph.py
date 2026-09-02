from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError
from networkx import Graph
from smonitor import signal

@signal(tags=['api', 'topology'])
@arg_digest()
def get_bondgraph(molecular_system, nodes_name='atom_index', selection='all', syntax='MolSysMT',
              to_form='networkx.Graph'):
    """
    Building a bond graph from a molecular system.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    nodes_name : str, default='atom_index'
        Atom attribute used to label graph nodes.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    to_form : str, default='networkx.Graph'
        Graph form to return; only `'networkx.Graph'` is currently implemented.

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
    >>> from molsysmt.topology.get_bondgraph import get_bondgraph
    >>> G = get_bondgraph(systems['pentalanine']['pentalanine.prmtop'])
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

            raise NotImplementedMethodError(caller='molsysmt.topology.get_bondgraph')

        output = G

    else:

        raise NotImplementedMethodError(caller='molsysmt.topology.get_bondgraph')

    return output
