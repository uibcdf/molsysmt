def bondgraph(molecular_system, nodes_name='atom_index', selection='all', syntaxis='MolSysMT',
              to_form='networkx.Graph'):

    # tengo que incluir la forma NetworkX para convertir.
    # en el caso de convert, lo que obtengo es una red con el nombre de los nodos dado por la
    # con el indice de atomo empezando por cero (todavía no lo he decidido)

    # el caso de este método es que nos da un grafo con los nodos nombrados según
    # nodes_name en ['atom_index', 'short_string', 'long_string']

    from molsysmt._private_tools.molecular_system import digest_molecular_system
    from molsysmt._private_tools.forms import digest_to_form

    molecular_system = digest_molecular_system(molecular_system)
    tmp_molecular_system = None

    to_form = digest_to_form(to_form)

    if to_form == 'networkx.Graph':

        from networkx import Graph
        from molsysmt.basic import get

        G = Graph()

        if nodes_name is 'atom_index':

            atom_indices, bonded_atoms = get(molecular_system, target='atom', selection=selection,
                                             syntaxis=syntaxis, atom_index=True, inner_bonded_atoms=True)

            G.add_nodes_from(atom_indices)
            G.add_edges_from(bonded_atoms)

        else:

            raise NotImplementedError

        tmp_molecular_system = G

    else:

        raise NotImplementedError

    return tmp_molecular_system

