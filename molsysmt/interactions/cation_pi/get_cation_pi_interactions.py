"""Public boundary for formal-cation/declared-aromatic observations."""

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

_CALLER = "molsysmt.interactions.cation_pi.get_cation_pi_interactions"


@signal(tags=["api", "interactions"])
@arg_digest()
@dep_digest("rdkit", when={"method": "prolif"})
@dep_digest("rdkit", when={"method": "centroid_distance_angle"})
@attributed("cation_pi")
def get_cation_pi_interactions(
    molecular_system, distance_threshold=None, angle_threshold=None, offset_threshold=None,
    planarity_threshold=None, selection="all", selection_2=None, structure_indices="all",
    chemical_state="reference", method="centroid_distance_angle",
    selection_mode="internal", pbc=True, assume_complete_connectivity=False,
    output_type="molsysmt.Interactions", syntax="MolSysMT", skip_digestion=False,
    *, max_cyclic_block_size=256, max_matches=100000, heavy_mode="auto", profile=None,
):
    """Detecting cation-pi geometries using an attributed or experimental method.

    The default reproduces ProLIF 2.2.2's CationPi SMARTS, centroid/normal
    construction and distance/angle acceptance. The separately named
    centroid_angle_offset method is a MolSysMT proposal, not a published method.
    Both return geometric evidence, without establishing attractive energy.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying coordinates, elements, complete declared
        selected-state connectivity, bond orders, formal charges and explicit
        aromatic atom/bond flags. A chemical-only domain has no element inventory.
    distance_threshold : quantity, str, or None, default=None
        Finite positive cation-point/ring-centroid cutoff with length units.
        None uses ProLIF's 0.45 nm or Mol* geometry's 0.60 nm; the custom
        method requires an explicit value.
    angle_threshold : quantity, str, or None, default=None
        Acute displacement/normal angle cutoff with angular units. ProLIF
        accepts a scalar maximum (minimum zero) or a quantity with two values
        [minimum, maximum] within 0 to 90 degrees; None uses [0, 30] degrees.
        The custom method requires an explicit nonnegative scalar below 90
        degrees. Leave None for Mol* geometry, which has no angular filter.
        Calculations and stored parameters use radians.
    offset_threshold : quantity, str, or None, default=None
        Custom method's finite nonnegative lateral displacement cutoff, with
        length units. Required for the custom method; must be None for ProLIF,
        which applies no offset filter. Mol* geometry defaults to 0.20 nm.
    planarity_threshold : quantity, str, or None, default=None
        Custom method's finite nonnegative maximum ring-plane deviation cutoff,
        with length units. Required for the custom method; must be None for
        ProLIF/Mol* geometry, which apply no planarity filter. Zero adds no absolute tolerance.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Include every atom of any intersected eligible participant. ProLIF
        cations are singleton matched atoms; custom cations may be compound.
        Fused rings sharing atoms can require extending a selection.
    selection_2 : str, list, tuple, numpy.ndarray, or None, default=None
        Disjoint second selection, required only for selection_mode='between'.
        Either selection may contain cations, rings or both.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Zero-based structure indices. Repeated indices are evaluated once in
        sorted order; evaluated structures without candidates remain explicit.
    chemical_state : {'reference', 'structure'}, int, or None, default='reference'
        Selected chemistry. Structure assignments must resolve one state across
        the requested structures; no protonation or parameterization is inferred.
    method : str, default='centroid_distance_angle'
        centroid_distance_angle, centroid_distance_offset, or the separately
        identified centroid_angle_offset proposal. Historical prolif and
        molstar_geometry selectors remain exact compatibility aliases.
        Reference implementations and adaptations are recorded separately.
    selection_mode : {'internal', 'incident', 'between'}, default='internal'
        Search within selection, from selection to every eligible system
        participant, or between selection and selection_2, respectively.
    pbc : bool, default=True
        Explicit MolSysMT extension: use MIC when a box exists. Participants
        must already be whole in their anchor-relative image; split groups fail.
    assume_complete_connectivity : bool, default=False
        Record an explicit completeness assumption without modifying the source.
    output_type : {'molsysmt.Interactions', 'molsysmt.InteractionsDict'}, default='molsysmt.Interactions'
        Sparse analysis object or its typed, versioned serialization dictionary.
    syntax : str, default='MolSysMT'
        Syntax used to evaluate selection and selection_2.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    max_cyclic_block_size : int, default=256
        Keyword-only aromatic basis limit for the custom method. ProLIF uses
        its original SMARTS ring recognition and does not use this limit.
    max_matches : int, default=100000
        Keyword-only bound per SMARTS query for ProLIF. Exceeding it raises
        instead of silently truncating. The custom method does not use this limit.
    heavy_mode : {'auto', 'force', 'off'}, default='auto'
        Keyword-only execution policy. Streaming requires the form's declared
        coordinate route; other supported forms use bounded eager getters.

    profile : str or None, default=None
        Keyword-only profile. centroid_distance_angle uses smarts_5_6;
        centroid_distance_offset uses three_atom_plane; centroid_angle_offset
        uses least_squares. These preserve the distinct recognition, normal
        construction and comparisons of each referenced definition.

    Returns
    -------
    molsysmt.Interactions or molsysmt.InteractionsDict
        Sparse cation_pi relations with cation/ring roles and complete source
        memberships. ProLIF rings preserve SMARTS atom order for reconstructing
        the normal; this is not sorted membership order. Measures include
        distance, acute normal angle, lateral offset, absolute height, ring
        RMS/maximum deviation and cation charge (nm, radians, elementary charge).
        For ProLIF, cation_charge is the matched atom's stored formal charge:
        a neutral nitrogen matched by the resonance pattern can have zero.
        For the custom method, it is the whole center's positive net charge.
        For ProLIF, oriented_normal_angle also preserves the original reported
        angle in [0, pi], before acute folding for acceptance.
        ProLIF deviations describe its centroid-edge plane, not a least-squares
        fit. They are diagnostic and do not filter its observations.
        Images shift the ring relative to the cation using row box vectors.
        Empty frames, eligible atom scope, producer version, original method
        reference and parameters are explicit; empty measure columns have (0,).

    Raises
    ------
    ArgumentError
        If cutoffs, method, selections or structure indices are invalid.
    StructuralInconsistencyError
        If declared chemistry is missing/contradictory, coordinates/boxes are
        invalid or a custom-method ring fails to define a unique fitted plane.
    NotImplementedMethodError
        If a periodic participant requires internal image reconstruction.
    UnsupportedHeavyOperationError
        If SMARTS matches exceed their limit, required streaming is unavailable
        or one projected frame exceeds its numerical working estimate.
    MemoryBudgetExceededError
        If matching, axes, candidates or resident sparse output exceed their
        configured allocation. No partial analysis is returned.

    Notes
    -----
    Canonical method names describe the criterion. Profiles and pinned source
    references preserve the complete reproduced definition. The detached
    parameters['attribution'] bibliography survives typed and H5MSM storage,
    independently of optional Ackredit tracking in the application's session.

    ProLIF uses its original cation SMARTS, including amidine/guanidine
    resonance and opposite-charge exclusions, and aromatic 5/6-member ring
    SMARTS. The ring centroid is the arithmetic mean; its normal is the cross
    product of centroid-to-first and centroid-to-second matched atom vectors.
    Require distance <= cutoff and angle within the inclusive acute interval,
    without an extra ULP allowance. Undefined normals or zero displacements
    produce no angular candidates. No least-squares, offset, planarity,
    overlap or direct-covalent exclusion is added to this method.

    MolSysMT extends the calculation to a single source with explicit scopes,
    all requested frames, bounded coordinate/candidate execution and optional
    MIC. It does not reproduce ProLIF's residue-pair/ligand preprocessing or
    fingerprint aggregation. RDKit is an optional dependency required by
    ProLIF recognition; ProLIF itself is not a runtime dependency. Native
    recognition reuses the chemistry-aware RDKit converter without coordinates
    and requires sanitization to preserve declared charges and aromaticity.

    The custom method uses positive formal-charge centers and declared aromatic
    minimum-cycle-basis rings. Its cation point is the unweighted mean of ALL
    participant atoms, not an electrical center or the ionic distance-reference
    subset. Planes are unweighted least squares. For d=point-ring_centroid and
    unit n: height=abs(dot(d,n)), offset=norm(d-dot(d,n)*n), and
    angle=atan2(offset,height). Require positive distance, angle/offset and
    maximum ring deviation within their cutoffs. Inclusive comparisons allow
    one float64 ULP, capped below pi/2 for angles. Overlap and direct covalent
    links exclude a pair; other intramolecular candidates remain included.
    This experimental proposal has no established accuracy advantage; its
    comparison is tracked in uibcdf/molsysmt#271.

    molstar_geometry reproduces the charged.ts geometric tester using distance
    <=0.60 nm and lateral offset <=0.20 nm, with a normal from the first three
    basis member atoms. It adds no angle/planarity or covalent exclusion.
    Its participants are MolSysMT declared formal-charge centers and aromatic
    basis rings, not Mol*'s valence-model/residue feature discovery. Their
    centroid uses all participating atoms; Mol* can mark atoms that do not
    contribute to its feature centroid. This named profile therefore compares
    geometry on supplied features and does not claim full Mol* detector parity.
    Undefined triangles/zero displacements are skipped; whole-participant MIC
    is an explicit extension. The pinned source reference survives serialization.

    Coverage contains eligible participants, not every atom examined during
    full-state recognition. Results are never attached automatically. H5MSM
    index selections read chemistry once and projected coordinates without
    saved analyses; rich file selections require bounded eager materialization.
    Numeric coordinate/geometry work reserves one quarter of the RAM budget,
    candidate search one eighth, sparse accumulation/packing one half. Source
    arrays, chemistry, Python overhead and process RSS are outside these
    estimates. The sparse result remains resident. Plane/spatial kernels are
    reused; no new compiled backend or incremental writer is introduced.

    See Also
    --------
    molsysmt.topology.get_substructure_matches
        Matching original chemical SMARTS without silent truncation.
    molsysmt.physchem.get_charge_centers
        Identifying the custom method's formal-charge centers.
    molsysmt.physchem.get_aromatic_rings
        Identifying the custom method's declared ring basis.
    molsysmt.structure.get_least_squares_plane
        Fitting general group planes.
    molsysmt.Interactions.query
        Filtering sparse observations by atoms and structures.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import pyunitwizard as puw
    >>> from rdkit import Chem
    >>> molsys = msm.convert(Chem.MolFromSmiles('[Na+]'), to_form='molsysmt.MolSys')
    >>> molsys.structures.append(coordinates=puw.quantity([[[0., 0., 0.]]], 'nm'))
    >>> from molsysmt.interactions.cation_pi import get_cation_pi_interactions
    >>> result = get_cation_pi_interactions(
    ...     molsys, assume_complete_connectivity=True, pbc=False)
    >>> result.n_interactions, result.evaluated_structure_indices.tolist()
    (0, [0])

    .. admonition:: User guide

       See :ref:`Getting cation-pi interactions <Tutorial_Get_cation_pi_interactions>`.

    .. versionadded:: 1.0.0
    """
    from copy import copy

    from molsysmt import configure
    from molsysmt._private.interaction_methods import resolve_method

    method = resolve_method("cation_pi", method, profile, caller=_CALLER)["implementation"]
    from molsysmt._private.execution.projected_geometry import (
        execute_projected_geometry,
    )
    from molsysmt._private.execution.sparse_accumulator import SparseColumnAccumulator
    from molsysmt._private.h5msm import modular_h5msm_dimensions
    from molsysmt.basic import convert, get, select
    from molsysmt.interactions.cation_pi._reducer import _CationPiReducer
    from molsysmt.interactions.result import Interactions
    from molsysmt.native import MolSys, Topology
    from molsysmt.physchem.get_aromatic_rings import get_aromatic_rings
    from molsysmt.physchem.get_charge_centers import get_charge_centers
    from molsysmt.topology._rings import ring_context

    if method == "prolif":
        if offset_threshold is not None or planarity_threshold is not None:
            raise ArgumentError("offset_threshold", caller=_CALLER,
                                message="ProLIF has no offset or planarity cutoff; leave both None.")
        distance_threshold = puw.quantity(.45, "nm") if distance_threshold is None else distance_threshold
        angle_threshold = puw.quantity([0., 30.], "degrees") if angle_threshold is None else angle_threshold
    elif method == "molstar_geometry":
        if angle_threshold is not None or planarity_threshold is not None:
            raise ArgumentError("angle_threshold", caller=_CALLER, message="Mol* cation-pi geometry has no angle or planarity filter; leave both None.")
        distance_threshold = puw.quantity(.6, "nm") if distance_threshold is None else distance_threshold
        offset_threshold = puw.quantity(.2, "nm") if offset_threshold is None else offset_threshold
    elif any(value is None for value in (distance_threshold, angle_threshold, offset_threshold, planarity_threshold)):
        raise ArgumentError("method", caller=_CALLER,
                            message="The custom centroid_angle_offset method requires all four explicit cutoffs.")
    thresholds = {}
    for name, value, unit, positive in (
        ("distance_threshold", distance_threshold, "nm", True),
        ("angle_threshold", angle_threshold, "radians", False),
        ("offset_threshold", offset_threshold, "nm", False),
        ("planarity_threshold", planarity_threshold, "nm", False),
    ):
        if value is None:
            continue
        number = np.asarray(puw.get_value(value, to_unit=unit))
        if name == "angle_threshold" and method == "prolif":
            interval = np.array([0., float(number)]) if number.shape == () else number
            if interval.shape != (2,) or not np.isfinite(interval).all() or not 0 <= interval[0] <= interval[1] <= np.pi / 2:
                raise ArgumentError(name, value=value, caller=_CALLER, message="Use a scalar maximum or a two-angle interval within 0 to 90 degrees.")
            thresholds[name] = interval.tolist()
            continue
        if number.shape != () or not np.isfinite(number) or number < 0 or (positive and number == 0):
            raise ArgumentError(name, value=value, caller=_CALLER, message="Use a finite scalar cutoff with the required units and range.")
        thresholds[name] = float(number)
    if method == "centroid_angle_offset" and thresholds["angle_threshold"] >= np.pi / 2:
        raise ArgumentError("angle_threshold", caller=_CALLER, message="Angular deviation must be strictly below 90 degrees.")
    if (selection_mode == "between") != (selection_2 is not None):
        raise ArgumentError("selection_2", caller=_CALLER, message="Supply a second selection only for between searches.")

    dimensions = modular_h5msm_dimensions(molecular_system)
    modular = dimensions is not None
    if dimensions is None:
        dimensions = get(molecular_system, n_atoms=True, n_structures=True)
    if any(size is None for size in dimensions):
        raise StructuralInconsistencyError(reason="Declared atom and structure axes are required for cation-pi geometry.", caller=_CALLER)
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
    source, states, state, state_index, _, covalent, selection_frames = ring_context(
        molecular_system, chemical_state, frames, assume_complete_connectivity, _CALLER,
    )
    if method == "prolif":
        from molsysmt.physchem._prolif import (
            PROLIF_PATTERNS,
            PROLIF_REFERENCE,
        )
        from molsysmt.topology import get_substructure_matches

        features = get_substructure_matches(source, PROLIF_PATTERNS, chemical_state=state_index,
                                            assume_complete_connectivity=assume_complete_connectivity,
                                            max_matches=max_matches)
        center_members = list(features["matches"][0])
        ring_members = sorted([row for matrix in features["matches"][1:] for row in matrix],
                              key=lambda row: tuple(sorted(row)))
        charges = np.asarray([state.atom_attributes["formal_charge"].iloc[int(row[0])] for row in center_members], dtype=float)
        feature_parameters = dict(
            method_reference=PROLIF_REFERENCE, geometry_rule_version="prolif.CationPi@2.2.2",
            smarts_patterns=list(PROLIF_PATTERNS), max_matches=max_matches,
            cation_point="matched_reference_atom", charge_policy="prolif_cation_smarts_including_resonance",
            participant_definition="prolif_default_5_6_membered_ring_smarts",
            plane_method="cross_of_centroid_to_first_two_smarts_atoms",
            cutoff_roundoff="none", distance_comparison="less_than_or_equal", angular_roundoff_cap=None,
            recognition_scope="full_source_chemical_state_rdkit_matches", chemistry_evidence=features["evidence"],
            hydrogen_policy="rdkit_declared_and_valence_implicit_hydrogens",
            adaptation="single_source_scopes_sparse_output_and_optional_mic_no_residue_pruning",
        )
        software = features["software"]
    else:
        rings = get_aromatic_rings(states, chemical_state=state_index,
                                  assume_complete_connectivity=assume_complete_connectivity,
                                  max_cyclic_block_size=max_cyclic_block_size)
        charge_topology = source.topology if isinstance(source, MolSys) else source if isinstance(source, Topology) else convert(source, to_form="molsysmt.Topology")
        if charge_topology is None:
            raise StructuralInconsistencyError(reason="Formal-charge center recognition requires an element inventory.", caller=_CALLER)
        charge_view, state_view = copy(charge_topology), copy(states)
        state_view._reference_index = state_index
        charge_view._chemical_states_domain = state_view
        charge_centers = get_charge_centers(charge_view, assume_complete_connectivity=assume_complete_connectivity)
        all_charges = np.asarray(puw.get_value(charge_centers["charges"], to_unit="e"))
        positive = np.flatnonzero(all_charges > 0)
        center_members = [charge_centers["atom_indices"][charge_centers["atom_offsets"][i]:charge_centers["atom_offsets"][i + 1]]
                          for i in positive]
        charges = all_charges[positive]
        ring_members = [rings["atom_indices"][a:b] for a, b in zip(rings["atom_offsets"][:-1], rings["atom_offsets"][1:])]
        feature_parameters = dict(
            geometry_rule_version="cation_centroid_angle_offset@1", method_reference=None,
            cation_point="arithmetic_centroid_of_all_participant_atoms",
            charge_definition=charge_centers["definition"], charge_source=charge_centers["charge_source"],
            charge_rule_version=charge_centers["rule_version"], charge_evidence=charge_centers["evidence"],
            charge_policy="positive_net_formal_charge_no_partial_charge_fallback",
            participant_definition=rings["definition"], recognition_rule_version=rings["rule_version"],
            ring_method=rings["method"], aromatic_evidence=rings["evidence"],
            max_cyclic_block_size=max_cyclic_block_size, recognition_scope="full_source_chemical_state",
            plane_method="unweighted_orthogonal_least_squares", cutoff_roundoff="one_float64_ulp",
            distance_comparison="positive_and_less_than_or_equal", angular_roundoff_cap="strictly_below_pi_over_2",
        )
        software = {**rings["software"], **charge_centers["software"]}
        if method == "molstar_geometry":
            from molsysmt._private.scientific_references import MOLSTAR_REFERENCE

            feature_parameters.update(
                method_reference=MOLSTAR_REFERENCE, geometry_rule_version="molstar.CationPi.geometry@48071795",
                plane_method="cross_of_first_three_basis_member_atoms", cutoff_roundoff="none",
                distance_comparison="positive_and_less_than_or_equal", angular_roundoff_cap=None,
                adaptation="geometry_only_declared_molsysmt_centers_and_ring_basis_no_molstar_valence_or_refinement",
            )
    n_cations = len(center_members)
    members = center_members + ring_members
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
    cations = np.arange(n_cations, dtype=np.int64)
    ring_indices = np.arange(n_cations, len(members), dtype=np.int64)
    first_cations, first_rings = cations[in_first[cations]], ring_indices[in_first[ring_indices]]
    if selection_mode == "between":
        searches = [(first_cations, ring_indices[in_second[ring_indices]]),
                    (cations[in_second[cations]], first_rings)]
    else:
        searches = [(first_cations, first_rings)]
        if selection_mode == "incident":
            searches.extend([(first_cations, ring_indices[~in_first[ring_indices]]),
                             (cations[~in_first[cations]], first_rings)])
    searches = [(a, b) for a, b in searches if len(a) and len(b)]
    universe = np.unique(np.concatenate([members[i] for i in active_indices])) if len(active_indices) else np.empty(0, dtype=np.int64)
    metadata = dict(
        n_atoms=n_atoms, n_structures=n_structures, evaluated_structure_indices=frames,
        method=_CALLER, software=software,
        measure_units={"distance": "nm", "normal_angle": "radians", "offset": "nm", "height": "nm",
                       "ring_rms_deviation": "nm", "ring_max_deviation": "nm", "cation_charge": "e",
                       **({"oriented_normal_angle": "radians"} if method == "prolif" else {})},
        parameters={
            "method": method, **feature_parameters,
            **{name: {"value": value, "unit": "radians" if name == "angle_threshold" else "nm"}
               for name, value in thresholds.items()},
            "chemical_state_index": state_index, "pbc": pbc,
            "image_policy": "whole_participants_anchor_relative_mic", "pbc_policy": "mic_when_box_available",
            "exclude_overlap": method == "centroid_angle_offset", "exclude_direct_covalent": method == "centroid_angle_offset", "intramolecular": "included",
            "memory_policy": "numeric_working_estimates@1",
        },
        evaluation_mode=selection_mode, evaluation_atom_indices=np.intersect1d(first, universe),
        evaluation_atom_indices_b=None if second is None else np.intersect1d(second, universe),
        evaluation_universe_indices=universe,
    )
    if not len(frames) or not searches:
        metadata["parameters"].update(execution="none", execution_chunks=0)
        result = Interactions.from_records([], **metadata)
    else:
        per_frame = 4 * 24 * len(universe) + 256 * len(active_indices) + 192 * max(len(members[i]) for i in active_indices) + 2048 + (288 if pbc else 0)
        reducer = _CationPiReducer(members=members, active=active_indices, universe=universe, searches=searches,
                              excluded=connected_group_pairs(members, covalent) if method == "centroid_angle_offset" else set(), thresholds=thresholds,
                                  n_cations=n_cations, charges=charges, method=method,
                                  metadata=metadata, budget_bytes=configure.max_ram_usage)
        result = execute_projected_geometry(coordinate_source, universe=universe, frames=frames,
                                            reducer=reducer, per_frame_bytes=per_frame,
                                            pbc=pbc, heavy_mode=heavy_mode, caller=_CALLER)
    return result if output_type == "molsysmt.interactions" else convert(result, to_form="molsysmt.InteractionsDict")
