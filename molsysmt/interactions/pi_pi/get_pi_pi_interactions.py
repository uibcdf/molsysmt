"""Public boundary for declared-aromatic ring geometry observations."""

import numpy as np
from depdigest import dep_digest
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.interaction_attribution import attributed
from molsysmt._private.smonitor import (
    ArgumentError,
    StructuralInconsistencyError,
    UnsupportedHeavyOperationError,
)
from molsysmt._private.sparse_membership import (
    connected_group_pairs,
    whole_group_selection,
)
from molsysmt._private.variables import is_all

_CALLER = "molsysmt.interactions.pi_pi.get_pi_pi_interactions"


@signal(tags=["api", "interactions"])
@arg_digest()
@dep_digest("rdkit", when={"method": "prolif"})
@dep_digest("rdkit", when={"method": "plane_angle_intersection", "profile": None})
@dep_digest("rdkit", when={"method": "plane_angle_intersection", "profile": "smarts_5_6"})
@attributed("pi_pi")
def get_pi_pi_interactions(
    molecular_system, distance_threshold=None, angle_threshold=None, offset_threshold=None,
    planarity_threshold=None, selection="all", selection_2=None, structure_indices="all",
    chemical_state="reference", method="centroid_angle_offset",
    selection_mode="internal", pbc=True, assume_complete_connectivity=False,
    output_type="molsysmt.Interactions", syntax="MolSysMT", skip_digestion=False,
    *, geometry="both", max_cyclic_block_size=256, max_matches=100000, heavy_mode="auto", profile=None,
):
    """Detecting aromatic ring geometries with explicit attributed criteria.

    Choose ProLIF, Mol*/MDTraj geometric profiles or the separate MolSysMT
    proposal. Reference recognition and plane construction remain explicit.
    Geometric cutoffs define candidates;
    the result does not establish attraction, binding energy or a chemical bond.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form providing coordinates and explicit selected-state
        atom/bond aromatic flags and complete covalent connectivity.
    distance_threshold : quantity, str, or None, default=None
        Finite positive centroid-distance cutoff with length units. Required
        for the custom method. None uses 0.55 nm for Mol* or separate 0.55/0.65 nm
        face/edge limits for ProLIF and MDTraj. An explicit value overrides both
        limits for those profiles.
    angle_threshold : quantity, str, or None, default=None
        Custom/Mol* maximum deviation from parallel or perpendicular planes, with angular
        units. Must be nonnegative and strictly below 45 degrees, keeping the
        two geometry classes disjoint. Mol* defaults to 30 degrees. Leave None
        for ProLIF/MDTraj, which use their named angular intervals. Internally
        evaluated in radians.
    offset_threshold : quantity, str, or None, default=None
        Finite nonnegative lateral offset cutoff with length units. Custom parallel
        geometries must satisfy both planes' offsets; edge-to-face geometries
        must satisfy at least one. Mol* defaults to 0.2 nm and accepts either
        offset for both classes. Leave None for ProLIF/MDTraj, which use angular
        and plane-intersection criteria instead.
    planarity_threshold : quantity, str, or None, default=None
        Custom method's required finite nonnegative maximum orthogonal atom deviation from each ring's
        fitted plane, with length units. Warped rings exceeding it are excluded.
        Zero requires numerically exact planarity; no absolute tolerance is added.
        Leave None for reference profiles, which do not filter planarity.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection. Include every atom of any intersected aromatic ring,
        including adjacent fused rings sharing selected atoms.
    selection_2 : str, list, tuple, numpy.ndarray, or None, default=None
        Disjoint second atom selection, required only for selection_mode='between'.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to evaluate. Repeated indices are evaluated
        once in sorted order; evaluated frames without observations stay explicit.
    chemical_state : {'reference', 'structure'}, int, or None, default='reference'
        State supplying the chemistry. Structure-assigned states must resolve
        to one state across the requested frames.
    method : str, default='centroid_angle_offset'
        centroid_angle_offset or plane_angle_intersection. Profiles distinguish
        the proposal and adapted reference definitions. Historical prolif,
        molstar_geometry and mdtraj_geometry selectors remain exact aliases;
        geometric adaptations do not reproduce complete feature pipelines.
    selection_mode : {'internal', 'incident', 'between'}, default='internal'
        Search within selection, from selection to every eligible system ring,
        or between selection and selection_2, respectively.
    pbc : bool, default=True
        Use MIC when a box exists. Participants must already be whole in the
        anchor-relative image. Split rings fail; coordinates are not unwrapped.
    assume_complete_connectivity : bool, default=False
        Explicitly assume supplied connectivity complete when stored metadata
        is insufficient. Record the assumption without modifying the source.
    output_type : {'molsysmt.Interactions', 'molsysmt.InteractionsDict'}, default='molsysmt.Interactions'
        Sparse analysis object or its typed, versioned serialization dictionary.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate selection and selection_2.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    geometry : {'parallel', 'edge_to_face', 'both'}, default='both'
        Keyword-only choice of accepted geometric classes.
    max_cyclic_block_size : int, default=256
        Keyword-only ring-basis limit per aromatic cyclic biconnected block.
        Increasing it can substantially increase recognition time and memory.
    max_matches : int, default=100000
        Keyword-only bound per ProLIF ring SMARTS query before selection. An
        exceeded limit raises rather than returning a truncated participant set.
    heavy_mode : {'auto', 'force', 'off'}, default='auto'
        Keyword-only execution policy. Streaming follows the form's declared
        coordinate support. Other supported forms use their ordinary getters
        eagerly when the selected working estimate fits the budget.

    profile : str or None, default=None
        Keyword-only profile. centroid_angle_offset defaults to least_squares;
        three_atom_plane selects the adapted Mol* geometry. For
        plane_angle_intersection, smarts_5_6 is the default ProLIF profile and
        aromatic_cycles uses the adapted MDTraj geometry on declared rings.

    Returns
    -------
    molsysmt.Interactions or molsysmt.InteractionsDict
        Sparse pi_pi relations with ring_a/ring_b whole-ring participants,
        ordered by their source memberships. Occurrences retain centroid
        distance, acute plane angle, both lateral offsets, and each ring's
        RMS/maximum deviation (nm and radians). Evidence distinguishes parallel
        and edge-to-face observations. Images shift ring_b relative to ring_a
        using row box vectors. Source axes, evaluated frames, examined aromatic
        atom scope, chemistry evidence, parameters and producer versions are
        explicit. Reference profiles also retain both normal/centroid acute
        angles and the tested intersection distance (nm); the latter is NaN
        where the intersection test was not applied. Empty columns have (0,).

    Raises
    ------
    ArgumentError
        If cutoffs, selections, method, geometry or structure indices are invalid.
    StructuralInconsistencyError
        If chemistry is missing/contradictory, coordinates or boxes are invalid,
        or a ring does not define a unique plane.
    NotImplementedMethodError
        If a periodic ring requires internal image reconstruction.
    UnsupportedHeavyOperationError
        If the form cannot supply required streaming, or one coordinate block
        cannot fit its allotted numerical working estimate.
    MemoryBudgetExceededError
        If source axes, candidates or the resident sparse-result estimate
        exceed their configured RAM allocation. No partial result is returned.

    Notes
    -----
    Canonical method/profile identities and their definition version accompany
    the effective cutoffs and pinned reference implementation. The detached
    parameters['attribution'] bibliography survives typed and H5MSM storage;
    optional Ackredit tracking credits the application's current session.

    For the custom method, let d be the observed MIC centroid displacement and n_a/n_b the unit
    normals. The acute plane angle is atan2(norm(cross(n_a,n_b)),
    abs(dot(n_a,n_b))). Each offset is norm(d-dot(d,n)*n). Parallel accepts
    angle <= angle_threshold and max(offset_a,offset_b) <= offset_threshold.
    Edge-to-face accepts pi/2-angle <= angle_threshold and
    min(offset_a,offset_b) <= offset_threshold. Both require a positive centroid
    distance within distance_threshold and both maximum deviations within
    planarity_threshold. Inclusive comparisons allow one float64 ULP, without
    an additional absolute tolerance. Angular roundoff is capped strictly below
    pi/4 so the two classes remain disjoint even near the numerical boundary.

    The custom method excludes self, overlapping/fused and directly covalently linked rings.
    Other intramolecular contacts are included; dative links do not exclude a
    pair. Reference profiles add no overlap/covalent exclusion; undefined normals
    and zero displacements are skipped explicitly. There is no energy, residue
    or component filter. A minimum cycle
    basis is not all cycles or SymmSSSR. Chemistry is examined across the full
    source; observation coverage contains only eligible aromatic atom scopes.
    Every selected frame is searched, without first-frame candidate pruning.
    The calculation neither attaches an analysis nor modifies its source.

    ProLIF uses its original five/six-member ring SMARTS and normals formed
    from centroid-to-first-two matched atoms. MDTraj geometry uses the same
    normal construction with supplied basis-member order. Face accepts distance
    <=0.55 nm, acute plane angle <=35 degrees and either normal/centroid angle
    <=33 degrees. Edge accepts distance <=0.65 nm, plane angle >=50 degrees,
    either normal/centroid angle <=30 degrees and the projected intersection
    within 0.15 nm of either centroid. The original core projects ring_a's
    centroid on the intersection line: this is role-dependent. Canonical source
    memberships fix ring_a/ring_b; atom reordering can therefore affect this
    criterion. It is not silently symmetrized. ProLIF checks exact determinant
    singularity; MDTraj uses NumPy isclose, without reproducing its random
    replacement of singular matrices. No first-frame pruning is performed.

    Mol* geometry uses the first three basis atoms for its triangle normal,
    distance <=0.55 nm, deviation <=30 degrees from parallel/perpendicular,
    and min(offset_a,offset_b)<=0.2 nm for both classes. Its valence-based feature
    recognition and contact refinement are not reproduced. Reference comparisons
    add no ULP allowance. Computation uses float64; MDTraj's float32 coordinates
    can yield different decisions exactly at thresholds. Coherent whole-ring
    MIC geometry is a MolSysMT extension;
    MDTraj's original pi routine wraps centroid distances but uses raw centroid
    vectors for angles/intersections. Producer versions and pinned references
    are separate metadata. No reference profile establishes attractive energy.

    H5MSM 0.5 index selections load chemistry/association metadata once and
    projected coordinate blocks, without saved analyses. Rich file selections
    use the eager route only within the full source-coordinate estimate;
    forced streaming requires index selections or 'all'. Coordinates/plane work reserve one quarter of
    configure.max_ram_usage, each bounded candidate search one eighth, and
    sparse accumulation/packing one half. The complete sparse result remains
    resident. Estimates bound numeric work, not caller-owned arrays, chemistry
    tables, Python overhead or process RSS. No incremental result writer is
    provided. No new Rust dependency is required: plane fitting and spatial
    search reuse bundled kernels; candidate geometry is vectorized NumPy.

    See Also
    --------
    molsysmt.physchem.get_aromatic_rings
        Identifying declared aromatic participants.
    molsysmt.structure.get_least_squares_plane
        Fitting general group planes without assuming aromatic chemistry.
    molsysmt.Interactions.query
        Filtering observed occurrences by atoms and structures.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt.interactions.pi_pi.get_pi_pi_interactions import get_pi_pi_interactions
    >>> from molsysmt.native import Topology
    >>> topology = Topology(n_atoms=1)
    >>> msm.set(topology, element='atom', atom_is_aromatic=[False])
    >>> molsys = msm.convert(topology, to_form='molsysmt.MolSys')
    >>> result = get_pi_pi_interactions(molsys, '0.6 nm', '30 degrees',
    ...     '0.2 nm', '0.02 nm', assume_complete_connectivity=True)
    >>> result.n_interactions, result.measure_units['plane_angle']
    (0, 'radians')

    .. admonition:: User guide

       See :ref:`Getting pi-pi interactions <Tutorial_Get_pi_pi_interactions>`.

    .. versionadded:: 1.0.0
    """
    from copy import copy

    from molsysmt import configure
    from molsysmt._private.interaction_methods import resolve_method

    method = resolve_method("pi_pi", method, profile, caller=_CALLER)["implementation"]
    from molsysmt._private.execution.projected_geometry import (
        execute_projected_geometry,
    )
    from molsysmt._private.execution.sparse_accumulator import SparseColumnAccumulator
    from molsysmt._private.h5msm import modular_h5msm_dimensions
    from molsysmt.basic import convert, get, select
    from molsysmt.interactions.pi_pi._reducer import _PiPiReducer
    from molsysmt.interactions.result import Interactions
    from molsysmt.native import MolSys
    from molsysmt.physchem.get_aromatic_rings import get_aromatic_rings
    from molsysmt.topology._rings import ring_context

    thresholds = {}
    reference_thresholds = {"face_distance": .55, "edge_distance": .65}
    if method == "centroid_angle_offset":
        if any(value is None for value in (distance_threshold, angle_threshold, offset_threshold, planarity_threshold)):
            raise ArgumentError("method", caller=_CALLER, message="The custom method requires all four explicit cutoffs.")
    elif method == "molstar_geometry":
        if planarity_threshold is not None:
            raise ArgumentError("planarity_threshold", caller=_CALLER, message="Mol* geometry has no planarity filter.")
        distance_threshold = puw.quantity(.55, "nm") if distance_threshold is None else distance_threshold
        angle_threshold = puw.quantity(30, "degrees") if angle_threshold is None else angle_threshold
        offset_threshold = puw.quantity(.2, "nm") if offset_threshold is None else offset_threshold
    else:
        if any(value is not None for value in (angle_threshold, offset_threshold, planarity_threshold)):
            raise ArgumentError("method", caller=_CALLER, message="ProLIF and MDTraj profiles use their named default angular/intersection criteria; leave angle, offset and planarity None.")
    for name, value, unit, positive in (
        ("distance_threshold", distance_threshold, "nm", True),
        ("angle_threshold", angle_threshold, "radians", False),
        ("offset_threshold", offset_threshold, "nm", False),
        ("planarity_threshold", planarity_threshold, "nm", False),
    ):
        if value is None:
            continue
        number = np.asarray(puw.get_value(value, to_unit=unit))
        if number.shape != () or not np.isfinite(number) or number < 0 or (positive and number == 0):
            raise ArgumentError(name, value=value, caller=_CALLER, message="Use a finite scalar cutoff with the required units and range.")
        thresholds[name] = float(number)
    if "angle_threshold" in thresholds and thresholds["angle_threshold"] >= np.pi / 4:
        raise ArgumentError("angle_threshold", caller=_CALLER, message="Angular deviation must be strictly below 45 degrees.")
    if method in {"prolif", "mdtraj_geometry"}:
        if distance_threshold is not None:
            reference_thresholds = dict.fromkeys(reference_thresholds, thresholds["distance_threshold"])
        thresholds.update(reference_thresholds)
        thresholds["distance_threshold"] = max(reference_thresholds.values())
    if (selection_mode == "between") != (selection_2 is not None):
        raise ArgumentError("selection_2", caller=_CALLER, message="Supply a second selection only for between searches.")

    dimensions = modular_h5msm_dimensions(molecular_system)
    modular = dimensions is not None
    if dimensions is None:
        dimensions = get(molecular_system, n_atoms=True, n_structures=True)
    if any(size is None for size in dimensions):
        raise StructuralInconsistencyError(reason="Declared atom and structure axes are required for pi-pi geometry.", caller=_CALLER)
    n_atoms, n_structures = map(int, dimensions)
    frames = np.arange(n_structures, dtype=np.int64) if is_all(structure_indices) else np.unique(structure_indices)
    frames = frames.astype(np.int64)
    if np.any((frames < 0) | (frames >= n_structures)):
        raise ArgumentError("structure_indices", value=structure_indices, caller=_CALLER)
    fixed_bytes = 8 * (2 * n_atoms + 4 * n_structures)
    SparseColumnAccumulator({}, budget_bytes=configure.max_ram_usage // 2, fixed_bytes=fixed_bytes).check_budget()
    coordinate_source = molecular_system
    index_selections = all(value is None or not isinstance(value, str) or is_all(value)
                           for value in (selection, selection_2))
    if modular and not index_selections:
        from molsysmt._private.execution.memory_policy import estimate_footprint
        from molsysmt._private.h5msm import maybe_read_modular_h5msm

        if heavy_mode == "force" or estimate_footprint(n_atoms, n_structures) > configure.max_ram_usage:
            raise UnsupportedHeavyOperationError(operation=_CALLER, form="H5MSM rich selections",
                                                 reason="Use atom-index selections or all for bounded file calculations; rich selection requires eager source materialization within budget.")
        molecular_system = maybe_read_modular_h5msm(molecular_system)
        coordinate_source = molecular_system
    source, states, _, state_index, _, covalent, selection_frames = ring_context(
        molecular_system, chemical_state, frames, assume_complete_connectivity, _CALLER,
    )
    if method == "prolif":
        from molsysmt.physchem._prolif import PROLIF_PATTERNS, PROLIF_REFERENCE
        from molsysmt.topology import get_substructure_matches

        matches = get_substructure_matches(source, PROLIF_PATTERNS[1:], chemical_state=state_index,
                                          assume_complete_connectivity=assume_complete_connectivity,
                                          max_matches=max_matches)
        members = sorted([row for matrix in matches["matches"] for row in matrix],
                         key=lambda row: tuple(sorted(row)))
        software = matches["software"]
        recognition = dict(participant_definition="prolif_default_5_6_membered_ring_smarts",
                           smarts_patterns=list(PROLIF_PATTERNS[1:]), max_matches=max_matches,
                           aromatic_evidence=matches["evidence"], method_reference=PROLIF_REFERENCE,
                           plane_method="cross_of_centroid_to_first_two_smarts_atoms",
                           adaptation="single_source_sparse_scopes_coherent_mic_no_full_fingerprint")
    else:
        rings = get_aromatic_rings(states, chemical_state=state_index,
                                  assume_complete_connectivity=assume_complete_connectivity,
                                  max_cyclic_block_size=max_cyclic_block_size)
        members = [rings["atom_indices"][a:b] for a, b in zip(rings["atom_offsets"][:-1], rings["atom_offsets"][1:])]
        software = rings["software"]
        recognition = dict(participant_definition=rings["definition"], recognition_rule_version=rings["rule_version"],
                           ring_method=rings["method"], aromatic_evidence=rings["evidence"],
                           plane_method="unweighted_orthogonal_least_squares", method_reference=None)
        if method == "molstar_geometry":
            from molsysmt._private.scientific_references import MOLSTAR_REFERENCE
            recognition.update(method_reference=MOLSTAR_REFERENCE,
                               plane_method="cross_of_first_three_basis_member_atoms",
                               adaptation="geometry_only_declared_molsysmt_ring_basis_no_molstar_valence_or_refinement")
        elif method == "mdtraj_geometry":
            from molsysmt._private.scientific_references import MDTRAJ_REFERENCE
            recognition.update(method_reference=MDTRAJ_REFERENCE,
                               plane_method="cross_of_centroid_to_first_two_basis_member_atoms",
                               adaptation="supplied_declared_molsysmt_ring_basis_no_first_frame_pruning")
    if index_selections:
        selection_source = copy(states)
        selection_source._reference_index = state_index
        selection_state = "reference"
    else:
        selection_source = source if isinstance(source, MolSys) else convert(source, to_form="molsysmt.MolSys")
        selection_state = state_index
    first = np.unique(select(selection_source, selection=selection, structure_indices=selection_frames,
                             chemical_state=selection_state, syntax=syntax)).astype(np.int64)
    second = None if selection_2 is None else np.unique(select(
        selection_source, selection=selection_2, structure_indices=selection_frames,
        chemical_state=selection_state, syntax=syntax)).astype(np.int64)
    if second is not None and np.intersect1d(first, second).size:
        raise ArgumentError("selection_2", caller=_CALLER, message="Between selections must be disjoint.")
    in_first = whole_group_selection(members, first, caller=_CALLER)
    in_second = None if second is None else whole_group_selection(members, second, caller=_CALLER, argument="selection_2")
    active = in_first if selection_mode == "internal" else np.ones(len(members), dtype=bool) if selection_mode == "incident" else in_first | in_second
    active_indices = np.flatnonzero(active)
    selected = np.flatnonzero(in_first)
    if selection_mode == "between":
        searches = [(selected, np.flatnonzero(in_second), False)]
    else:
        searches = [(selected, selected, True)]
        if selection_mode == "incident":
            searches.append((selected, np.flatnonzero(~in_first), False))
    searches = [(a, b, triangular) for a, b, triangular in searches
                if len(a) and len(b) and (not triangular or len(a) > 1)]
    universe = np.unique(np.concatenate([members[i] for i in active_indices])) if len(active_indices) else np.empty(0, dtype=np.int64)
    metadata = dict(
        n_atoms=n_atoms, n_structures=n_structures, evaluated_structure_indices=frames,
        method=_CALLER, software=software,
        measure_units={"distance": "nm", "plane_angle": "radians", "offset_a": "nm", "offset_b": "nm",
                       "rms_deviation_a": "nm", "rms_deviation_b": "nm", "max_deviation_a": "nm", "max_deviation_b": "nm",
                       **({"normal_angle_a": "radians", "normal_angle_b": "radians", "intersection_distance": "nm"}
                          if method != "centroid_angle_offset" else {})},
        parameters={
            "method": method, "geometry": geometry, "geometry_rule_version": "centroid_angle_offset@1" if method == "centroid_angle_offset" else method + "_pi_pi@1",
            **{name: {"value": value, "unit": "radians" if name == "angle_threshold" else "nm"}
               for name, value in thresholds.items()},
            "cutoff_roundoff": "one_float64_ulp", "distance_comparison": "positive_and_less_than_or_equal",
            "angular_roundoff_cap": "strictly_below_pi_over_4",
            "parallel_offsets": "both", "edge_to_face_offsets": "at_least_one",
            "max_cyclic_block_size": max_cyclic_block_size, "recognition_scope": "full_source_chemical_state",
            "chemical_state_index": state_index, "pbc": pbc, **recognition,
            "canonical_roles": "ring_a_has_lexicographically_smaller_source_membership",
            "intersection_projection": "ring_a_centroid" if method in {"prolif", "mdtraj_geometry"} else None,
            **({"face_plane_angle_degrees": [0, 35], "edge_plane_angle_degrees": [50, 90],
                "face_normal_angle_degrees": [0, 33], "edge_normal_angle_degrees": [0, 30],
                "intersection_radius": {"value": .15, "unit": "nm"},
                "normal_angle_policy": "at_least_one", "near_singular_intersection": method == "mdtraj_geometry"}
               if method in {"prolif", "mdtraj_geometry"} else {}),
            "image_policy": "whole_participants_anchor_relative_mic", "pbc_policy": "mic_when_box_available",
            "exclude_overlap": method == "centroid_angle_offset", "exclude_direct_covalent": method == "centroid_angle_offset", "intramolecular": "included",
            "memory_policy": "numeric_working_estimates@1",
        },
        evaluation_mode=selection_mode, evaluation_atom_indices=np.intersect1d(first, universe),
        evaluation_atom_indices_b=None if second is None else np.intersect1d(second, universe),
        evaluation_universe_indices=universe,
    )
    if method != "centroid_angle_offset":
        metadata["parameters"].update(cutoff_roundoff="none", angular_roundoff_cap=None,
                                      parallel_offsets="at_least_one" if method == "molstar_geometry" else "not_used",
                                      edge_to_face_offsets="at_least_one" if method == "molstar_geometry" else "not_used")
    if not len(frames) or not searches:
        metadata["parameters"].update(execution="none", execution_chunks=0)
        result = Interactions.from_records([], **metadata)
    else:
        per_frame = 4 * 24 * len(universe) + 256 * len(active_indices) + 192 * max(len(members[i]) for i in active_indices) + 2048 + (288 if pbc else 0)
        reducer = _PiPiReducer(members=members, active=active_indices, universe=universe, searches=searches,
                              excluded=connected_group_pairs(members, covalent) if method == "centroid_angle_offset" else set(), thresholds=thresholds,
                              method=method,
                              geometry=geometry, metadata=metadata, budget_bytes=configure.max_ram_usage)
        result = execute_projected_geometry(coordinate_source, universe=universe, frames=frames,
                                            reducer=reducer, per_frame_bytes=per_frame,
                                            pbc=pbc, heavy_mode=heavy_mode, caller=_CALLER)
    return result if output_type == "molsysmt.interactions" else convert(result, to_form="molsysmt.InteractionsDict")
