from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import networkx as nx
import numpy as np

@arg_digest(form='openmm.Topology')
def to_networkx_Graph(item, atom_indices='all', skip_digestion=False):
    """
    Converting from openmm.Topology to networkx.Graph.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    networkx.Graph
        Resulting object in networkx.Graph form.


    .. versionadded:: 1.0.0
    """

    g = nx.Graph()

    if is_all(atom_indices):

        g.add_nodes_from(range(item.getNumAtoms()))

        output=[[bond.atom1.index, bond.atom2.index] for bond in item.bonds()]
        g.add_edges_from(np.array(output))
        del output

    else:

        raise NotImplementedError

    return g
