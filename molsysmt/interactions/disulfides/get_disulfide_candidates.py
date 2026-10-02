import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.interaction_attribution import attributed
from molsysmt._private.variables import is_all
from molsysmt.element.bond import max_expected_bond_length


@arg_digest()
@attributed("disulfides", "sulfur_sulfur_distance")
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
    *,
    output_type="tuple",
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
    output_type : {'tuple', 'molsysmt.Interactions'}, default='tuple'
        Return the existing pair and distance lists, or a sparse analysis
        with explicit evaluated coverage, atom scope, and observed images.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    tuple of list or molsysmt.Interactions
        By default, ``(atom_pairs, distances)`` with one entry per requested structure.
        Each pair array has shape ``(n_candidates, 2)`` and global atom indices;
        its aligned distance array is a quantity in nanometers. Empty evaluated
        structures contain arrays with shapes ``(0, 2)`` and ``(0,)``. The
        optional analysis uses the original system's atom and structure indices.

    Notes
    -----
    Candidate pairs are observations in individual structures. They do not
    change the molecular topology or imply that a recorded bond is missing.
    The optional analysis records the calculation-time MolSysMT version in
    ``software``, independently of the version used to save or load it.
    Analysis parameters record the sulfur_sulfur_distance criterion and
    calculation bibliography. Optional Ackredit sessions collect completed
    calculations; the default tuple output retains its existing layout.

    See Also
    --------
    :func:`molsysmt.build.get_disulfide_bonds`
        Get candidate pairs in the build API for one structure.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import pyunitwizard as puw
    >>> from molsysmt.interactions.disulfides.get_disulfide_candidates import get_disulfide_candidates
    >>> builder = msm.MolSysBuilder()
    >>> first = builder.add_atom(atom_name="SG", atom_type="S")
    >>> second = builder.add_atom(atom_name="SG", atom_type="S")
    >>> _ = builder.add_group([first], group_name="CYS")
    >>> _ = builder.add_group([second], group_name="CYS")
    >>> builder.set_coordinates(puw.quantity([[0, 0, 0], [0.2, 0, 0]], "nm"))
    >>> molsys = builder.build()
    >>> result = get_disulfide_candidates(
    ...     molsys, pbc=False, output_type="molsysmt.Interactions")
    >>> result.n_interactions
    1

    .. admonition:: User guide

       See :ref:`Get disulfide bonds <Tutorial_Get_disulfide_bonds>` for a
       tutorial on per-structure candidates and the build wrapper.

    .. versionadded:: 1.0.0
    """
    from molsysmt.basic import get, select
    from molsysmt.structure import get_neighbors

    return_interactions = str(output_type).lower() == "molsysmt.interactions"

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
        pairs = [empty_pairs() for _ in frame_indices]
        distances = [empty_distances() for _ in frame_indices]
        if return_interactions:
            return _as_interactions(
                molecular_system,
                frame_indices,
                sulfur_indices,
                pairs,
                distances,
                max_bond_length,
                group_names,
                pbc,
            )
        return pairs, distances

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

    if return_interactions:
        return _as_interactions(
            molecular_system,
            frame_indices,
            sulfur_indices,
            pairs_by_structure,
            distances_by_structure,
            max_bond_length,
            group_names,
            pbc,
        )
    return pairs_by_structure, distances_by_structure


def _as_interactions(
    molecular_system,
    frame_indices,
    sulfur_indices,
    pairs_by_structure,
    distances_by_structure,
    max_bond_length,
    group_names,
    pbc,
):
    """Build a scoped sparse analysis from the detector's aligned output."""
    from molsysmt._private.rust_backend import get_mic_pair_observations
    from molsysmt.basic import get
    from molsysmt.interactions.result import Interactions

    records = []
    visited_frames = set()
    for frame, pairs, frame_distances in zip(
        frame_indices, pairs_by_structure, distances_by_structure
    ):
        frame = int(frame)
        if frame in visited_frames:
            continue
        visited_frames.add(frame)
        if len(pairs) == 0:
            continue
        pairs = np.sort(np.asarray(pairs, dtype=np.int64), axis=1)
        distances_nm = np.asarray(
            puw.get_value(frame_distances, to_unit="nanometers"), dtype=np.float64
        )
        images = None
        if pbc:
            box = get(
                molecular_system,
                element="system",
                structure_indices=int(frame),
                box=True,
            )
            if box is not None and box[0] is not None:
                box_nm = np.asarray(puw.get_value(box, to_unit="nanometers"))
                atoms = np.unique(pairs)
                coordinates = get(
                    molecular_system,
                    element="atom",
                    selection=atoms,
                    structure_indices=int(frame),
                    coordinates=True,
                )
                coordinates_nm = np.asarray(
                    puw.get_value(coordinates, to_unit="nanometers")
                )[0]
                pair_positions = np.searchsorted(atoms, pairs)
                observed_distances, images = get_mic_pair_observations(
                    coordinates_nm[pair_positions[:, 0]],
                    coordinates_nm[pair_positions[:, 1]],
                    box_nm,
                    np.zeros(len(pairs), dtype=np.int64),
                )
                if not np.allclose(
                    observed_distances, distances_nm, atol=1e-8, rtol=1e-8
                ):
                    raise ValueError(
                        "Periodic candidate images disagree with detected distances."
                    )
        for index, (first, second) in enumerate(pairs):
            record = {
                "structure_index": int(frame),
                "interaction_type": "disulfide_candidate",
                "participants": [
                    {"role": "sulfur", "atom_indices": [int(first)]},
                    {"role": "sulfur", "atom_indices": [int(second)]},
                ],
                "measurements": {"distance": float(distances_nm[index])},
                "evidence": "geometric_proximity",
            }
            if images is not None:
                record["images"] = [[0, 0, 0], images[index].tolist()]
            records.append(record)

    from molsysmt import __version__

    return Interactions.from_records(
        records,
        n_atoms=get(molecular_system, n_atoms=True),
        n_structures=get(molecular_system, n_structures=True),
        evaluated_structure_indices=frame_indices,
        method="molsysmt.interactions.disulfides.get_disulfide_candidates",
        software={"molsysmt": __version__},
        parameters={
            "max_bond_length_nm": float(
                puw.get_value(max_bond_length, to_unit="nanometers")
            ),
            "group_names": [str(name) for name in group_names],
            "pbc": bool(pbc),
        },
        measure_units={"distance": "nm"},
        evaluation_mode="internal",
        evaluation_atom_indices=sulfur_indices,
        evaluation_universe_indices=sulfur_indices,
    )
