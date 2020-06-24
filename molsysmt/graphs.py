def bondgraph(item, nodes_name='atom_index', selection='all', syntaxis='MolSysMT',
              to_form='NetworkX'):

    # tengo que incluir la forma NetworkX para convertir.
    # en el caso de convert, lo que obtengo es una red con el nombre de los nodos dado por la
    # con el indice de atomo empezando por cero (todavía no lo he decidido)

    # el caso de este método es que nos da un grafo con los nodos nombrados según
    # nodes_name en ['atom_index', 'short_string', 'long_string']

    tmp_item = None

    if to_form is 'NetworkX':

        from networkx import Graph
        from molsysmt import get

        G = Graph()

        if nodes_name is 'atom_index':

            bonded_atoms = get(item, target='atom', selection=selection, syntaxis=syntaxis, inner_bonded_atoms=True)

            G.add_edges_from(bonded_atoms)

        else:

            raise NotImplementedError

        tmp_item = G

    else:

        raise NotImplementedError

    return tmp_item

