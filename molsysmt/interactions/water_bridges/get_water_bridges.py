"""Compose indexed one- or two-water paths from attributed hydrogen bonds."""

from copy import deepcopy

import numpy as np
from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.interaction_attribution import attributed
from molsysmt._private.interaction_methods import resolve_method
from molsysmt._private.smonitor import (
    ArgumentError,
    StructuralInconsistencyError,
    UnsupportedHeavyOperationError,
)
from molsysmt._private.variables import is_all


@signal(tags=["api", "interactions"])
@arg_digest()
@dep_digest("rdkit")
@attributed("water_bridges")
def get_water_bridges(
    molecular_system,
    selection="all",
    selection_2=None,
    structure_indices="all",
    chemical_state="reference",
    method="hbond_water_path",
    distance_threshold=None,
    angle_threshold=None,
    selection_mode="internal",
    pbc=True,
    assume_complete_connectivity=False,
    output_type="molsysmt.Interactions",
    syntax="MolSysMT",
    skip_digestion=False,
    *,
    hbond_method="baker_hubbard",
    hbond_profile=None,
    max_matches=100000,
    heavy_mode="auto",
    profile=None,
    order=1,
):
    """Observing simultaneous hydrogen bonds through one or two indexed waters.

    Return an independent analysis; attachment to a molecular system is explicit.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying coordinates and complete declared chemistry:
        elements, covalent orders, formal charges and atom/bond aromatic flags.
        Waters require two explicitly indexed hydrogens.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Source atom selection. All-participant scope includes mediator atoms and
        hydrogens actually used by the observed legs.
    selection_2 : str, list, tuple, numpy.ndarray, or None, default=None
        Disjoint second selection, required only for between mode. Mediator atoms
        must be in the union for between mode; use incident for endpoint-only sets.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based). Evaluate repeated indices once, sorted.
        Frames without bridges retain explicit evaluated coverage.
    chemical_state : {'reference', 'structure'}, int, or None, default='reference'
        State supplying waters and leg sites. Requested frames must resolve one state.
    method : str, default='hbond_water_path'
        Simple paths of observed D-H-A legs through the requested water order.
        The previous two_hbonds_one_water selector remains available for order one.
    distance_threshold : quantity, str, or None, default=None
        Positive scalar length cutoff passed to the leg detector. None uses its
        named scientific default: H-A <0.25 nm for Baker-Hubbard, for example.
    angle_threshold : quantity, str, or None, default=None
        Angular minimum passed to the leg detector. None uses its scientific
        default; leave None for the Wernet-Nilsson distance-angle curve.
    selection_mode : {'internal', 'incident', 'between'}, default='internal'
        All participating atoms in selection, any in selection, or all in the
        union of disjoint selections with at least one in each, respectively.
        These are atom scopes, not implicit ligand/protein endpoint selections.
    pbc : bool, default=True
        Preserve observed leg MIC images when a valid box exists. Translate the
        next leg onto its shared water oxygen image, keeping every geometry.
    assume_complete_connectivity : bool, default=False
        Record a completeness assumption without repairing chemical assignments.
    output_type : str, default='molsysmt.Interactions'
        Sparse molsysmt.Interactions or typed molsysmt.InteractionsDict.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate selection and selection_2.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    hbond_method : str, default='baker_hubbard'
        Keyword-only criterion for every leg: baker_hubbard, wernet_nilsson, or
        donor_acceptor_distance_angle with an automatic chemical site profile.
    hbond_profile : str or None, default=None
        Keyword-only recognition/geometry profile passed to get_hbonds. None
        selects the leg method's default. explicit_sites is unavailable here.
    max_matches : int, default=100000
        Keyword-only maximum full-source matches per water or leg SMARTS query.
    heavy_mode : {'auto', 'force', 'off'}, default='auto'
        Keyword-only leg-coordinate execution policy. Eligible native/H5MSM inputs
        stream projected coordinates. Accepted legs and bridges remain in RAM.
    profile : str or None, default=None
        Keyword-only indexed_water profile. None selects this profile.
    order : int, default=1
        Keyword-only exact number of distinct mediator waters: one or two.
        Two waters require three simultaneous legs. This is not a maximum order;
        store separate named analyses to retain both one- and two-water paths.

    Returns
    -------
    molsysmt.Interactions or molsysmt.InteractionsDict
        Relations of type water_bridge, six or nine singleton roles in D-H-A triples:
        leg_1_donor, leg_1_hydrogen, leg_1_acceptor, leg_2_donor,
        leg_2_hydrogen, leg_2_acceptor, plus leg_3 roles for order two. Each mediator
        oxygen repeats in its adjacent legs;
        each role retains its own observed image. Measures prefixed ``leg_1_`` and
        ``leg_2_`` (and ``leg_3_`` for order two) retain nm or radians. Scope, frames, reference/producer provenance,
        and the complete attributed leg parameters accompany the result.

    Raises
    ------
    ArgumentError
        If units, methods, profiles, state, indices or selections are invalid.
    StructuralInconsistencyError
        If chemistry/geometry is unavailable or joined shared images conflict.
    UnsupportedHeavyOperationError
        If forced streaming is unsupported or a chemical match cap is exceeded.
    MemoryBudgetExceededError
        If numerical graphs, leg/bridge output or join estimates exceed budget.

    Notes
    -----
    The path construction follows the water-mediated hydrogen-bond path concept
    used by ProLIF WaterBridge and MDAnalysis WaterBridgeAnalysis, adapted to
    atom-level observations rather than residue fingerprints. Leg science is
    explicitly chosen and attributed; the default uses Baker-Hubbard criteria,
    not ProLIF's default thresholds. No global parity with either application's
    pruning, networks, force-field typing or aggregation is claimed.

    Join only simultaneous legs with distinct nonwater endpoint heavy atoms.
    The water can donate both legs, accept both, or donate one and accept one.
    Different donor hydrogens are different observations, including bifurcated
    hydrogen bonds; neither branch direction nor hydrogen roles are discarded.
    Order legs along the path starting from the lower external heavy-atom index,
    preserving each directed D-H-A tuple. An undirected path appears once per
    exact leg sequence and frame. Order two requires two distinct water oxygens
    and their observed connecting leg; cycles and repeated endpoint atoms are excluded.
    All returned participants are actual leg atoms; an unused water hydrogen
    is not an additional participant. Internal queries and atom removal use
    those participants. Neutral explicit waters are recognized by chemical
    graph, not residue name. Paths through more than two waters, implicit
    hydrogens, energies and global frequency pruning are excluded.

    No dense atom-pair or trajectory tensor is allocated. Leg coordinates use
    the existing projected executor. Numeric resident leg columns, join arrays
    and sparse bridge packing are checked against the configured budget; source
    chemistry, Python overhead and process RSS are not fully modeled. All
    accepted leg and bridge output must fit in RAM; this is not a streaming writer.

    See Also
    --------
    molsysmt.physchem.get_water_sites
        Recognizing explicitly indexed neutral water molecules without geometry.
    molsysmt.interactions.hbonds.get_hbonds
        Applying the attributed scientific criterion for each branch.
    molsysmt.Interactions.query
        Querying all-participant sparse observations by atoms and structures.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from rdkit import Chem
    >>> molsys = msm.convert(Chem.AddHs(Chem.MolFromSmiles('O')), to_form='molsysmt.MolSys')
    >>> molsys.structures.append(coordinates=msm.pyunitwizard.quantity([[[0,0,0],[0.1,0,0],[0,0.1,0]]], 'nm'))
    >>> result = msm.interactions.water_bridges.get_water_bridges(molsys, pbc=False)
    >>> result.n_interactions, result.evaluated_structure_indices.tolist()
    (0, [0])

    .. admonition:: User guide

       See :ref:`Getting water bridges <Tutorial_Get_water_bridges>`.

    .. versionadded:: 1.0.0
    """
    from molsysmt import configure
    from molsysmt._private.execution.sparse_accumulator import SparseColumnAccumulator
    from molsysmt._private.h5msm import modular_h5msm_dimensions
    from molsysmt.basic import convert, get
    from molsysmt.interactions.hbonds import get_hbonds
    from molsysmt.physchem import get_water_sites
    from molsysmt.physchem._prolif import PROLIF_REFERENCE
    from molsysmt.topology._chemical_graph import (
        chemical_graph_context,
        select_chemical_atoms,
    )

    from ._join import join_water_legs

    caller = "molsysmt.interactions.water_bridges.get_water_bridges"
    if method == "two_hbonds_one_water" and order != 1:
        raise ArgumentError(
            "order",
            caller=caller,
            message="two_hbonds_one_water requires order=1; use hbond_water_path for order=2.",
        )
    leg_definition = resolve_method(
        "hbonds", hbond_method, hbond_profile, caller=caller
    )
    if leg_definition["implementation"] == "mdanalysis_geometry":
        raise ArgumentError(
            "hbond_profile",
            caller=caller,
            message="Water bridges require automatic leg site recognition.",
        )
    if (selection_mode == "between") != (selection_2 is not None):
        raise ArgumentError(
            "selection_2",
            caller=caller,
            message="Supply a second selection only for between searches.",
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
    waters = get_water_sites(
        source,
        chemical_state=state_index,
        assume_complete_connectivity=assume_complete_connectivity,
        max_matches=max_matches,
    )
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
    oxygen = waters["water_atom_indices"][:, 0]
    if selection_mode != "incident":
        oxygen = np.intersect1d(
            oxygen, first if second is None else np.union1d(first, second)
        )
    # Keep validation at the leg public boundary: thresholds and resolved source
    # form have not yet been normalized to that callee's full contract.
    legs = get_hbonds(
        coordinate_source,
        selection=oxygen,
        selection_mode="incident",
        structure_indices=frames,
        chemical_state=state_index,
        method=hbond_method,
        profile=hbond_profile,
        distance_threshold=distance_threshold,
        angle_threshold=angle_threshold,
        pbc=pbc,
        assume_complete_connectivity=assume_complete_connectivity,
        max_matches=max_matches,
        heavy_mode=heavy_mode,
    )
    reference = dict(PROLIF_REFERENCE)
    reference["implementation"] = reference["implementation"].replace(
        "interactions.py", "water_bridge.py"
    )
    universe = legs.evaluation_universe_indices
    metadata = dict(
        n_atoms=n_atoms,
        n_structures=n_structures,
        evaluated_structure_indices=frames,
        method=caller,
        software={**waters["software"], **legs.software},
        measure_units={
            f"leg_{branch}_{name}": unit
            for branch in range(1, order + 2)
            for name, unit in legs.measure_units.items()
        },
        evaluation_mode=selection_mode,
        evaluation_atom_indices=np.intersect1d(first, universe),
        evaluation_atom_indices_b=None
        if second is None
        else np.intersect1d(second, universe),
        evaluation_universe_indices=universe,
        parameters=dict(
            method=method,
            method_reference=reference,
            geometry_rule_version=f"hbond_water_path_order_{order}@1",
            hbond_method=leg_definition["method"],
            hbond_profile=leg_definition["profile"],
            hbond_parameters=deepcopy(legs.parameters),
            water_definition=waters["method"],
            water_smarts=waters["smarts_patterns"],
            chemistry_evidence=waters["evidence"],
            scientific_references=[leg_definition["method"]]
            if leg_definition["method"] in {"baker_hubbard", "wernet_nilsson"}
            else [],
            chemical_state_index=state_index,
            max_matches=max_matches,
            assume_complete_connectivity=assume_complete_connectivity,
            pbc=pbc,
            branch_identity="distinct_external_heavy_atom_then_directed_dha",
            selection_policy="all_actual_leg_participants",
            mediator_order=order,
            hydrogen_policy="indexed_atoms_only",
            image_policy="align_shared_water_oxygen_then_anchor_first_role",
        ),
    )
    leg_execution = (
        legs.execution_records[0]["details"] if legs.execution_records else {}
    )
    metadata["execution"] = {
        **leg_execution,
        "hbond_execution": leg_execution,
        "memory_policy": "resident_legs_and_sparse_join_numeric_estimates@1",
    }
    result = join_water_legs(
        legs,
        all_water_oxygen=waters["water_atom_indices"][:, 0],
        first=first,
        second=second,
        metadata=metadata,
        budget_bytes=configure.max_ram_usage,
    )
    return (
        result
        if output_type == "molsysmt.interactions"
        else convert(result, to_form="molsysmt.InteractionsDict")
    )
