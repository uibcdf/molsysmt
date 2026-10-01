"""Public boundary for declared-aromatic ring geometry observations."""

import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import (
    ArgumentError,
    MemoryBudgetExceededError,
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
def get_pi_pi_interactions(
    molecular_system, distance_threshold, angle_threshold, offset_threshold,
    planarity_threshold, selection="all", selection_2=None, structure_indices="all",
    chemical_state="reference", method="centroid_angle_offset",
    selection_mode="internal", pbc=True, assume_complete_connectivity=False,
    output_type="molsysmt.Interactions", syntax="MolSysMT", skip_digestion=False,
    *, geometry="both", max_cyclic_block_size=256, heavy_mode="auto",
):
    """Detecting parallel and edge-to-face geometries between declared aromatic rings.

    Use complete ring memberships from get_aromatic_rings and unweighted
    least-squares planes. Explicit cutoffs define geometric candidates;
    the result does not establish attraction, binding energy or a chemical bond.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form providing coordinates and explicit selected-state
        atom/bond aromatic flags and complete covalent connectivity.
    distance_threshold : quantity or str
        Finite positive cutoff for the centroid distance, with length units.
        No universal default is supplied.
    angle_threshold : quantity or str
        Maximum deviation from parallel or perpendicular planes, with angular
        units. Must be nonnegative and strictly below 45 degrees, keeping the
        two geometry classes disjoint. Internally evaluated in radians.
    offset_threshold : quantity or str
        Finite nonnegative lateral offset cutoff, with length units. Parallel
        geometries must satisfy both planes' offsets; edge-to-face geometries
        must satisfy at least one. No universal default is supplied.
    planarity_threshold : quantity or str
        Finite nonnegative maximum orthogonal atom deviation from each ring's
        fitted plane, with length units. Warped rings exceeding it are excluded.
        Zero requires numerically exact planarity; no absolute tolerance is added.
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
        Only the documented centroid, unoriented plane-angle and offset rule
        is supported. Its version is recorded in the result.
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
    heavy_mode : {'auto', 'force', 'off'}, default='auto'
        Keyword-only execution policy. Streaming follows the form's declared
        coordinate support. Other supported forms use their ordinary getters
        eagerly when the selected working estimate fits the budget.

    Returns
    -------
    molsysmt.Interactions or dict
        Sparse pi_pi relations with ring_a/ring_b whole-ring participants,
        ordered by their source memberships. Occurrences retain centroid
        distance, acute plane angle, both lateral offsets, and each ring's
        RMS/maximum deviation (nm and radians). Evidence distinguishes parallel
        and edge-to-face observations. Images shift ring_b relative to ring_a
        using row box vectors. Source axes, evaluated frames, examined aromatic
        atom scope, chemistry evidence, parameters and producer versions are
        explicit. Empty numeric measure columns have shape (0,).

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
    Let d be the observed MIC centroid displacement and n_a/n_b the unit
    normals. The acute plane angle is atan2(norm(cross(n_a,n_b)),
    abs(dot(n_a,n_b))). Each offset is norm(d-dot(d,n)*n). Parallel accepts
    angle <= angle_threshold and max(offset_a,offset_b) <= offset_threshold.
    Edge-to-face accepts pi/2-angle <= angle_threshold and
    min(offset_a,offset_b) <= offset_threshold. Both require a positive centroid
    distance within distance_threshold and both maximum deviations within
    planarity_threshold. Inclusive comparisons allow one float64 ULP, without
    an additional absolute tolerance. Angular roundoff is capped strictly below
    pi/4 so the two classes remain disjoint even near the numerical boundary.

    Self, overlapping/fused and directly covalently linked rings are excluded.
    Other intramolecular contacts are included; dative links do not exclude a
    pair. There is no clash, energy, residue or component filter. A minimum cycle
    basis is not all cycles or SymmSSSR. Chemistry is examined across the full
    source; observation coverage contains only eligible aromatic atom scopes.
    Every selected frame is searched, without first-frame candidate pruning.
    The calculation neither attaches an analysis nor modifies its source.

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
    from molsysmt._private.execution import ChunkedExecutor
    from molsysmt._private.execution.memory_policy import decide_mode
    from molsysmt._private.execution.sparse_accumulator import SparseColumnAccumulator
    from molsysmt._private.h5msm import modular_h5msm_dimensions
    from molsysmt.basic import convert, get, get_form, select
    from molsysmt.form import _dict_modules
    from molsysmt.interactions.pi_pi._reducer import _PiPiReducer
    from molsysmt.interactions.result import Interactions
    from molsysmt.native import MolSys
    from molsysmt.physchem.get_aromatic_rings import get_aromatic_rings
    from molsysmt.topology._rings import ring_context

    thresholds = {}
    for name, value, unit, positive in (
        ("distance_threshold", distance_threshold, "nm", True),
        ("angle_threshold", angle_threshold, "radians", False),
        ("offset_threshold", offset_threshold, "nm", False),
        ("planarity_threshold", planarity_threshold, "nm", False),
    ):
        number = np.asarray(puw.get_value(value, to_unit=unit))
        if number.shape != () or not np.isfinite(number) or number < 0 or (positive and number == 0):
            raise ArgumentError(name, value=value, caller=_CALLER, message="Use a finite scalar cutoff with the required units and range.")
        thresholds[name] = float(number)
    if thresholds["angle_threshold"] >= np.pi / 4:
        raise ArgumentError("angle_threshold", caller=_CALLER, message="Angular deviation must be strictly below 45 degrees.")
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
    rings = get_aromatic_rings(states, chemical_state=state_index,
                              assume_complete_connectivity=assume_complete_connectivity,
                              max_cyclic_block_size=max_cyclic_block_size)
    members = [rings["atom_indices"][a:b] for a, b in zip(rings["atom_offsets"][:-1], rings["atom_offsets"][1:])]
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
        method=_CALLER, software=rings["software"],
        measure_units={"distance": "nm", "plane_angle": "radians", "offset_a": "nm", "offset_b": "nm",
                       "rms_deviation_a": "nm", "rms_deviation_b": "nm", "max_deviation_a": "nm", "max_deviation_b": "nm"},
        parameters={
            "method": method, "geometry": geometry, "geometry_rule_version": "centroid_angle_offset@1",
            **{name: {"value": value, "unit": "radians" if name == "angle_threshold" else "nm"}
               for name, value in thresholds.items()},
            "cutoff_roundoff": "one_float64_ulp", "distance_comparison": "positive_and_less_than_or_equal",
            "angular_roundoff_cap": "strictly_below_pi_over_4",
            "parallel_offsets": "both", "edge_to_face_offsets": "at_least_one",
            "participant_definition": rings["definition"], "recognition_rule_version": rings["rule_version"],
            "ring_method": rings["method"], "chemical_state_index": state_index, "aromatic_evidence": rings["evidence"],
            "max_cyclic_block_size": max_cyclic_block_size, "recognition_scope": "full_source_chemical_state",
            "plane_method": "unweighted_orthogonal_least_squares", "pbc": pbc,
            "image_policy": "whole_participants_anchor_relative_mic", "pbc_policy": "mic_when_box_available",
            "exclude_overlap": True, "exclude_direct_covalent": True, "intramolecular": "included",
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
        block_budget = configure.max_ram_usage // 4
        max_chunk_size = min(configure.chunk_size, block_budget // per_frame)
        if max_chunk_size < 1:
            raise UnsupportedHeavyOperationError(operation=_CALLER, form="pi-pi coordinate blocks",
                                                 reason="One projected coordinate/plane frame exceeds the block working estimate.")
        mode = decide_mode(per_frame * len(frames) * 4, heavy_mode)
        if mode == "eager" and per_frame * len(frames) > block_budget:
            raise MemoryBudgetExceededError(reason="Selected eager plane work exceeds the block budget; use streaming.",
                                            predicted_bytes=per_frame * len(frames), available_bytes=block_budget, caller=_CALLER)
        metadata["parameters"]["execution"] = "chunked" if mode == "heavy" else "eager"
        reducer = _PiPiReducer(members=members, active=active_indices, universe=universe, searches=searches,
                              excluded=connected_group_pairs(members, covalent), thresholds=thresholds,
                              geometry=geometry, metadata=metadata, budget_bytes=configure.max_ram_usage)
        form = get_form(coordinate_source)
        attributes = ["coordinates", "box"] if pbc else ["coordinates"]
        if isinstance(form, str) and getattr(_dict_modules[form], "_heavy_support", {}).get("coordinates", False):
            result = ChunkedExecutor(coordinate_source, form, _CALLER, reducer=reducer, atom_indices=universe,
                                     structure_indices=frames, attributes=attributes,
                                     heavy_mode="force" if mode == "heavy" else "off",
                                     max_chunk_size=max_chunk_size).execute()
        else:
            if mode == "heavy":
                raise UnsupportedHeavyOperationError(operation=_CALLER, form=str(form), reason="No streamed coordinate delivery route.")
            reducer.initialize({})
            coordinates = get(coordinate_source, selection=universe, structure_indices=frames, coordinates=True)
            box = get(coordinate_source, structure_indices=frames, box=True) if pbc else None
            reducer.consume(ChunkedExecutor._build_chunk({"coordinates": coordinates, "box": box, "structure_indices": frames}))
            result = reducer.finalize()
    return result if output_type == "molsysmt.interactions" else convert(result, to_form="molsysmt.InteractionsDict")
