import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt.element.bond import max_expected_bond_length


@arg_digest()
def get_disulfide_candidates(
    molecular_system,
    selection="all",
    structure_indices="all",
    max_bond_length=None,
    group_names=None,
    pbc=True,
    syntax="MolSysMT",
    sorted=True,
    skip_digestion=False,
):
    """Identifying candidate disulfide atom pairs in selected structures.

    Sulfur atoms in different selected groups are candidates when their
    separation does not exceed ``max_bond_length``. Geometry alone does not
    establish a covalent bond; inspect the topology to determine which bonds
    are recorded.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying atoms.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to inspect, in the requested order.
    max_bond_length : quantity or None, default=None
        Maximum S–S separation; ``None`` uses 0.205 nm.
    group_names : list of str or None, default=None
        Eligible group names; ``None`` selects ``CYS``.
    pbc : bool, default=True
        Whether to apply periodic boundary conditions when a box is available.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate ``selection``.
    sorted : bool, default=True
        Whether to sort candidate pairs by atom indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    tuple of list
        ``(atom_pairs, distances)`` with one entry per requested structure.
        Each pair array has shape ``(n_candidates, 2)`` and global atom indices;
        its aligned distance array is a quantity in nanometers. Empty evaluated
        structures contain arrays with shapes ``(0, 2)`` and ``(0,)``.

    Notes
    -----
    Candidate pairs are observations in individual structures. They do not
    change the molecular topology or imply that a recorded bond is missing.

    See Also
    --------
    :func:`molsysmt.build.get_disulfide_bonds`
        Get candidate pairs in the build API for one structure.

    .. admonition:: User guide

       See :ref:`Get disulfide bonds <Tutorial_Get_disulfide_bonds>` for a
       tutorial on per-structure candidates and the build wrapper.

    .. versionadded:: 1.0.0
    """
    from molsysmt.basic import get, select
    from molsysmt.structure import get_neighbors

    if group_names is None:
        group_names = ["CYS"]
    if max_bond_length is None:
        max_bond_length = max_expected_bond_length["protein"]["S"]["S"]

    n_structures = get(molecular_system, n_structures=True)
    if is_all(structure_indices):
        frame_indices = np.arange(n_structures, dtype=np.int64)
    else:
        frame_indices = np.atleast_1d(structure_indices)

    if is_all(selection):
        mask = None
    else:
        mask = select(molecular_system, selection=selection, syntax=syntax)

    sulfur_indices = select(
        molecular_system,
        element="atom",
        selection='atom_type=="S"',
        mask=mask,
        syntax="MolSysMT",
    )
    if len(sulfur_indices) > 0:
        group_indices, names = get(
            molecular_system,
            element="atom",
            selection=sulfur_indices,
            group_index=True,
            group_name=True,
        )
        eligible = np.isin(names, group_names)
        sulfur_indices = np.asarray(sulfur_indices)[eligible]
        group_indices = np.asarray(group_indices)[eligible]

    def empty_pairs():
        return np.empty((0, 2), dtype=np.int64)

    def empty_distances():
        return puw.quantity(np.empty(0, dtype=np.float64), "nanometers")

    if len(sulfur_indices) < 2:
        return (
            [empty_pairs() for _ in frame_indices],
            [empty_distances() for _ in frame_indices],
        )

    neighbor_pairs, neighbor_distances = get_neighbors(
        molecular_system,
        selection=sulfur_indices,
        structure_indices=frame_indices,
        threshold=max_bond_length,
        unique_pairs=True,
        pbc=pbc,
        output_type="pairs",
        output_indices="selection",
        sorted=sorted,
    )

    pairs_by_structure = []
    distances_by_structure = []
    for frame_pairs, frame_distances in zip(neighbor_pairs, neighbor_distances):
        accepted_pairs = []
        accepted_distances = []
        for pair, distance in zip(frame_pairs, frame_distances):
            first, second = pair
            if group_indices[first] == group_indices[second]:
                continue
            accepted_pairs.append((sulfur_indices[first], sulfur_indices[second]))
            accepted_distances.append(puw.get_value(distance, to_unit="nanometers"))

        if accepted_pairs:
            pairs_by_structure.append(np.asarray(accepted_pairs, dtype=np.int64))
            distances_by_structure.append(
                puw.quantity(np.asarray(accepted_distances), "nanometers")
            )
        else:
            pairs_by_structure.append(empty_pairs())
            distances_by_structure.append(empty_distances())

    return pairs_by_structure, distances_by_structure
