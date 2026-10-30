from networkx import Graph
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError


@signal(tags=["api", "chemical_states"])
@arg_digest()
def get_bondgraph(
    molecular_system,
    nodes_name="atom_index",
    selection="all",
    syntax="MolSysMT",
    to_form="networkx.Graph",
    *,
    chemical_state="reference",
    structure_indices="all",
    skip_digestion=False,
):
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
    chemical_state : str, int or None, default='reference'
        State supplying stored relationships. 'structure' resolves the state
        assigned to the selected structures, which must agree on one state.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Source structure indices used for state resolution and spatial selections.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    networkx.Graph
        Induced graph on the selected atoms, with full source atom indices as
        nodes and only stored bonds whose two endpoints are selected as edges.


    Raises
    ------
    NotImplementedMethodError
        If `nodes_name` or `to_form` is not supported.
    ArgumentError
        If an index, selection or state request is invalid.
    StructuralInconsistencyError
        If the state is unavailable or selected structures have missing/mixed
        chemical-state associations.


    Notes
    -----
    - Bonds are taken from `inner_bonded_atom_pairs` at the atom level.
      Missing connectivity is not inferred or certified complete. Relationship
      types retain the existing stored-bond behavior; no extra chemical filter
      is introduced. State resolution never falls back to reference on ambiguity.
    - Nodes are ordered by source atom index, independently of selection order
      or repetition. Selecting a subset does not connect it through omitted atoms.


    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> from molsysmt.chemical_states.get_bondgraph import get_bondgraph
    >>> G = get_bondgraph(systems['pentalanine']['pentalanine.prmtop'])
    >>> G.number_of_nodes() > 0
    True


    .. versionadded:: 1.0.0
    """

    import numpy as np

    from molsysmt.basic import convert, get, get_form
    from molsysmt.native import ChemicalStates, ChemicalStatesDict, MolSys, Topology

    if chemical_state != "reference" and not isinstance(
        molecular_system, (MolSys, Topology, ChemicalStates, ChemicalStatesDict)
    ):
        molecular_system = convert(
            molecular_system,
            to_form="molsysmt.Topology"
            if get_form(molecular_system) == "molsysmt.TopologyDict"
            else "molsysmt.MolSys",
        )

    output = None

    if to_form == "networkx.Graph":
        G = Graph()

        if nodes_name == "atom_index":
            atom_indices, bonded_atoms = get(
                molecular_system,
                element="atom",
                selection=selection,
                syntax=syntax,
                chemical_state=chemical_state,
                structure_indices=structure_indices,
                atom_index=True,
                inner_bonded_atom_pairs=True,
            )

            if bonded_atoms is None:
                from molsysmt._private.smonitor import StructuralInconsistencyError

                raise StructuralInconsistencyError(
                    reason="A chemical-states domain with a selected state is required.",
                    caller="molsysmt.chemical_states.get_bondgraph",
                )
            G.add_nodes_from(np.unique(atom_indices).tolist())
            G.add_edges_from(bonded_atoms)

        else:
            raise NotImplementedMethodError(
                caller="molsysmt.chemical_states.get_bondgraph"
            )

        output = G

    else:
        raise NotImplementedMethodError(caller="molsysmt.chemical_states.get_bondgraph")

    return output
