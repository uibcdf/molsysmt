import numpy as np
from networkx import connected_components
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError, NotImplementedMethodError


@signal(tags=["api", "chemical_states"])
@arg_digest()
def get_covalent_blocks(
    molecular_system,
    selection="all",
    remove_bonds=None,
    output_type="sets",
    syntax="MolSysMT",
    *,
    chemical_state="reference",
    structure_indices="all",
    skip_digestion=False,
):
    """
    Identifying the sets of atoms that remain covalently connected when bonds are removed.

    The purpose of this function is `remove_bonds`: it answers which atoms would still
    hold together if the given bonds were cut. That is how the groups of atoms rotating
    around a dihedral angle are obtained, for example.

    Without cuts, this partitions the selected induced graph in the requested
    chemical state. An omitted atom cannot connect two selected atoms. With all
    atoms and the reference covalent graph, these are the system's components.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    remove_bonds : list, tuple, numpy.ndarray, or None, default=None
        Zero-based atom-index pairs removed before finding covalent blocks.
    output_type : str, default='sets'
        Representation used for the returned result.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    chemical_state : str, int or None, default='reference'
        State supplying stored relationships. 'structure' resolves the state
        assigned to the selected structures, which must agree on one state.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Source structure indices used for state resolution and spatial selections.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    numpy.ndarray or list
        Object array of sets of full source atom indices, or an integer array
        with one block label per source atom and -1 at every unselected atom.
        Blocks are ordered by their smallest atom index; empty selections give
        an empty set array or an all-minus-one label array.


    Raises
    ------
    NotImplementedMethodError
        If `output_type` is unsupported.
    ArgumentError
        If an index, selection, cut shape or state request is invalid.
    StructuralInconsistencyError
        If the state is unavailable or selected structures have missing/mixed
        chemical-state associations.


    Notes
    -----
    - Builds a bond graph with `get_bondgraph` and returns its connected components
      after removing the requested bonds.
    - The blocks are not the `component` attribute of the system unless `remove_bonds`
      is `None` and `selection` is `'all'`. With either of them the result describes a
      hypothetical connectivity, not the system's own components.


    See Also
    --------
    :func:`molsysmt.basic.get`
        Retrieving `component_index` and the rest of the system's own attributes.
    :func:`molsysmt.chemical_states.get_covalent_paths`
        Finding paths of covalently bonded atoms matching an ordered pattern.


    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    from . import get_bondgraph

    G = get_bondgraph(
        molecular_system,
        nodes_name="atom_index",
        selection=selection,
        syntax=syntax,
        chemical_state=chemical_state,
        structure_indices=structure_indices,
    )

    if remove_bonds is not None:
        if type(remove_bonds) in [list, tuple]:
            remove_bonds = np.array(remove_bonds)

        if len(remove_bonds.shape) == 1:
            if remove_bonds.shape[0] == 2:
                remove_bonds = remove_bonds.reshape([1, 2])
            else:
                raise ArgumentError(
                    "remove_bonds",
                    value=remove_bonds,
                    caller="molsysmt.chemical_states.get_covalent_blocks",
                    message="Input argument bonded_atoms with wrong shape",
                )
        elif len(remove_bonds.shape) == 2:
            if remove_bonds.shape[1] != 2:
                raise ArgumentError(
                    "remove_bonds",
                    value=remove_bonds,
                    caller="molsysmt.chemical_states.get_covalent_blocks",
                    message="Input argument bonded_atoms with wrong shape",
                )
        else:
            raise ArgumentError(
                "remove_bonds",
                value=remove_bonds,
                caller="molsysmt.chemical_states.get_covalent_blocks",
                message="Input argument bonded_atoms with wrong shape",
            )

        for atom_pair in remove_bonds:
            G.remove_edge(atom_pair[0], atom_pair[1])

    components = connected_components(G)

    del G

    if output_type == "sets":
        blocks = list(components)

    elif output_type == "numpy.ndarray":
        n_atoms = get(molecular_system, element="system", n_atoms=True)
        blocks = -np.ones([n_atoms], dtype=int)
        component_index = 0
        for component in components:
            blocks[list(component)] = component_index
            component_index += 1

    else:
        raise NotImplementedMethodError(
            caller="molsysmt.chemical_states.get_covalent_blocks"
        )

    return np.array(blocks, dtype=object if output_type == "sets" else int)
