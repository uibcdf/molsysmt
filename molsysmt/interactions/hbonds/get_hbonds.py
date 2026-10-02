"""Detect attributable hydrogen-bond observations from reusable chemical sites."""

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
@dep_digest("rdkit", when={"method": "prolif", "donor_hydrogen_pairs": None})
@dep_digest("rdkit", when={"method": "donor_acceptor_distance_angle", "profile": "smarts_donor_acceptor", "donor_hydrogen_pairs": None})
@attributed("hbonds")
def get_hbonds(
    molecular_system, selection="all", selection_2=None, structure_indices="all",
    chemical_state="reference", method="baker_hubbard", distance_threshold=None,
    angle_threshold=None, selection_mode="internal", pbc=True,
    assume_complete_connectivity=False, output_type="molsysmt.Interactions",
    syntax="MolSysMT", skip_digestion=False, *, donor_hydrogen_pairs=None,
    acceptor_atom_indices=None, max_matches=100000, heavy_mode="auto", profile=None,
):
    """Detecting sparse hydrogen bonds with an explicitly attributed criterion.

    Calculate individual donor-H-acceptor observations for every requested
    structure. Existing Buch and Luzard–Chandler functions retain their outputs.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form with element symbols, complete declared covalent
        connectivity and coordinates. ProLIF additionally needs formal charges,
        bond orders and explicit atom/bond aromatic flags.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Source atom selection defining the calculation scope. An individual
        hydrogen may be selected in incident mode; roles remain separate atoms.
    selection_2 : str, list, tuple, numpy.ndarray, or None, default=None
        Disjoint second selection, required only for between mode.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based). Repeated indices are evaluated once in
        sorted order; evaluated structures without observations stay explicit.
    chemical_state : {'reference', 'structure'}, int, or None, default='reference'
        State supplying chemical sites. Structure assignments must resolve
        to one state across all requested structures.
    method : str, default='baker_hubbard'
        baker_hubbard, wernet_nilsson, or donor_acceptor_distance_angle.
        The profile fixes recognition and exact geometric conventions.
        cpptraj, prolif and mdanalysis_geometry remain compatibility aliases.
    distance_threshold : quantity, str, or None, default=None
        Positive scalar cutoff with length units. None uses H-A <0.25 nm for
        Baker–Hubbard, D-A <=0.30 nm for CPPTRAJ/MDAnalysis, D-A <=0.35 nm for
        ProLIF, or the 0.33 nm intercept of Wernet–Nilsson's angular curve.
    angle_threshold : quantity, str, or None, default=None
        Scalar minimum D-H-A angle with angular units, within 0 to 180 degrees.
        None uses >120 degrees for Baker–Hubbard, >=135 degrees for CPPTRAJ,
        >=130 degrees for ProLIF, or >150 degrees for MDAnalysis. Leave None
        for Wernet–Nilsson, whose angular criterion is its distance curve.
    selection_mode : {'internal', 'incident', 'between'}, default='internal'
        Require all three atoms in selection, at least one in selection, or
        all in the union of both selections and at least one in each, respectively.
    pbc : bool, default=True
        Use MIC when a box exists. Stored images reproduce measured geometry;
        inconsistent independent image choices raise. CPPTRAJ requires whole
        donor-H coordinates, matching its source's unwrapped donor-H vector.
    assume_complete_connectivity : bool, default=False
        Explicitly assume supplied connectivity complete when metadata is
        insufficient. Record the assumption without changing the source.
    output_type : str, default='molsysmt.Interactions'
        Sparse molsysmt.Interactions or its typed molsysmt.InteractionsDict form.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate selection and selection_2.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    donor_hydrogen_pairs : list, tuple, numpy.ndarray, or None, default=None
        Keyword-only source atom pairs with shape (n_pairs, 2), in donor/H order.
        Both explicit site arrays must be supplied together. Each pair must be
        a declared covalent bond to an indexed hydrogen; duplicates are removed.
    acceptor_atom_indices : list, tuple, numpy.ndarray, or None, default=None
        Keyword-only explicit source acceptor indices. No automatic chemical
        acceptor rule is applied to this supplied set; hydrogens are rejected.
    max_matches : int, default=100000
        Keyword-only bound per ProLIF chemical SMARTS query before selection.
    heavy_mode : {'auto', 'force', 'off'}, default='auto'
        Keyword-only execution policy. Native/H5MSM projected coordinate routes
        process bounded blocks; other forms require bounded eager delivery.

    profile : str or None, default=None
        Keyword-only calculation profile. donor_acceptor_distance_angle uses
        elemental_fon by default; smarts_donor_acceptor and explicit_sites
        select the adapted ProLIF and MDAnalysis definitions respectively.
        explicit_sites requires both site arrays. Author-named methods use
        nitrogen_oxygen. An alias already fixes its profile.

    Returns
    -------
    molsysmt.Interactions or molsysmt.InteractionsDict
        Sparse hbond relations with donor, hydrogen and acceptor singleton
        participants. Measurements retain all three observed distances in nm
        and D-H-A/H-D-A angles in radians, including empty (0,) columns. Coverage,
        source indices, chemical scope, parameters, evidence, reference method
        and actual producer versions remain explicit and serialize in H5MSM 0.5.
        Periodic image vectors shift each atom relative to the donor using row
        box vectors. No result is automatically attached to the source.

    Raises
    ------
    ArgumentError
        If cutoffs, explicit sites, selections, method or indices are invalid.
    StructuralInconsistencyError
        If required chemistry, coordinates or coherent periodic geometry are absent.
    UnsupportedHeavyOperationError
        If streamed delivery is unavailable or a coordinate block exceeds budget.
    MemoryBudgetExceededError
        If candidate work or the resident sparse result exceeds the RAM estimate.

    Notes
    -----
    Completed calculations retain an offline bibliography in
    parameters['attribution'], including results with zero observations.
    Optional Ackredit tracking contributes to the current application session.
    Reference implementations are distinguished from executed software;
    loading a stored analysis does not credit a new calculation.

    This reproduces supported reference cores, not whole package workflows:
    no occupancy aggregation, residue/solvent/sidechain pruning, water bridges,
    force-field energy or implicit coordinate construction. ProLIF recognition
    uses its original SMARTS. CPPTRAJ uses F/O/N elemental sites, MDTraj N/O.
    MDAnalysis retains its >0.10 nm lower D-A limit, but no partial-charge guesses.
    Explicit sites are caller declarations, recorded separately from automatic
    recognition. Undefined angles are skipped.

    Wernet–Nilsson follows MDTraj's implemented curve:
    D-A < distance_threshold - 0.000044 nm/degree**2 * (H-D-A in degrees)**2.
    Its source's additional comparison with the literal 45 is in radians and
    has no effect on defined angles; no extra 45-degree cutoff is invented.
    N/O generalization and water inclusion extend the original water criterion.
    Baker–Hubbard is evaluated per frame rather than using MDTraj's default
    frequency filter. CPPTRAJ source inequalities are inclusive despite the
    strict inequalities printed in its help text.

    Geometry at H uses donor-H then H-acceptor images. Wernet–Nilsson uses
    donor-H and donor-acceptor images. D-A methods reject incompatible H-centered
    and independently wrapped D-A geometry rather than storing misleading images.
    Numeric block work reserves one quarter of configure.max_ram_usage,
    candidate search one eighth and resident sparse accumulation one half.
    Caller-owned arrays, chemistry, Python overhead and process RSS are outside
    these estimates. Source chemistry is recognized once; no dense all-pairs
    matrix or per-occurrence Python object list is materialized.

    See Also
    --------
    molsysmt.physchem.get_hbond_sites
        Recognizing candidate sites independently of coordinates.
    molsysmt.interactions.hbonds.get_buch_hbonds
        Preserving the established Buch calculation and optional analysis output.
    molsysmt.Interactions.query
        Querying observations by source atoms and structures.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import pyunitwizard as puw
    >>> from rdkit import Chem
    >>> molsys = msm.convert(Chem.AddHs(Chem.MolFromSmiles('O')),
    ...     to_form='molsysmt.MolSys')
    >>> molsys.structures.append(coordinates=puw.quantity(
    ...     [[[0., 0., 0.], [.1, 0., 0.], [0., .1, 0.]]], 'nm'))
    >>> result = msm.interactions.hbonds.get_hbonds(
    ...     molsys, assume_complete_connectivity=True, pbc=False)
    >>> result.n_interactions, result.evaluated_structure_indices.tolist()
    (0, [0])

    .. admonition:: User guide

       See :ref:`Getting attributed hydrogen bonds <Tutorial_Get_hbonds>`.

    .. versionadded:: 1.0.0
    """
    from molsysmt import __version__, configure
    from molsysmt._private.execution.projected_geometry import (
        execute_projected_geometry,
    )
    from molsysmt._private.execution.sparse_accumulator import SparseColumnAccumulator
    from molsysmt._private.h5msm import modular_h5msm_dimensions
    from molsysmt._private.scientific_references import MDANALYSIS_REFERENCE
    from molsysmt.basic import convert, get
    from molsysmt.interactions.hbonds._reducer import _HBondReducer
    from molsysmt.interactions.result import Interactions
    from molsysmt.physchem import get_hbond_sites
    from molsysmt.topology._chemical_graph import (
        chemical_graph_context,
        select_chemical_atoms,
    )

    caller = "molsysmt.interactions.hbonds.get_hbonds"
    from molsysmt._private.interaction_methods import resolve_method

    method = resolve_method("hbonds", method, profile, caller=caller)["implementation"]
    if (selection_mode == "between") != (selection_2 is not None):
        raise ArgumentError("selection_2", caller=caller, message="Supply a second selection only for between searches.")
    explicit = donor_hydrogen_pairs is not None
    if explicit != (acceptor_atom_indices is not None) or (method == "mdanalysis_geometry" and not explicit):
        raise ArgumentError("donor_hydrogen_pairs", caller=caller, message="Supply both explicit site arrays together; MDAnalysis geometry requires them.")
    if method == "wernet_nilsson" and angle_threshold is not None:
        raise ArgumentError("angle_threshold", caller=caller, message="Wernet-Nilsson uses its distance-angle curve; leave angle_threshold None.")
    default_distance = {"baker_hubbard": .25, "wernet_nilsson": .33, "cpptraj": .3, "prolif": .35, "mdanalysis_geometry": .3}
    default_angle = {"baker_hubbard": 120., "cpptraj": 135., "prolif": 130., "mdanalysis_geometry": 150., "wernet_nilsson": 0.}
    distance = default_distance[method] if distance_threshold is None else np.asarray(puw.get_value(distance_threshold, to_unit="nm"))
    angle = np.deg2rad(default_angle[method]) if angle_threshold is None else np.asarray(puw.get_value(angle_threshold, to_unit="radians"))
    if np.shape(distance) != () or not np.isfinite(distance) or distance <= 0:
        raise ArgumentError("distance_threshold", caller=caller, message="Use a finite positive scalar length.")
    if np.shape(angle) != () or not np.isfinite(angle) or not 0 <= angle <= np.pi:
        raise ArgumentError("angle_threshold", caller=caller, message="Use a finite scalar angle between zero and pi radians.")
    distance, angle = float(distance), float(angle)
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
    source, states, _, state_index, _, covalent, selection_frames = chemical_graph_context(
        molecular_system, chemical_state, frames, assume_complete_connectivity, caller)
    if explicit:
        if np.any(donor_hydrogen_pairs >= n_atoms) or np.any(acceptor_atom_indices >= n_atoms):
            raise ArgumentError("donor_hydrogen_pairs", caller=caller, message="Explicit sites must use valid source atom indices.")
        symbols = np.asarray(get(source, element="atom", atom_type=True), dtype=object)
        pairs = np.sort(donor_hydrogen_pairs, axis=1)
        dtype = np.dtype([("a", np.int64), ("b", np.int64)])
        bonded = np.isin(np.ascontiguousarray(pairs).view(dtype).ravel(),
                         np.ascontiguousarray(np.sort(covalent, axis=1)).view(dtype).ravel())
        if (not bonded.all() or np.any(symbols[donor_hydrogen_pairs[:, 1]] != "H")
            or np.any(symbols[donor_hydrogen_pairs[:, 0]] == "H") or np.any(symbols[acceptor_atom_indices] == "H")):
            raise ArgumentError("donor_hydrogen_pairs", caller=caller, message="Declare covalently bonded heavy-atom/H pairs and non-hydrogen acceptors.")
        donors, acceptors = donor_hydrogen_pairs, acceptor_atom_indices
        sites = dict(method="explicit_sites", evidence="caller_declared_sites_and_covalent_hydrogens",
                     method_reference=MDANALYSIS_REFERENCE if method == "mdanalysis_geometry" else None,
                     software={"molsysmt": __version__}, smarts_patterns=None)
    else:
        site_method = {"baker_hubbard": "elemental_nitrogen_oxygen", "wernet_nilsson": "elemental_nitrogen_oxygen",
                       "cpptraj": "elemental_fluorine_oxygen_nitrogen", "prolif": "smarts_donor_acceptor"}[method]
        sites = get_hbond_sites(source, chemical_state=state_index, method=site_method,
                                assume_complete_connectivity=assume_complete_connectivity, max_matches=max_matches)
        donors, acceptors = sites["donor_hydrogen_pairs"], sites["acceptor_atom_indices"]
    first = select_chemical_atoms(source, states, state_index, selection, selection_frames, syntax)
    second = None if selection_2 is None else select_chemical_atoms(source, states, state_index, selection_2, selection_frames, syntax)
    if second is not None and np.intersect1d(first, second).size:
        raise ArgumentError("selection_2", caller=caller, message="Between selections must be disjoint.")
    if selection_mode != "incident":
        union = first if second is None else np.union1d(first, second)
        donors = donors[np.isin(donors, union).all(axis=1)]
        acceptors = acceptors[np.isin(acceptors, union)]
    donor_rows, acceptor_rows = np.arange(len(donors)), np.arange(len(acceptors))
    if selection_mode == "incident":
        in_first = np.isin(donors, first).any(axis=1)
        searches = [(donor_rows[in_first], acceptor_rows),
                    (donor_rows[~in_first], acceptor_rows[np.isin(acceptors, first)])]
    else:
        searches = [(donor_rows, acceptor_rows)]
    searches = [(d, a) for d, a in searches if len(d) and len(a)]
    universe = np.unique(np.concatenate((donors.ravel(), acceptors)))
    # Explicit sites change recognition, never the named geometric criterion.
    from molsysmt._private.scientific_references import (
        CPPTRAJ_REFERENCE,
        MDTRAJ_REFERENCE,
    )
    from molsysmt.physchem._prolif import PROLIF_REFERENCE
    references = dict(cpptraj=CPPTRAJ_REFERENCE, prolif=PROLIF_REFERENCE, mdanalysis_geometry=MDANALYSIS_REFERENCE,
                      baker_hubbard=MDTRAJ_REFERENCE, wernet_nilsson=MDTRAJ_REFERENCE)
    metadata = dict(n_atoms=n_atoms, n_structures=n_structures, evaluated_structure_indices=frames,
                    method=caller, software=sites["software"],
                    measure_units={"donor_hydrogen_distance": "nm", "donor_acceptor_distance": "nm",
                                   "hydrogen_acceptor_distance": "nm", "dha_angle": "radians", "hda_angle": "radians"},
                    evaluation_mode=selection_mode, evaluation_atom_indices=np.intersect1d(first, universe),
                    evaluation_atom_indices_b=None if second is None else np.intersect1d(second, universe),
                    evaluation_universe_indices=universe,
                    parameters=dict(method=method, method_reference=references[method], geometry_rule_version=method + "_hbond@1",
                                    site_definition=sites["method"], chemistry_evidence=sites["evidence"],
                                    smarts_patterns=sites["smarts_patterns"], max_matches=max_matches,
                                    distance_threshold={"value": distance, "unit": "nm"},
                                    angle_threshold=None if method == "wernet_nilsson" else {"value": angle, "unit": "radians"},
                                    curve_coefficient_nm_per_degree_squared=.000044 if method == "wernet_nilsson" else None,
                                    lower_da_distance_nm=.1 if method == "mdanalysis_geometry" else None,
                                    distance_reference="hydrogen_acceptor" if method == "baker_hubbard" else "donor_acceptor",
                                    angle_reference="hydrogen_donor_acceptor" if method == "wernet_nilsson" else "donor_hydrogen_acceptor",
                                    comparisons="inclusive" if method in {"cpptraj", "prolif"} else "strict_angle_inclusive_distance" if method == "mdanalysis_geometry" else "strict",
                                    chemical_state_index=state_index, assume_complete_connectivity=assume_complete_connectivity,
                                    recognition_scope="caller_declared_sites" if explicit else "full_source_chemical_state",
                                    pbc=pbc, pbc_policy="mic_when_box_available", hydrogen_policy="indexed_atoms_only",
                                    image_policy="donor_centered_mic" if method == "wernet_nilsson" else "donor_hydrogen_then_hydrogen_acceptor_mic",
                                    periodic_triangle_policy="reject_inconsistent_independent_da_image",
                                    water_policy="included", occupancy_policy="individual_frame_observations",
                                    adaptation="single_source_sparse_scopes_no_residue_solvent_frequency_pruning"))
    metadata["execution"] = {"memory_policy": "numeric_working_estimates@1"}
    if not len(frames) or not searches:
        metadata["execution"].update(execution="none", execution_chunks=0)
        result = Interactions.from_records([], **metadata)
    else:
        reducer = _HBondReducer(donors=donors, acceptors=acceptors, universe=universe, searches=searches,
                               first=first, second=second, method=method, distance=distance, angle=angle,
                               metadata=metadata, budget_bytes=configure.max_ram_usage)
        per_frame = 4 * 24 * len(universe) + 256 * (len(donors) + len(acceptors)) + 4096 + (288 if pbc else 0)
        result = execute_projected_geometry(coordinate_source, universe=universe, frames=frames, reducer=reducer,
                                           per_frame_bytes=per_frame, pbc=pbc, heavy_mode=heavy_mode, caller=caller)
    return result if output_type == "molsysmt.interactions" else convert(result, to_form="molsysmt.InteractionsDict")
