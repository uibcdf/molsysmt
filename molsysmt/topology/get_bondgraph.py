from molsysmt._private.digestion import digest
from networkx import Graph

@digest()
def get_bondgraph(molecular_system, nodes_name='atom_index', selection='all', syntax='MolSysMT',
              to_form='networkx.Graph'):

    # tengo que incluir la forma NetworkX para convertir.
    # en el caso de convert, lo que obtengo es una red con el nombre de los nodos dado por la
    # con el indice de atomo empezando por cero (todavía no lo he decidido)

    # el caso de este método es que nos da un grafo con los nodos nombrados según
    # nodes_name en ['atom_index', 'short_string', 'long_string']

    from molsysmt.basic import get

    output = None

    if to_form == 'networkx.Graph':

        G = Graph()

        if nodes_name is 'atom_index':

            atom_indices, bonded_atoms = get(molecular_system, element='atom', selection=selection, syntax=syntax,
                                             atom_index=True, inner_bonded_atoms=True)

            G.add_nodes_from(atom_indices)
            G.add_edges_from(bonded_atoms)

        else:

            raise NotImplementedError

        output = G

    else:

        raise NotImplementedError

    return output

