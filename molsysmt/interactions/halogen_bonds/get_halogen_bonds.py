"""Detect directional halogen observations with sparse source indices."""

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
from molsysmt._private.variables import is_all


@signal(tags=["api", "interactions"])
@arg_digest()
@dep_digest("rdkit")
@attributed("halogen_bonds")
def get_halogen_bonds(
    molecular_system,
    selection="all",
    selection_2=None,
    structure_indices="all",
    chemical_state="reference",
    method="distance_two_angles",
    distance_threshold=None,
    donor_angle_range=None,
    acceptor_angle_range=None,
    selection_mode="internal",
    pbc=True,
    assume_complete_connectivity=False,
    output_type="molsysmt.Interactions",
    syntax="MolSysMT",
    skip_digestion=False,
    *,
    max_matches=100000,
    heavy_mode="auto",
    profile=None,
):
    """Detecting sparse halogen bonds by distance and two directional angles.

    Evaluate D-X...A-R chemical sites using a separately identified recognition
    profile. Return observations without automatically attaching them to MolSys.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying coordinates and declared elements,
        connectivity, covalent orders, formal charges and aromatic flags.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Source atom selection defining the calculation scope. All four roles
        count for internal, incident and between membership.
    selection_2 : str, list, tuple, numpy.ndarray, or None, default=None
        Disjoint second selection, required only for between mode.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based). Evaluate repeated indices once, sorted;
        evaluated frames without observations remain explicit.
    chemical_state : {'reference', 'structure'}, int, or None, default='reference'
        State supplying chemical sites. Structure-assigned states must resolve
        one known state across all requested frames.
    method : str, default='distance_two_angles'
        Distance and two inclusive angular intervals. The recognition profile
        and exact reference definition are recorded separately.
    distance_threshold : quantity, str, or None, default=None
        Finite positive scalar length cutoff for X-A. None uses 0.35 nm.
    donor_angle_range : quantity, str, or None, default=None
        Two-value angular quantity [minimum, maximum] for D-X-A, ordered within
        zero to pi radians. None uses [130, 180] degrees.
    acceptor_angle_range : quantity, str, or None, default=None
        Two-value angular quantity [minimum, maximum] for X-A-R, ordered within
        zero to pi radians. None uses [80, 140] degrees.
    selection_mode : {'internal', 'incident', 'between'}, default='internal'
        Require all four atoms in selection, any atom in selection, or all in
        the union of both selections with at least one in each, respectively.
    pbc : bool, default=True
        Use MIC when a box exists. Reconstruct the observed D-X-A-R chain from
        adjacent MIC vectors and retain its integer images, anchored on D.
    assume_complete_connectivity : bool, default=False
        Record an explicit completeness assumption without repairing source
        chemistry when connectivity metadata is insufficient.
    output_type : str, default='molsysmt.Interactions'
        Sparse molsysmt.Interactions or typed molsysmt.InteractionsDict.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate selection and selection_2.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    max_matches : int, default=100000
        Keyword-only maximum matches per chemical SMARTS before selection.
    heavy_mode : {'auto', 'force', 'off'}, default='auto'
        Keyword-only execution policy. Native/H5MSM projected coordinates use
        bounded blocks; accepted sparse observations remain in memory.
    profile : str or None, default=None
        Keyword-only smarts_donor_acceptor profile from ProLIF 2.2.2. None
        selects that profile. The ProLIF package is not a runtime dependency.

    Returns
    -------
    molsysmt.Interactions or molsysmt.InteractionsDict
        Four singleton roles donor, halogen, acceptor, acceptor_reference;
        X-A, D-X and A-R distances in nm and D-X-A/X-A-R angles in radians.
        Distinct reference neighbors remain distinct relations. Coverage,
        actual atom scope, versions, scientific/reference bibliography and
        periodic images serialize without a dense pair-by-frame matrix.

    Raises
    ------
    ArgumentError
        If units, intervals, method, selections, state or indices are invalid.
    StructuralInconsistencyError
        If required chemistry, finite coordinates or valid boxes are absent.
    UnsupportedHeavyOperationError
        If forced streaming is unavailable, a block exceeds budget or a
        chemical match limit is exceeded.
    MemoryBudgetExceededError
        If chemical matching, candidates or resident sparse output exceed
        their numerical working estimates.

    Notes
    -----
    Reproduce ProLIF 2.2.2 XBAcceptor/DoubleAngle core on the full source graph,
    without ligand/protein residue fingerprinting or covalent/intramolecular
    exclusions. Geometry adapts Auffinger et al., PNAS 2004,
    doi:10.1073/pnas.0407607101. This is not the paper's exact element-specific
    van der Waals criterion or proof of attractive energy. All interval bounds
    are inclusive with no added geometric tolerance; undefined angles are skipped.
    Floating-point evaluation and angstrom-to-nanometer conversion can change
    membership exactly on a cutoff even when measured angles agree to roundoff.
    Chemical acceptor rules differ from hydrogen bonds. Every A-R neighbor
    matching the profile supplies a separately identifiable directional observation.

    Coherent chain MIC is a MolSysMT periodic extension to the raw reference
    coordinates. It reconstructs listed adjacent vectors, not ring closure or a
    whole molecular component. Stored row-box shifts reproduce both measured
    angles and the contact distance. Numeric coordinate blocks reserve one
    quarter of the configured RAM budget, candidates one eighth and sparse
    accumulation one half; graphs, Python overhead and process RSS are outside
    those estimates. There is no incremental result writer.

    Completed empty calculations retain coverage and attribution. Optional
    Ackredit credits the active workflow; reading results does not credit a
    new calculation. RDKit is lazy and used for chemical matching, not ProLIF.

    See Also
    --------
    molsysmt.physchem.get_halogen_bond_sites
        Preparing ordered chemical sites without evaluating coordinates.
    molsysmt.Interactions.query
        Querying observations by structure and participating atom indices.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from rdkit import Chem
    >>> system = msm.convert(Chem.MolFromSmiles('CCl.C=O'), to_form='molsysmt.MolSys')
    >>> xyz = [[[-0.15, 0, 0], [0, 0, 0], [0.36, 0.104, 0], [0.30, 0, 0]]]
    >>> system.structures.append(coordinates=msm.pyunitwizard.quantity(xyz, 'nm'))
    >>> analysis = msm.interactions.halogen_bonds.get_halogen_bonds(system, pbc=False)
    >>> analysis.n_interactions, analysis.parameters['method']
    (1, 'distance_two_angles')

    .. admonition:: User guide

       See :ref:`Getting halogen bonds <Tutorial_Get_halogen_bonds>`.

    .. versionadded:: 1.0.0
    """
    from molsysmt import configure
    from molsysmt._private.execution.projected_geometry import (
        execute_projected_geometry,
    )
    from molsysmt._private.execution.sparse_accumulator import SparseColumnAccumulator
    from molsysmt._private.h5msm import modular_h5msm_dimensions
    from molsysmt.basic import convert, get
    from molsysmt.interactions.result import Interactions
    from molsysmt.physchem import get_halogen_bond_sites
    from molsysmt.topology._chemical_graph import (
        chemical_graph_context,
        select_chemical_atoms,
    )

    from ._reducer import _HalogenReducer

    caller = "molsysmt.interactions.halogen_bonds.get_halogen_bonds"
    if (selection_mode == "between") != (selection_2 is not None):
        raise ArgumentError(
            "selection_2",
            caller=caller,
            message="Supply a second selection only for between searches.",
        )
    distance = (
        0.35
        if distance_threshold is None
        else np.asarray(puw.get_value(distance_threshold, to_unit="nm"))
    )
    if np.shape(distance) != () or not np.isfinite(distance) or distance <= 0:
        raise ArgumentError(
            "distance_threshold",
            caller=caller,
            message="Use a finite positive scalar length.",
        )
    donor_angle = (
        np.deg2rad([130.0, 180.0])
        if donor_angle_range is None
        else np.asarray(puw.get_value(donor_angle_range, to_unit="radians"))
    )
    acceptor_angle = (
        np.deg2rad([80.0, 140.0])
        if acceptor_angle_range is None
        else np.asarray(puw.get_value(acceptor_angle_range, to_unit="radians"))
    )
    dimensions = modular_h5msm_dimensions(molecular_system)
    modular = dimensions is not None
    if dimensions is None:
        dimensions = get(molecular_system, n_atoms=True, n_structures=True)
    if any(value is None for value in dimensions):
        raise StructuralInconsistencyError(
            reason="Declared atom and structure axes are required.", caller=caller
        )
    n_atoms, n_structures = map(int, dimensions)
    frames = (
        np.arange(n_structures, dtype=np.int64)
        if is_all(structure_indices)
        else np.unique(structure_indices).astype(np.int64)
    )
    if np.any(frames < 0) or np.any(frames >= n_structures):
        raise ArgumentError("structure_indices", value=structure_indices, caller=caller)
    fixed = 8 * (2 * n_atoms + 4 * n_structures)
    SparseColumnAccumulator(
        {}, budget_bytes=configure.max_ram_usage // 2, fixed_bytes=fixed
    ).check_budget()
    coordinate_source = molecular_system
    index_selections = all(
        value is None or not isinstance(value, str) or is_all(value)
        for value in (selection, selection_2)
    )
    if modular and not index_selections:
        from molsysmt._private.execution.memory_policy import estimate_footprint
        from molsysmt._private.h5msm import maybe_read_modular_h5msm

        if (
            heavy_mode == "force"
            or estimate_footprint(n_atoms, n_structures) > configure.max_ram_usage
        ):
            raise UnsupportedHeavyOperationError(
                operation=caller,
                form="H5MSM rich selections",
                reason="Use atom-index selections or all for bounded file calculations.",
            )
        molecular_system = maybe_read_modular_h5msm(molecular_system)
        coordinate_source = molecular_system
    source, states, _, state_index, _, _, selection_frames = chemical_graph_context(
        molecular_system, chemical_state, frames, assume_complete_connectivity, caller
    )
    sites = get_halogen_bond_sites(
        source,
        chemical_state=state_index,
        assume_complete_connectivity=assume_complete_connectivity,
        max_matches=max_matches,
    )
    donors, acceptors = sites["donor_halogen_pairs"], sites["acceptor_reference_pairs"]
    first = select_chemical_atoms(
        source, states, state_index, selection, selection_frames, syntax
    )
    second = (
        None
        if selection_2 is None
        else select_chemical_atoms(
            source, states, state_index, selection_2, selection_frames, syntax
        )
    )
    if second is not None and np.intersect1d(first, second).size:
        raise ArgumentError(
            "selection_2", caller=caller, message="Between selections must be disjoint."
        )
    if selection_mode != "incident":
        union = first if second is None else np.union1d(first, second)
        donors = donors[np.isin(donors, union).all(axis=1)]
        acceptors = acceptors[np.isin(acceptors, union).all(axis=1)]
    donor_rows, acceptor_rows = np.arange(len(donors)), np.arange(len(acceptors))
    if selection_mode == "incident":
        in_first = np.isin(donors, first).any(axis=1)
        searches = [
            (donor_rows[in_first], acceptor_rows),
            (
                donor_rows[~in_first],
                acceptor_rows[np.isin(acceptors, first).any(axis=1)],
            ),
        ]
    else:
        searches = [(donor_rows, acceptor_rows)]
    searches = [(d, a) for d, a in searches if len(d) and len(a)]
    universe = np.unique(np.concatenate((donors.ravel(), acceptors.ravel())))
    metadata = dict(
        n_atoms=n_atoms,
        n_structures=n_structures,
        evaluated_structure_indices=frames,
        method=caller,
        software=sites["software"],
        measure_units={
            "distance": "nm",
            "donor_angle": "radians",
            "acceptor_angle": "radians",
            "donor_halogen_distance": "nm",
            "acceptor_reference_distance": "nm",
        },
        evaluation_mode=selection_mode,
        evaluation_atom_indices=np.intersect1d(first, universe),
        evaluation_atom_indices_b=None
        if second is None
        else np.intersect1d(second, universe),
        evaluation_universe_indices=universe,
        parameters=dict(
            method=method,
            method_reference=sites["method_reference"],
            geometry_rule_version="distance_two_angles_halogen@1",
            scientific_references=["auffinger_2004"],
            scientific_reference_relationship="adapted_not_original_thresholds",
            site_definition=sites["method"],
            chemistry_evidence=sites["evidence"],
            smarts_patterns=sites["smarts_patterns"],
            max_matches=max_matches,
            distance_threshold={"value": float(distance), "unit": "nm"},
            donor_angle_range={"value": donor_angle.tolist(), "unit": "radians"},
            acceptor_angle_range={"value": acceptor_angle.tolist(), "unit": "radians"},
            comparisons="inclusive_without_tolerance",
            chemical_state_index=state_index,
            assume_complete_connectivity=assume_complete_connectivity,
            recognition_scope="full_source_chemical_state",
            pbc=pbc,
            pbc_policy="mic_when_box_available",
            image_policy="adjacent_chain_mic_anchored_on_donor",
            reference_neighbors="distinct_directional_observations",
            intramolecular="included",
            covalent_exclusion="none",
            undefined_angles="skipped",
            occupancy_policy="individual_frame_observations",
            adaptation="single_source_sparse_scopes_no_residue_pruning_coherent_chain_mic",
        ),
    )
    metadata["execution"] = {"memory_policy": "numeric_working_estimates@1"}
    if not len(frames) or not searches:
        metadata["execution"].update(execution="none", execution_chunks=0)
        result = Interactions.from_records([], **metadata)
    else:
        reducer = _HalogenReducer(
            donors=donors,
            acceptors=acceptors,
            universe=universe,
            searches=searches,
            first=first,
            second=second,
            distance=float(distance),
            donor_angle=donor_angle,
            acceptor_angle=acceptor_angle,
            metadata=metadata,
            budget_bytes=configure.max_ram_usage,
        )
        per_frame = (
            4 * 24 * len(universe)
            + 384 * (len(donors) + len(acceptors))
            + 4096
            + (288 if pbc else 0)
        )
        result = execute_projected_geometry(
            coordinate_source,
            universe=universe,
            frames=frames,
            reducer=reducer,
            per_frame_bytes=per_frame,
            pbc=pbc,
            heavy_mode=heavy_mode,
            caller=caller,
        )
    return (
        result
        if output_type == "molsysmt.interactions"
        else convert(result, to_form="molsysmt.InteractionsDict")
    )
