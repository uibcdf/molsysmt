from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.digestion import *
from networkx import Graph
from molsysmt.basic import get

def get_bondgraph(molecular_system, nodes_name='atom_index', selection='all', syntaxis='MolSysMT',
              to_form='networkx.Graph', check=True):

    # tengo que incluir la forma NetworkX para convertir.
    # en el caso de convert, lo que obtengo es una red con el nombre de los nodos dado por la
    # con el indice de atomo empezando por cero (todavía no lo he decidido)

    # el caso de este método es que nos da un grafo con los nodos nombrados según
    # nodes_name en ['atom_index', 'short_string', 'long_string']

    if check:
        from molsysmt.tools.molecular_system import is_molecular_system
        if not is_molecular_system(molecular_system):
            raise MolecularSystemNeededError()

    tmp_molecular_system = None

    to_form = digest_to_form(to_form)

    if to_form == 'networkx.Graph':

        G = Graph()

        if nodes_name is 'atom_index':

            atom_indices, bonded_atoms = get(molecular_system, target='atom', selection=selection,
                                             syntaxis=syntaxis, atom_index=True,
                                             inner_bonded_atoms=True, check=False)

            G.add_nodes_from(atom_indices)
            G.add_edges_from(bonded_atoms)

        else:

            raise NotImplementedError

        tmp_molecular_system = G

    else:

        raise NotImplementedError

    return tmp_molecular_system

