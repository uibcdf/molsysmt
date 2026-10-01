"""Detecting minimum-distance observations between formal-charge participants."""

import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.interaction_attribution import attributed
from molsysmt._private.smonitor import (
    ArgumentError,
    StructuralInconsistencyError,
    UnsupportedHeavyOperationError,
)
from molsysmt._private.sparse_membership import whole_group_selection
from molsysmt._private.variables import is_all

_CALLER = "molsysmt.interactions.ionic.get_ionic_interactions"


@signal(tags=["api", "interactions"])
@arg_digest()
@attributed("ionic", "minimum_distance")
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
    *,
    heavy_mode="auto",
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
    heavy_mode : {'auto', 'force', 'off'}, default='auto'
        Keyword-only execution policy. Chunked execution supports native MolSys
        and H5MSM 0.5 paths with atom-index selections or 'all'. Auto also
        considers selected-block working estimates. Off requests eager execution
        within the budget; force processes bounded coordinate blocks.

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
        If chunked execution is needed for an unsupported form/selection, or
        selected coordinate buffers cannot fit the configured working estimate.
    MemoryBudgetExceededError
        If candidate or resident sparse-result working estimates exceed their
        allocated portions of configure.max_ram_usage. No partial result is returned.

    Notes
    -----
    Analysis parameters retain the minimum_distance criterion and compact
    bibliography. Completed calculations also contribute to an optional
    Ackredit session; loading or querying an analysis does not credit a new
    calculation. Bibliographic metadata is identical without Ackredit.

    This experimental definition recognizes carboxylate and guanidinium plus
    literal formal-charge atoms/clusters; phosphate, sulfate, and aromatic
    delocalization are not resolved universally. Intramolecular contacts are
    included. Self/overlapping centers cannot occur in the recognizer's disjoint
    partition. Directly covalently bonded centers are excluded; dative bonds
    do not impose this exclusion. No residue, component, or energy exclusion
    is inferred. All source chemistry is examined before filtering centers.
    The calculation neither attaches an analysis nor modifies coordinates.
    Chemistry is prepared once. Chunked H5MSM 0.5 calculations load topology,
    chemical states, and association metadata without loading structural series
    or saved analyses. Atom axes must have declared identity links. A structure
    selection must resolve to one state when chemical_state='structure'.
    Rich string selections retain the eager route; chunked requests reject them.
    The complete sparse result remains resident. Coordinate blocks reserve one
    quarter of the configured budget, candidate searches one eighth each, and
    sparse accumulation/packing one half. Estimates include numerical workspace
    factors, not caller-owned coordinates, chemistry tables, Python overhead,
    or a process RSS guarantee. There is no incremental result writer or public
    checkpoint/resume route. Candidate batching uses a conservative possible-pair
    bound and can reject a budget even when actual neighbors would be sparse.

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
    from molsysmt._private.execution import ChunkedExecutor
    from molsysmt._private.execution.memory_policy import (
        decide_mode,
        estimate_footprint,
    )
    from molsysmt._private.h5msm import (
        maybe_read_modular_h5msm,
        modular_h5msm_dimensions,
    )
    from molsysmt.basic import convert, get, select
    from molsysmt.interactions.ionic._reducer import _IonicReducer
    from molsysmt.interactions.result import Interactions
    from molsysmt.native import MolSys
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
    modular_source = dimensions is not None
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
    mode = decide_mode(estimate_footprint(n_atoms, n_structures), heavy_mode)
    index_selections = all(
        value is None or not isinstance(value, str) or is_all(value)
        for value in (selection, selection_2)
    )
    supported_source = isinstance(molecular_system, MolSys) or modular_source
    if mode == "heavy" and not (supported_source and index_selections):
        raise UnsupportedHeavyOperationError(
            operation=_CALLER, form="ionic detection",
            reason="Chunked ionic detection requires native MolSys or H5MSM 0.5 and atom-index selections or all.",
        )
    if mode == "eager" and estimate_footprint(n_atoms, n_structures) > config.max_ram_usage:
        raise UnsupportedHeavyOperationError(
            operation=_CALLER, form="eager ionic detection",
            reason="The source coordinate estimate exceeds the RAM budget with heavy_mode='off'.",
        )
    coordinate_source = molecular_system
    selection_frames = frames
    if modular_source and index_selections:
        from molsysmt.form._h5msm05_modular import _read_calculation_chemistry

        molecular_system, chemical_state = _read_calculation_chemistry(
            molecular_system, chemical_state=chemical_state, structure_indices=frames,
        )
        selection_frames = "all"
    else:
        molecular_system = maybe_read_modular_h5msm(molecular_system)
        coordinate_source = molecular_system
        if chemical_state == "structure" and isinstance(molecular_system, MolSys):
            chemical_state = molecular_system._resolve_structure_chemical_state_index(frames)
    centers = get_charge_centers(
        molecular_system,
        chemical_state=chemical_state,
        structure_indices=selection_frames,
        assume_complete_connectivity=assume_complete_connectivity,
    )
    first = np.unique(
        select(
            molecular_system,
            selection=selection,
            syntax=syntax,
            structure_indices=selection_frames,
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
                structure_indices=selection_frames,
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
            "execution": "chunked" if mode == "heavy" else "eager",
            "memory_policy": "numeric_working_estimates@1",
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
        topology = (
            molecular_system.topology if isinstance(molecular_system, MolSys)
            else convert(molecular_system, to_form="molsysmt.Topology")
        )
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
        reducer = _IonicReducer(
            centers=centers, members=members, universe=universe,
            active=np.concatenate((positive, negative)), searches=searches,
            threshold=threshold, excluded=excluded, metadata=metadata,
            budget_bytes=config.max_ram_usage,
        )
        if supported_source:
            if modular_source and index_selections:
                import h5py

                with h5py.File(coordinate_source, "r") as source_file:
                    has_coordinates = "structures/coordinates" in source_file
            else:
                has_coordinates = (
                    coordinate_source.structures is not None
                    and coordinate_source.structures.coordinates is not None
                )
            if not has_coordinates:
                raise StructuralInconsistencyError(
                    reason="Coordinates are required to evaluate nonempty center pairs.",
                    caller=_CALLER,
                )
            frame_working_bytes = 4 * (24 * len(universe) + (72 if pbc else 0))
            block_budget = config.max_ram_usage // 4
            max_chunk_size = min(config.chunk_size, block_budget // max(1, frame_working_bytes))
            if max_chunk_size < 1:
                raise UnsupportedHeavyOperationError(
                    operation=_CALLER, form="ionic coordinate blocks",
                    reason="One selected coordinate frame exceeds the block working-memory estimate.",
                )
            if mode == "eager" and len(frames) * frame_working_bytes > block_budget:
                if heavy_mode == "auto" and index_selections:
                    mode = "heavy"
                    metadata["parameters"]["execution"] = "chunked"
                else:
                    raise UnsupportedHeavyOperationError(
                        operation=_CALLER, form="eager ionic coordinate blocks",
                        reason="Selected eager coordinates exceed the block working-memory estimate; request chunked execution.",
                    )
            result = ChunkedExecutor(
                coordinate_source,
                "file:h5msm" if modular_source and index_selections else "molsysmt.MolSys",
                _CALLER, reducer=reducer, atom_indices=universe,
                structure_indices=frames,
                heavy_mode="force" if mode == "heavy" else "off",
                attributes=["coordinates", "box"] if pbc else ["coordinates"],
                max_chunk_size=max_chunk_size,
            ).execute()
        else:
            if 4 * len(frames) * (24 * len(universe) + (72 if pbc else 0)) > config.max_ram_usage // 4:
                raise UnsupportedHeavyOperationError(
                    operation=_CALLER, form="eager ionic coordinate blocks",
                    reason="Selected eager coordinates exceed the block working-memory estimate.",
                )
            coordinates = get(molecular_system, selection=universe, structure_indices=frames, coordinates=True)
            boxes = get(molecular_system, structure_indices=frames, box=True) if pbc else None
            reducer.initialize({})
            reducer.consume({
                "coordinates": None if coordinates is None else np.asarray(puw.get_value(coordinates, to_unit="nm"), dtype=np.float64),
                "box": None if boxes is None else np.asarray(puw.get_value(boxes, to_unit="nm"), dtype=np.float64),
                "structure_indices": frames,
            })
            result = reducer.finalize()
    else:
        from molsysmt._private.execution.sparse_accumulator import (
            SparseColumnAccumulator,
        )

        SparseColumnAccumulator(
            {}, budget_bytes=config.max_ram_usage // 2,
            fixed_bytes=8 * (2 * n_atoms + 4 * n_structures),
        ).check_budget()
        metadata["parameters"]["execution_chunks"] = 0
        result = Interactions.from_records([], **metadata)
    return (
        result
        if output_type == "molsysmt.interactions"
        else convert(result, to_form="molsysmt.InteractionsDict")
    )


def _whole_selection(members, selected):
    return whole_group_selection(members, selected, caller=_CALLER,
                                 description="compound charge center")


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
