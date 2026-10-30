import numpy as np
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.chemical_state import resolve_chemical_state
from molsysmt._private.variables import is_all
from molsysmt.basic import select


@signal(tags=["api", "chemical_states"])
@arg_digest()
@resolve_chemical_state(convert_if_missing=True)
def get_covalent_paths(
    molecular_system,
    path=None,
    selection="all",
    syntax="MolSysMT",
    *,
    chemical_state="reference",
    structure_indices="all",
    skip_digestion=False,
):
    """
    Finding paths of covalently bonded atoms matching an ordered pattern.

    Every returned path is a walk along covalent bonds whose n-th atom satisfies the
    n-th selection of `path`. Typical uses are locating the atom quartets that define
    a dihedral angle, or the donor-hydrogen pairs of a hydrogen bond.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    path : list, tuple, or numpy.ndarray, or None, default=None
        Ordered pattern containing at least one position. Each position is an
        atom-selection expression, one source atom index, or a flat collection
        of integer source atom indices. For example, ``[[0, 2], [1]]`` asks for
        two-atom walks starting at atom 0 or 2 and ending at atom 1. An empty
        position is valid and matches no walks. None and an empty outer pattern
        are invalid.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    syntax : str, default='MolSysMT'
        Selection syntax used for `selection` and each string in `path`.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    chemical_state : str, int or None, default='reference'
        State supplying the stored graph. 'structure' requires one state across
        the selected structures; explicit selection never changes the reference.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure positions used for state association and spatial selections.

    Returns
    -------
    numpy.ndarray
        Int64 array of shape ``(n_paths, len(path))`` containing full source atom
        indices. No matching walks give shape ``(0, len(path))``. A one-position
        pattern gives one column. Order within a walk follows the pattern;
        walks can revisit atoms and are not deduplicated by reversal.

    Raises
    ------
    ArgumentError
        If the pattern is missing or empty, a position is not a supported atom
        selector, or a selection or source index is invalid. Every position is
        validated even when another position matches no atoms.


    Notes
    -----
    - "Path" is used in the graph sense: a walk over the covalent bond graph. It is
      unrelated to the `chain` element of a molecular system, which is a polymer chain.
      To work with those, use :func:`molsysmt.basic.get` with `element='chain'`.
    - Only covalent bonds are traversed. See :func:`molsysmt.chemical_states.get_bondgraph`
      for the graph itself.
    - `selection` restricts every position to its selected source atoms. Numeric
      indices always refer to the complete source system, not a renumbered subset.
    - No-match results do not infer bonds, add hydrogens or indicate missing
      chemical information. Scientific prerequisites retain their own diagnostics.


    See Also
    --------
    :func:`molsysmt.chemical_states.get_covalent_blocks`
        Sets of atoms mutually connected through covalent bonds, optionally after
        removing bonds.

    Examples
    --------
    >>> import molsysmt as msm
    >>> builder = msm.MolSysBuilder()
    >>> _ = [builder.add_atom(atom_name=name, atom_type=kind)
    ...      for name, kind in [('N', 'N'), ('H', 'H'), ('O', 'O')]]
    >>> _ = builder.add_group([0, 1, 2], group_name='LIG')
    >>> _ = builder.add_bond(0, 1)
    >>> molsys = builder.build()
    >>> msm.chemical_states.get_covalent_paths(molsys, path=[[0], [1]]).tolist()
    [[0, 1]]
    >>> msm.chemical_states.get_covalent_paths(molsys, path=[[2], []]).shape
    (0, 2)

    .. admonition:: User guide

       See :ref:`Tutorial_Get_covalent_paths` for candidate patterns and no-match results.


    .. versionadded:: 1.0.0
    """

    from . import get_bondgraph

    if is_all(selection):
        mask = None
    else:
        mask = select(
            molecular_system,
            selection=selection,
            syntax=syntax,
            structure_indices=structure_indices,
        )

    path_atom_indices = []

    for sel_in_path in path:
        atom_indices = select(
            molecular_system,
            selection=sel_in_path,
            mask=mask,
            syntax=syntax,
            structure_indices=structure_indices,
        )
        path_atom_indices.append(atom_indices)

    n_positions = len(path_atom_indices)
    if any(len(indices) == 0 for indices in path_atom_indices):
        return np.empty((0, n_positions), dtype=np.int64)

    atom_indices = np.sort(np.unique(np.concatenate(path_atom_indices)))

    graph = get_bondgraph(
        molecular_system,
        selection=atom_indices,
        nodes_name="atom_index",
        structure_indices=structure_indices,
    )

    output = [[ii] for ii in path_atom_indices[0]]
    for position in range(n_positions):
        path_atom_indices[position] = set(path_atom_indices[position])

    for position in range(1, n_positions):
        previous_position = position - 1
        tmp_output = output.copy()
        output = []
        for walk in tmp_output:
            for ii in graph.neighbors(walk[previous_position]):
                if ii in path_atom_indices[position]:
                    new_walk = walk.copy()
                    new_walk.append(ii)
                    output.append(new_walk)
    del graph

    return np.asarray(output, dtype=np.int64).reshape(-1, n_positions)
