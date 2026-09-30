"""Detecting minimum-distance observations between formal-charge participants."""

import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import (
    ArgumentError,
    StructuralInconsistencyError,
    UnsupportedHeavyOperationError,
)
from molsysmt._private.variables import is_all

_CALLER = "molsysmt.interactions.ionic.get_ionic_interactions"


@signal(tags=["api", "interactions"])
@arg_digest()
def get_ionic_interactions(
    molecular_system,
    distance_threshold,
    selection="all",
    selection_2=None,
    structure_indices="all",
    chemical_state="reference",
    method="minimum_distance",
    selection_mode="internal",
    pbc=True,
    assume_complete_connectivity=False,
    output_type="molsysmt.Interactions",
    syntax="MolSysMT",
    skip_digestion=False,
):
    """Detecting minimum-distance contacts between opposite formal-charge centers.

    Use the bounded formal-charge definition of get_charge_centers. One
    occurrence represents a positive/negative center pair in one structure,
    with the minimum distance between their geometry-reference atoms.
    The criterion is geometric evidence, not an electrostatic energy or bond.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system with coordinates and explicit selected-state chemistry.
    distance_threshold : quantity or str
        Explicit, finite positive distance cutoff with length units. Accept
        distances less than or equal to the cutoff, allowing one float64 ULP
        for unit-conversion roundoff; no universal default is used.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection. A selection intersecting a compound center must
        include all its atoms. Original atom indices are preserved.
    selection_2 : str, list, tuple, or numpy.ndarray or None, default=None
        Disjoint second atom selection, required only for selection_mode='between'.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to evaluate. Repeated indices are evaluated
        once, in sorted order. Empty evaluated frames remain explicit.
    chemical_state : {'reference', 'structure'}, int, or None, default='reference'
        State used to identify centers. Structure-assigned states must resolve
        to the same state for every requested structure.
    method : str, default='minimum_distance'
        Supported geometric criterion; only 'minimum_distance' is implemented.
    selection_mode : {'internal', 'incident', 'between'}, default='internal'
        Search within selection, from selection to any eligible center in the
        system, or between selection and selection_2, respectively.
    pbc : bool, default=True
        Use MIC distances when a box exists. Boxes use row lattice vectors.
        Compound participants requiring internal MIC image shifts are rejected.
    assume_complete_connectivity : bool, default=False
        Explicitly declare supplied connectivity complete when stored metadata
        is insufficient. Record the assumption without modifying the source.
    output_type : {'molsysmt.Interactions', 'molsysmt.InteractionsDict'}, default='molsysmt.Interactions'
        Sparse analysis object or its typed, versioned serialization dictionary.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate selection and selection_2.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Interactions or dict
        Sparse ionic_contact observations with positive and negative participant
        roles, distance in nm, and participant charges in elementary charge
        units. Each relation contains whole-center atoms; distance references
        follow the recorded recognition-rule version. Source axes, evaluated
        frames, eligible atom scope, parameters, evidence, and producer version
        remain explicit. Periodic images shift the whole negative participant
        relative to the positive participant. Empty measure columns have (0,).

    Raises
    ------
    ArgumentError
        If the threshold, method, selections, or search mode are invalid.
    StructuralInconsistencyError
        If required chemistry or finite coordinates/boxes are missing.
    NotImplementedMethodError
        If periodic participants require internal image shifts.
    UnsupportedHeavyOperationError
        If the estimated full source coordinate footprint exceeds the eager RAM
        budget. This initial implementation has no chunked execution route.

    Notes
    -----
    This experimental definition recognizes carboxylate and guanidinium plus
    literal formal-charge atoms/clusters; phosphate, sulfate, and aromatic
    delocalization are not resolved universally. Intramolecular contacts are
    included. Self/overlapping centers cannot occur in the recognizer's disjoint
    partition. Directly covalently bonded centers are excluded; dative bonds
    do not impose this exclusion. No residue, component, or energy exclusion
    is inferred. All source chemistry is examined before filtering centers.
    The calculation neither attaches an analysis nor modifies coordinates.
    Coordinate, candidate, and complete result arrays are currently in memory;
    the footprint check is an input estimate, not a total peak-RAM guarantee.

    See Also
    --------
    molsysmt.physchem.get_charge_centers
        Identifying state-specific chemical participants.
    molsysmt.Interactions.query
        Filtering calculated occurrences by atoms and structures.

    Examples
    --------
    >>> import molsysmt as msm
    >>> import numpy as np
    >>> from molsysmt import pyunitwizard as puw
    >>> from molsysmt.native import MolSys, Topology
    >>> from molsysmt.interactions.ionic.get_ionic_interactions import get_ionic_interactions
    >>> molsys = MolSys()
    >>> molsys.topology = Topology(n_atoms=2)
    >>> molsys.topology.atoms['atom_type'] = ['Na', 'Cl']
    >>> msm.set(molsys, element='atom', formal_charge=[1, -1])
    >>> molsys.structures.append(coordinates=puw.quantity(
    ...     np.array([[[0., 0., 0.], [0.3, 0., 0.]]]), 'nm'))
    >>> result = get_ionic_interactions(molsys, '0.4 nm', pbc=False,
    ...     assume_complete_connectivity=True)
    >>> result.n_interactions
    1
    >>> result.measure_units['distance']
    'nm'

    .. admonition:: User guide

       See :ref:`Getting ionic interactions <Tutorial_Get_ionic_interactions>`.

    .. versionadded:: 1.0.0
    """
    import molsysmt.configure as config
    from molsysmt import __version__
    from molsysmt._private.execution.memory_policy import estimate_footprint
    from molsysmt._private.h5msm import (
        maybe_read_modular_h5msm,
        modular_h5msm_dimensions,
    )
    from molsysmt.basic import convert, get, select
    from molsysmt.interactions.result import Interactions
    from molsysmt.physchem.get_charge_centers import get_charge_centers

    threshold_value = np.asarray(puw.get_value(distance_threshold, to_unit="nm"))
    if threshold_value.shape != ():
        raise ArgumentError(
            "distance_threshold",
            value=distance_threshold,
            caller=_CALLER,
            message="The distance cutoff must be a scalar quantity.",
        )
    threshold = float(threshold_value)
    if not np.isfinite(threshold) or threshold <= 0:
        raise ArgumentError(
            "distance_threshold", value=distance_threshold, caller=_CALLER
        )
    if selection_mode == "between":
        if selection_2 is None:
            raise ArgumentError(
                "selection_2",
                caller=_CALLER,
                message="Between searches require a second selection.",
            )
    elif selection_2 is not None:
        raise ArgumentError(
            "selection_2",
            caller=_CALLER,
            message="A second selection is only valid for a between search.",
        )

    dimensions = modular_h5msm_dimensions(molecular_system)
    if dimensions is None:
        dimensions = get(molecular_system, n_atoms=True, n_structures=True)
    n_atoms, n_structures = dimensions
    frames = (
        np.arange(n_structures, dtype=np.int64)
        if is_all(structure_indices)
        else np.unique(np.atleast_1d(structure_indices)).astype(np.int64)
    )
    if np.any(frames < 0) or np.any(frames >= n_structures):
        raise ArgumentError(
            "structure_indices", value=structure_indices, caller=_CALLER
        )
    if estimate_footprint(n_atoms, n_structures) > config.max_ram_usage:
        raise UnsupportedHeavyOperationError(
            operation=_CALLER,
            form="eager ionic detection",
            reason="The initial ionic method has no chunked execution route.",
        )

    molecular_system = maybe_read_modular_h5msm(molecular_system)
    centers = get_charge_centers(
        molecular_system,
        chemical_state=chemical_state,
        structure_indices=frames,
        assume_complete_connectivity=assume_complete_connectivity,
    )
    first = np.unique(
        select(
            molecular_system,
            selection=selection,
            syntax=syntax,
            structure_indices=frames,
            chemical_state=chemical_state,
        )
    ).astype(np.int64)
    second = None
    if selection_2 is not None:
        second = np.unique(
            select(
                molecular_system,
                selection=selection_2,
                syntax=syntax,
                structure_indices=frames,
                chemical_state=chemical_state,
            )
        ).astype(np.int64)
        if np.intersect1d(first, second).size:
            raise ArgumentError(
                "selection_2",
                value=selection_2,
                caller=_CALLER,
                message="Between selections must be disjoint.",
            )
    members = [
        centers["atom_indices"][start:stop]
        for start, stop in zip(
            centers["atom_offsets"][:-1], centers["atom_offsets"][1:]
        )
    ]
    in_first = _whole_selection(members, first)
    in_second = None if second is None else _whole_selection(members, second)
    active = (
        in_first
        if selection_mode == "internal"
        else np.ones(len(members), dtype=bool)
        if selection_mode == "incident"
        else in_first | in_second
    )
    universe = (
        np.unique(np.concatenate([members[i] for i in np.flatnonzero(active)]))
        if active.any()
        else np.empty(0, dtype=np.int64)
    )
    scope_first = np.intersect1d(first, universe)
    scope_second = None if second is None else np.intersect1d(second, universe)
    charges = np.asarray(puw.get_value(centers["charges"], to_unit="e"))

    positive = np.flatnonzero(active & (charges > 0))
    negative = np.flatnonzero(active & (charges < 0))
    metadata = dict(
        n_atoms=n_atoms,
        n_structures=n_structures,
        evaluated_structure_indices=frames,
        method=_CALLER,
        software={"molsysmt": __version__},
        measure_units={
            "distance": "nm",
            "positive_charge": "e",
            "negative_charge": "e",
        },
        parameters={
            "method": method,
            "distance_threshold": {"value": threshold, "unit": "nm"},
            "distance_comparison": "less_than_or_equal",
            "cutoff_roundoff": "one_float64_ulp",
            "charge_source": centers["charge_source"],
            "participant_definition": centers["definition"],
            "recognition_rule_version": centers["rule_version"],
            "chemical_state_index": centers["chemical_state_index"],
            "charge_evidence": centers["evidence"],
            "pbc": pbc,
            "image_policy": "whole_participants_anchor_relative_mic",
            "pbc_policy": "mic_when_box_available",
            "recognition_scope": "full_source_chemical_state",
            "execution": "eager",
            "intramolecular": "included",
            "exclude_direct_covalent": True,
        },
        evaluation_mode=selection_mode,
        evaluation_atom_indices=scope_first,
        evaluation_atom_indices_b=scope_second,
        evaluation_universe_indices=universe,
    )
    searches = _search_sets(positive, negative, in_first, in_second, selection_mode)
    if len(frames) and searches:
        coordinates = get(
            molecular_system,
            selection=universe,
            structure_indices=frames,
            coordinates=True,
        )
        if coordinates is None:
            raise StructuralInconsistencyError(
                reason="Coordinates are required to evaluate nonempty center pairs.",
                caller=_CALLER,
            )
        coordinates = np.asarray(
            puw.get_value(coordinates, to_unit="nm"), dtype=np.float64
        )
        boxes = (
            get(molecular_system, structure_indices=frames, box=True) if pbc else None
        )
        boxes = (
            None
            if boxes is None
            else np.asarray(puw.get_value(boxes, to_unit="nm"), dtype=np.float64)
        )
        if (
            coordinates.shape != (len(frames), len(universe), 3)
            or not np.isfinite(coordinates).all()
        ):
            raise StructuralInconsistencyError(
                reason="Finite coordinates are required for every evaluated center.",
                caller=_CALLER,
            )
        if boxes is not None and (
            boxes.shape != (len(frames), 3, 3)
            or not np.isfinite(boxes).all()
            or np.any(np.abs(np.linalg.det(boxes)) < 1e-12)
        ):
            raise StructuralInconsistencyError(
                reason="Periodic boxes must be finite and nonsingular.", caller=_CALLER
            )
        topology = convert(molecular_system, to_form="molsysmt.Topology")
        state = topology._chemical_states[centers["chemical_state_index"]]
        covalent = (
            state.bonds.loc[state.bonds["bond_type"] == "covalent"]
            if len(state.bonds)
            else state.bonds
        )
        atom_centers = np.full(n_atoms, -1, dtype=np.int64)
        for index, atoms in enumerate(members):
            atom_centers[atoms] = index
        excluded = set()
        for a, b in covalent[["atom1_index", "atom2_index"]].to_numpy(dtype=np.int64):
            ca, cb = atom_centers[a], atom_centers[b]
            if ca >= 0 and cb >= 0 and ca != cb:
                excluded.add(tuple(sorted((int(ca), int(cb)))))
        result = _detect(
            coordinates,
            boxes,
            universe,
            frames,
            centers,
            members,
            positive,
            negative,
            in_first,
            in_second,
            selection_mode,
            threshold,
            excluded,
            metadata,
        )
    else:
        result = Interactions.from_records([], **metadata)
    return (
        result
        if output_type == "molsysmt.interactions"
        else convert(result, to_form="molsysmt.InteractionsDict")
    )


def _whole_selection(members, selected):
    selected = set(selected.tolist())
    result = np.zeros(len(members), dtype=bool)
    for index, atoms in enumerate(members):
        overlap = selected.intersection(atoms.tolist())
        if overlap and len(overlap) != len(atoms):
            raise ArgumentError(
                "selection",
                caller=_CALLER,
                message="The selection cuts a compound charge center.",
            )
        result[index] = bool(overlap)
    return result


def _search_sets(positive, negative, in_first, in_second, mode):
    """Plan disjoint oriented searches without generating unrelated center pairs."""
    if mode == "internal":
        pairs = [(positive, negative)]
    elif mode == "incident":
        pairs = [
            (positive[in_first[positive]], negative),
            (positive[~in_first[positive]], negative[in_first[negative]]),
        ]
    else:
        pairs = [
            (positive[in_first[positive]], negative[in_second[negative]]),
            (positive[in_second[positive]], negative[in_first[negative]]),
        ]
    return [(first, second) for first, second in pairs if len(first) and len(second)]


def _detect(
    coordinates,
    boxes,
    universe,
    frames,
    centers,
    members,
    positive,
    negative,
    in_first,
    in_second,
    mode,
    threshold,
    excluded,
    metadata,
):
    from molsysmt._private.sparse_membership import pack_membership
    from molsysmt.interactions.result import Interactions
    from molsysmt.pbc._whole_participants import require_whole_participants
    from molsysmt.structure._group_minimum_contacts import group_minimum_contacts

    geometry = centers["geometry_atom_indices"]
    offsets = centers["geometry_atom_offsets"]

    def reference_atoms(indices):
        groups = [geometry[offsets[i] : offsets[i + 1]] for i in indices]
        return np.concatenate(groups), np.repeat(
            indices, [len(group) for group in groups]
        )

    searches = []
    for first, second in _search_sets(positive, negative, in_first, in_second, mode):
        pos_atoms, pos_centers = reference_atoms(first)
        neg_atoms, neg_centers = reference_atoms(second)
        searches.append(
            (
                np.searchsorted(universe, pos_atoms),
                pos_centers,
                np.searchsorted(universe, neg_atoms),
                neg_centers,
            )
        )
    frame_columns, pair_columns, distance_columns, image_columns = [], [], [], []
    pair_dtype = np.dtype([("a", np.int64), ("b", np.int64)])
    excluded_rows = (
        np.asarray(sorted(excluded), dtype=np.int64)
        .reshape(-1, 2)
        .view(pair_dtype)
        .ravel()
    )
    active = np.concatenate((positive, negative))
    whole_atoms = np.concatenate([members[i] for i in active])
    whole_offsets = np.concatenate(([0], np.cumsum([len(members[i]) for i in active])))
    whole_positions = np.searchsorted(universe, whole_atoms)
    for local_frame, frame in enumerate(frames):
        xyz = coordinates[local_frame]
        box = None if boxes is None else boxes[local_frame]
        if box is not None:
            require_whole_participants(
                xyz, box, whole_offsets, whole_positions, _CALLER
            )
        observations = [
            group_minimum_contacts(
                xyz[pos_positions],
                pos_centers,
                xyz[neg_positions],
                neg_centers,
                threshold,
                box,
            )
            for pos_positions, pos_centers, neg_positions, neg_centers in searches
        ]
        pairs, distances, target_images = [
            np.concatenate(columns) for columns in zip(*observations)
        ]
        allowed = (
            np.ones(len(pairs), dtype=bool)
            if mode == "internal"
            else in_first[pairs[:, 0]] | in_first[pairs[:, 1]]
            if mode == "incident"
            else (
                (in_first[pairs[:, 0]] & in_second[pairs[:, 1]])
                | (in_second[pairs[:, 0]] & in_first[pairs[:, 1]])
            )
        )
        if excluded:
            canonical = (
                np.ascontiguousarray(np.sort(pairs, axis=1)).view(pair_dtype).ravel()
            )
            allowed &= ~np.isin(canonical, excluded_rows)
        pairs, distances, target_images = (
            pairs[allowed],
            distances[allowed],
            target_images[allowed],
        )
        if not len(pairs):
            continue
        images = np.zeros((len(pairs), 2, 3), dtype=np.int32)
        images[:, 1] = target_images
        frame_columns.append(np.full(len(pairs), frame, dtype=np.int64))
        pair_columns.append(pairs)
        distance_columns.append(distances)
        image_columns.append(images)
    if not pair_columns:
        return Interactions.from_records([], **metadata)
    relation_pairs, occurrence_relations = np.unique(
        np.concatenate(pair_columns),
        axis=0,
        return_inverse=True,
    )
    occurrence_frames = np.concatenate(frame_columns)
    order = np.lexsort((occurrence_relations, occurrence_frames))
    occurrence_relations, occurrence_frames = (
        occurrence_relations[order],
        occurrence_frames[order],
    )
    participant_groups = [members[i] for i in relation_pairs.ravel()]
    atoms, atom_offsets = pack_membership(participant_groups)
    charges = puw.get_value(centers["charges"], to_unit="e")
    return Interactions(
        relation_types=["ionic_contact"] * len(relation_pairs),
        relation_participant_offsets=np.arange(len(relation_pairs) + 1) * 2,
        participant_roles=[
            role for _ in relation_pairs for role in ("positive", "negative")
        ],
        participant_atom_offsets=atom_offsets,
        participant_atoms=atoms,
        occurrence_structures=occurrence_frames,
        occurrence_relations=occurrence_relations,
        occurrence_evidence=np.zeros(len(occurrence_relations), dtype=np.int32),
        evidence_labels=["formal_charge_geometric_proximity"],
        measurements={
            "distance": np.concatenate(distance_columns)[order],
            "positive_charge": charges[relation_pairs[occurrence_relations, 0]],
            "negative_charge": charges[relation_pairs[occurrence_relations, 1]],
        },
        occurrence_image_offsets=None
        if boxes is None
        else np.arange(len(order) + 1) * 2,
        image_vectors=None
        if boxes is None
        else np.concatenate(image_columns)[order].reshape(-1, 3),
        **metadata,
    )
