from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from networkx import Graph

def get_bondgraph(molecular_system, nodes_name='atom_index', selection='all', syntaxis='MolSysMT',
              to_form='networkx.Graph', check=True):

    # tengo que incluir la forma NetworkX para convertir.
    # en el caso de convert, lo que obtengo es una red con el nombre de los nodos dado por la
    # con el indice de atomo empezando por cero (todavía no lo he decidido)

    # el caso de este método es que nos da un grafo con los nodos nombrados según
    # nodes_name en ['atom_index', 'short_string', 'long_string']

    if check:

        digest_single_molecular_system(molecular_system)
        syntaxis = digest_syntaxis(syntaxis)
        selection = digest_selection(selection, syntaxis)
        to_form = digest_to_form(to_form)

    from molsysmt.basic import get

    output = None

    if to_form == 'networkx.Graph':

        G = Graph()

        if nodes_name is 'atom_index':

            atom_indices, bonded_atoms = get(molecular_system, element='atom', selection=selection,
                                             syntaxis=syntaxis, atom_index=True,
                                             inner_bonded_atoms=True, check=False)

            G.add_nodes_from(atom_indices)
            G.add_edges_from(bonded_atoms)

        else:

            raise NotImplementedError

        output = G

    else:

        raise NotImplementedError

    return output

