"""Detect sparse proximity observations between chemically typed hydrophobic atoms."""

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
@attributed("hydrophobic")
def get_hydrophobic_interactions(
    molecular_system, selection="all", selection_2=None, structure_indices="all",
    chemical_state="reference", method="atom_pair_distance", distance_threshold=None,
    selection_mode="internal", pbc=True, assume_complete_connectivity=False,
    output_type="molsysmt.Interactions", syntax="MolSysMT", skip_digestion=False,
    *, max_matches=100000, heavy_mode="auto", profile=None,
):
    """Detecting sparse hydrophobic atom pairs with an inclusive distance cutoff.

    Return an independent analysis; attachment to a molecular system is explicit.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying coordinates, elements, complete connectivity,
        covalent orders, formal charges and aromatic atom/bond flags.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Source atom selection defining the calculation scope. Full source
        chemistry is recognized before filtering eligible atoms.
    selection_2 : str, list, tuple, numpy.ndarray, or None, default=None
        Disjoint second selection, required only for between mode.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based). Repeated indices are evaluated once, sorted;
        frames without observations retain explicit evaluated coverage.
    chemical_state : {'reference', 'structure'}, int, or None, default='reference'
        Chemical state supplying sites. Structure assignments must resolve one
        known state across all selected structures.
    method : str, default='atom_pair_distance'
        Descriptive distance criterion. Exact chemical recognition and numerical
        reference conventions are selected by profile and recorded separately.
    distance_threshold : quantity, str, or None, default=None
        Finite positive scalar length cutoff. None uses 0.45 nm. Bounds are
        inclusive, without an added geometric tolerance.
    selection_mode : {'internal', 'incident', 'between'}, default='internal'
        Require both atoms in selection, either atom in selection, or one atom
        in each of two disjoint selections, respectively.
    pbc : bool, default=True
        Use MIC when a valid box exists, anchored on the lower atom index.
        Preserve the actual periodic image used for the measured distance.
    assume_complete_connectivity : bool, default=False
        Record an explicit completeness assumption without repairing chemistry.
    output_type : str, default='molsysmt.Interactions'
        Sparse molsysmt.Interactions or typed molsysmt.InteractionsDict.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate selection and selection_2.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    max_matches : int, default=100000
        Keyword-only maximum full-source chemical matches before selection.
    heavy_mode : {'auto', 'force', 'off'}, default='auto'
        Keyword-only execution policy. Eligible native/H5MSM inputs deliver
        projected coordinate blocks; accepted sparse output remains in RAM.
    profile : str or None, default=None
        Keyword-only smarts_hydrophobic_atoms profile from ProLIF 2.2.2. None
        selects that profile. The ProLIF package is not required at runtime.

    Returns
    -------
    molsysmt.Interactions or molsysmt.InteractionsDict
        Distinct unordered atom pairs, in ascending source-index order, with
        singleton roles hydrophobic_1 and hydrophobic_2 and distance in nm.
        Coverage, actual search scope, chemistry evidence, reference bibliography,
        producer versions and periodic images accompany every named analysis.

    Raises
    ------
    ArgumentError
        If units, cutoff, method, profile, selections, state or indices are invalid.
    StructuralInconsistencyError
        If required chemistry, finite coordinates or valid periodic boxes are absent.
    UnsupportedHeavyOperationError
        If a forced streaming route is unsupported or a chemical match cap is exceeded.
    MemoryBudgetExceededError
        If numerical matching, candidate or resident-result estimates exceed budget.

    Notes
    -----
    Reproduce the ProLIF 2.2.2 Hydrophobic/Distance core with its SMARTS sites and
    inclusive distance rule. Source patterns incorporate RDKit chemical features;
    reference attribution does not claim invented authorship of the criterion.
    Recognition is independently available in physchem.get_hydrophobic_sites.
    This typed proximity definition is not a residue hydrophobicity scale,
    interaction energy or proof of solvent-mediated attraction. Mol* uses a
    different elemental/neighbor rule, pair exclusion and default cutoff.

    Within one source system, same-atom observations and reverse duplicates are
    excluded. Distinct coincident atoms may have zero distance. No extra covalent
    or intramolecular exclusion is inferred from the reference core. Use between
    mode with disjoint ligand/environment selections for an interfacial analysis.
    All default scope modes preserve unordered identity and canonical MIC images.
    Pair roles do not encode which selection was the ligand. This is not the
    reference application's residue fingerprint pruning or all-periodic-images
    enumeration. Roundoff at an exact cutoff can affect reference membership.

    Source chemistry and accepted sparse output remain resident. Projected
    coordinate blocks reserve one quarter of the configured numeric RAM budget,
    candidates one eighth and accumulation/packing one half. Graphs, Python
    overhead and process RSS are outside these estimates. Rich H5MSM selections
    require bounded eager loading; forced unsupported routes fail explicitly.
    There is no incremental result writer. Optional Ackredit credits completed
    calculations, including known-empty results; reading saved results does not
    credit a newly performed scientific calculation.

    See Also
    --------
    molsysmt.physchem.get_hydrophobic_sites
        Preparing chemically interpreted atom sites without geometry.
    molsysmt.physchem.get_hydrophobicity
        Looking up independent residue hydrophobicity scales.
    molsysmt.Interactions.query
        Querying occurrences by atom and structure indices.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from rdkit import Chem
    >>> molsys = msm.convert(Chem.MolFromSmiles('CCC.CCC'), to_form='molsysmt.MolSys')
    >>> xyz = [[[0,0,0], [0.15,0,0], [0.30,0,0], [0,0.3,0], [0.15,0.3,0], [0.30,0.3,0]]]
    >>> molsys.structures.append(coordinates=msm.pyunitwizard.quantity(xyz, 'nm'))
    >>> analysis = msm.interactions.hydrophobic.get_hydrophobic_interactions(molsys, pbc=False)
    >>> analysis.participant_atoms.tolist(), analysis.n_interactions
    ([1, 4], 1)

    .. admonition:: User guide

       See :ref:`Getting hydrophobic interactions <Tutorial_Get_hydrophobic_interactions>`.

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
    from molsysmt.physchem import get_hydrophobic_sites
    from molsysmt.topology._chemical_graph import (
        chemical_graph_context,
        select_chemical_atoms,
    )

    from ._reducer import _HydrophobicReducer

    caller = "molsysmt.interactions.hydrophobic.get_hydrophobic_interactions"
    if (selection_mode == "between") != (selection_2 is not None):
        raise ArgumentError("selection_2", caller=caller, message="Supply a second selection only for between searches.")
    distance = .45 if distance_threshold is None else np.asarray(puw.get_value(distance_threshold, to_unit="nm"))
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
    sites = get_hydrophobic_sites(source, chemical_state=state_index,
                                 assume_complete_connectivity=assume_complete_connectivity, max_matches=max_matches)
    atoms = sites["hydrophobic_atom_indices"]
    first = select_chemical_atoms(source, states, state_index, selection, selection_frames, syntax)
    second = None if selection_2 is None else select_chemical_atoms(source, states, state_index, selection_2, selection_frames, syntax)
    if second is not None and np.intersect1d(first, second).size:
        raise ArgumentError("selection_2", caller=caller, message="Between selections must be disjoint.")
    selected = np.intersect1d(atoms, first)
    if selection_mode == "internal":
        universe = selected
        searches = [(selected, selected, True)] if len(selected) > 1 else []
    elif selection_mode == "incident":
        universe = atoms
        external = np.setdiff1d(atoms, first)
        searches = [(selected, selected, True)] if len(selected) > 1 else []
        if len(selected) and len(external):
            searches.append((selected, external, False))
    else:
        other = np.intersect1d(atoms, second)
        universe = np.union1d(selected, other)
        searches = [(selected, other, False)] if len(selected) and len(other) else []
    reference = dict(sites["method_reference"])
    reference["geometry"] = reference["implementation"].replace("interactions.py", "base.py")
    metadata = dict(
        n_atoms=n_atoms, n_structures=n_structures, evaluated_structure_indices=frames,
        method=caller, software=sites["software"], measure_units={"distance": "nm"},
        evaluation_mode=selection_mode, evaluation_atom_indices=selected,
        evaluation_atom_indices_b=None if second is None else np.intersect1d(second, atoms),
        evaluation_universe_indices=universe,
        parameters=dict(
            method=method, method_reference=reference, geometry_rule_version="hydrophobic_atom_pair_distance@1",
            site_definition=sites["method"], chemistry_evidence=sites["evidence"], smarts_patterns=sites["smarts_patterns"],
            max_matches=max_matches, distance_threshold={"value": float(distance), "unit": "nm"},
            comparisons="inclusive_without_tolerance", chemical_state_index=state_index,
            assume_complete_connectivity=assume_complete_connectivity, recognition_scope="full_source_chemical_state",
            pbc=pbc, pbc_policy="mic_when_box_available", image_policy="pair_mic_anchored_on_lower_atom_index",
            pair_identity="distinct_unordered_source_atom_indices", intramolecular="included", covalent_exclusion="none",
            occupancy_policy="individual_frame_observations", adaptation="single_source_sparse_scopes_no_residue_pruning_canonical_pair_mic",
            memory_policy="numeric_working_estimates@1",
        ),
    )
    if not len(frames) or not searches:
        metadata["parameters"].update(execution="none", execution_chunks=0)
        result = Interactions.from_records([], **metadata)
    else:
        reducer = _HydrophobicReducer(universe=universe, searches=searches, distance=float(distance),
                                      metadata=metadata, budget_bytes=configure.max_ram_usage)
        per_frame = 4 * 24 * len(universe) + 256 * len(atoms) + 4096 + (288 if pbc else 0)
        result = execute_projected_geometry(coordinate_source, universe=universe, frames=frames, reducer=reducer,
                                           per_frame_bytes=per_frame, pbc=pbc, heavy_mode=heavy_mode, caller=caller)
    return result if output_type == "molsysmt.interactions" else convert(result, to_form="molsysmt.InteractionsDict")
