"""Detect sparse proximity observations between chemically typed metal_coordination atoms."""

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
@attributed("metal_coordination")
def get_metal_coordination(
    molecular_system, selection="all", selection_2=None, structure_indices="all",
    chemical_state="reference", method="metal_ligand_distance", distance_threshold=None,
    selection_mode="internal", pbc=True, assume_complete_connectivity=False,
    output_type="molsysmt.Interactions", syntax="MolSysMT", skip_digestion=False,
    *, max_matches=100000, heavy_mode="auto", profile=None,
):
    """Observing sparse metal-ligand candidates with an inclusive distance cutoff.

    Return an independent analysis; attachment to a molecular system is explicit.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying coordinates and complete declared chemistry:
        elements, covalent orders, formal charges and atom/bond aromatic flags.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Source atom selection. Recognize full chemistry before filtering sites.
    selection_2 : str, list, tuple, numpy.ndarray, or None, default=None
        Disjoint second selection, required only for between mode.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based). Evaluate repeated indices once, sorted.
        Frames without candidates retain explicit evaluated coverage.
    chemical_state : {'reference', 'structure'}, int, or None, default='reference'
        State supplying sites. Structure assignments must resolve one state.
    method : str, default='metal_ligand_distance'
        Descriptive pair-distance criterion. The profile fixes chemical sites.
    distance_threshold : quantity, str, or None, default=None
        Finite positive scalar length cutoff. None uses 0.28 nm, inclusive
        without an added tolerance, matching the reference Distance core.
    selection_mode : {'internal', 'incident', 'between'}, default='internal'
        Both atoms in selection, either atom in selection, or one in each of two
        disjoint selections. Roles always remain metal followed by ligand.
    pbc : bool, default=True
        Use MIC when a valid box exists, anchored on the metal. Preserve the
        actual periodic image used for the observed pair distance.
    assume_complete_connectivity : bool, default=False
        Record a completeness assumption without repairing chemical assignments.
    output_type : str, default='molsysmt.Interactions'
        Sparse molsysmt.Interactions or typed molsysmt.InteractionsDict.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate selection and selection_2.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    max_matches : int, default=100000
        Keyword-only maximum full-source matches per chemical SMARTS.
    heavy_mode : {'auto', 'force', 'off'}, default='auto'
        Keyword-only execution policy. Native/H5MSM index selections can stream
        projected coordinate blocks. Accepted sparse output remains in RAM.
    profile : str or None, default=None
        Keyword-only smarts_metal_ligand profile from ProLIF 2.2.2. None selects
        that profile. The ProLIF package is not required at runtime.

    Returns
    -------
    molsysmt.Interactions or molsysmt.InteractionsDict
        Directed distinct pairs, singleton metal and ligand roles, distance in
        nm, explicit scope, evaluated frames, chemistry evidence, producer
        versions, reference bibliography and observed periodic images.

    Raises
    ------
    ArgumentError
        If cutoff, units, profile, state, selections or indices are invalid.
    StructuralInconsistencyError
        If chemistry, finite coordinates or valid periodic boxes are absent.
    UnsupportedHeavyOperationError
        If a forced streaming route is unsupported or max_matches is exceeded.
    MemoryBudgetExceededError
        If numerical graph, candidate or resident-result estimates exceed budget.

    Notes
    -----
    Reproduce ProLIF 2.2.2 MetalDonor/Distance sites and <=0.28 nm geometry.
    This is a broad experimental proximity profile, not a metal-specific
    physical model or proof of a coordination bond, oxidation state, geometry,
    coordination number, affinity or energy. Water oxygen can be a ligand.
    Recognition excludes dative graph edges; stored dative assignments remain
    independent and are never created or changed by this calculation.
    Self pairs are excluded. Covalent neighbors and intramolecular pairs are
    included. If an atom has both site roles, reversed role assignments are
    distinct relations rather than unordered duplicates.

    The calculation retains full source chemistry and accepted sparse output.
    Coordinate blocks, candidate searches and accumulation use bounded numeric
    working estimates; Python overhead and process RSS are excluded. Rich H5MSM
    selections require bounded eager loading. No incremental writer is supplied.
    Optional Ackredit credits completed calculations; saved producer provenance
    identifies the original calculation, not the software used on later reads.

    See Also
    --------
    molsysmt.physchem.get_metal_coordination_sites
        Recognizing reusable metal and ligand sites without geometry.
    molsysmt.Interactions.query
        Querying sparse occurrences by atom and structure indices.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from rdkit import Chem
    >>> molsys = msm.convert(Chem.MolFromSmiles('[Zn+2].O'), to_form='molsysmt.MolSys')
    >>> molsys.structures.append(coordinates=msm.pyunitwizard.quantity([[[0,0,0],[0.2,0,0]]], 'nm'))
    >>> result = msm.interactions.metal_coordination.get_metal_coordination(molsys, pbc=False)
    >>> result.participant_roles, result.n_interactions
    (('metal', 'ligand'), 1)

    .. admonition:: User guide

       See :ref:`Getting metal coordination <Tutorial_Get_metal_coordination>`.

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
    from molsysmt.physchem import get_metal_coordination_sites
    from molsysmt.topology._chemical_graph import (
        chemical_graph_context,
        select_chemical_atoms,
    )

    from ._reducer import _MetalCoordinationReducer

    caller = "molsysmt.interactions.metal_coordination.get_metal_coordination"
    if (selection_mode == "between") != (selection_2 is not None):
        raise ArgumentError("selection_2", caller=caller, message="Supply a second selection only for between searches.")
    distance = .28 if distance_threshold is None else np.asarray(puw.get_value(distance_threshold, to_unit="nm"))
    if np.shape(distance) != () or not np.isfinite(distance) or distance <= 0:
        raise ArgumentError("distance_threshold", caller=caller, message="Use a finite positive scalar length.")
    dimensions = modular_h5msm_dimensions(molecular_system)
    modular = dimensions is not None
    if dimensions is None:
        dimensions = get(molecular_system, n_atoms=True, n_structures=True)
    if any(value is None for value in dimensions):
        raise StructuralInconsistencyError(reason="Declared atom and structure axes are required.", caller=caller)
    n_atoms, n_structures = map(int, dimensions)
    frames = np.arange(n_structures, dtype=np.int64) if is_all(structure_indices) else np.unique(structure_indices).astype(np.int64)
    if np.any(frames < 0) or np.any(frames >= n_structures):
        raise ArgumentError("structure_indices", value=structure_indices, caller=caller)
    fixed = 8 * (2 * n_atoms + 4 * n_structures)
    SparseColumnAccumulator({}, budget_bytes=configure.max_ram_usage // 2, fixed_bytes=fixed).check_budget()
    coordinate_source = molecular_system
    index_selections = all(value is None or not isinstance(value, str) or is_all(value) for value in (selection, selection_2))
    if modular and not index_selections:
        from molsysmt._private.execution.memory_policy import estimate_footprint
        from molsysmt._private.h5msm import maybe_read_modular_h5msm

        if heavy_mode == "force" or estimate_footprint(n_atoms, n_structures) > configure.max_ram_usage:
            raise UnsupportedHeavyOperationError(operation=caller, form="H5MSM rich selections",
                                                 reason="Use atom-index selections or all for bounded file calculations.")
        molecular_system = maybe_read_modular_h5msm(molecular_system)
        coordinate_source = molecular_system
    source, states, _, state_index, _, _, selection_frames = chemical_graph_context(
        molecular_system, chemical_state, frames, assume_complete_connectivity, caller)
    sites = get_metal_coordination_sites(source, chemical_state=state_index,
                                 assume_complete_connectivity=assume_complete_connectivity, max_matches=max_matches)
    metals, ligands = sites["metal_atom_indices"], sites["ligand_atom_indices"]
    first = select_chemical_atoms(source, states, state_index, selection, selection_frames, syntax)
    second = None if selection_2 is None else select_chemical_atoms(source, states, state_index, selection_2, selection_frames, syntax)
    if second is not None and np.intersect1d(first, second).size:
        raise ArgumentError("selection_2", caller=caller, message="Between selections must be disjoint.")
    selected_metals, selected_ligands = np.intersect1d(metals, first), np.intersect1d(ligands, first)
    if selection_mode == "internal":
        searches = [(selected_metals, selected_ligands)]
    elif selection_mode == "incident":
        searches = [(selected_metals, ligands), (np.setdiff1d(metals, first), selected_ligands)]
    else:
        searches = [(selected_metals, np.intersect1d(ligands, second)),
                    (np.intersect1d(metals, second), selected_ligands)]
    searches = [(a, b) for a, b in searches if len(a) and len(b)]
    universe = np.unique(np.concatenate([np.concatenate(pair) for pair in searches])) if searches else np.empty(0, dtype=np.int64)
    selected = np.intersect1d(first, universe)
    atoms = np.union1d(metals, ligands)
    reference = dict(sites["method_reference"])
    reference["geometry"] = reference["implementation"].replace("interactions.py", "base.py")
    metadata = dict(
        n_atoms=n_atoms, n_structures=n_structures, evaluated_structure_indices=frames,
        method=caller, software=sites["software"], measure_units={"distance": "nm"},
        evaluation_mode=selection_mode, evaluation_atom_indices=selected,
        evaluation_atom_indices_b=None if second is None else np.intersect1d(second, universe),
        evaluation_universe_indices=universe,
        parameters=dict(
            method=method, method_reference=reference, geometry_rule_version="metal_coordination_metal_ligand_distance@1",
            site_definition=sites["method"], chemistry_evidence=sites["evidence"], smarts_patterns=sites["smarts_patterns"],
            max_matches=max_matches, distance_threshold={"value": float(distance), "unit": "nm"},
            comparisons="inclusive_without_tolerance", chemical_state_index=state_index,
            assume_complete_connectivity=assume_complete_connectivity, recognition_scope="full_source_chemical_state",
            pbc=pbc, pbc_policy="mic_when_box_available", image_policy="pair_mic_anchored_on_metal",
            pair_identity="distinct_directed_metal_ligand_source_atom_indices", intramolecular="included", covalent_exclusion="none",
            occupancy_policy="individual_frame_observations", adaptation="single_source_sparse_scopes_no_residue_pruning_metal_anchored_pair_mic",
            memory_policy="numeric_working_estimates@1",
        ),
    )
    if not len(frames) or not searches:
        metadata["parameters"].update(execution="none", execution_chunks=0)
        result = Interactions.from_records([], **metadata)
    else:
        reducer = _MetalCoordinationReducer(universe=universe, searches=searches, distance=float(distance),
                                      metadata=metadata, budget_bytes=configure.max_ram_usage)
        per_frame = 4 * 24 * len(universe) + 256 * len(atoms) + 4096 + (288 if pbc else 0)
        result = execute_projected_geometry(coordinate_source, universe=universe, frames=frames, reducer=reducer,
                                           per_frame_bytes=per_frame, pbc=pbc, heavy_mode=heavy_mode, caller=caller)
    return result if output_type == "molsysmt.interactions" else convert(result, to_form="molsysmt.InteractionsDict")
