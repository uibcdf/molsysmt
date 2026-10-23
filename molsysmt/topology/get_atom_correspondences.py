"""Finding reusable atom correspondences constrained by declared chemical states."""

import numpy as np
from depdigest import dep_digest
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import (
    MemoryBudgetExceededError,
    UnsupportedHeavyOperationError,
)


@signal(tags=["api", "topology"])
@arg_digest()
@dep_digest("rdkit")
def get_atom_correspondences(
    molecular_system,
    selection="all",
    structure_indices="all",
    reference_molecular_system=None,
    reference_selection=None,
    reference_structure_indices="all",
    chemical_state="reference",
    reference_chemical_state="reference",
    method="declared_graph_isomorphism",
    max_matches=100000,
    syntax="MolSysMT",
    skip_digestion=False,
    *,
    fixed_atom_correspondence=None,
    candidate_atom_correspondences=None,
):
    """Finding chemically constrained bijections without using coordinates.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying a complete chemical graph and elements.
    selection : str, list, tuple or numpy.ndarray, default='all'
        Nonempty atom population to compare, within one covalent component.
        Its complete component supplies chemical context, including omitted H.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices for selection and fixed chemical-state resolution only.
    reference_molecular_system : molecular system or None, default=None
        Reference graph; None uses molecular_system.
    reference_selection : str, list, tuple, numpy.ndarray or None, default=None
        Reference population; None uses selection. Selection order is canonical.
    reference_structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Reference structure indices for selection and state resolution only.
    chemical_state : str or int, default='reference'
        Query state; 'structure' requires one state across requested structures.
    reference_chemical_state : str or int, default='reference'
        Reference state, resolved independently of the query.
    method : str, default='declared_graph_isomorphism'
        Exact declared-state profile, with no resonance or tautomer normalization.
    max_matches : int, default=100000
        Maximum complete-context candidate mappings before projection/filtering.
        Anchors prune before this cap. In supplied-map mode it bounds distinct
        proposed maps. Exceeding the bound raises; no truncated minimum is certified.
    syntax : str, default='MolSysMT'
        Selection syntax used for both molecular systems.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    fixed_atom_correspondence : list, tuple, numpy.ndarray or None, default=None
        Partial injective query/reference source-index pairs, shape (n_fixed, 2).
        Anchors may include unselected atoms in the complete covalent components.
        Matching enforces them during enumeration. None supplies no anchors.
    candidate_atom_correspondences : list, tuple, numpy.ndarray or None, default=None
        Complete selected-population maps, shape (n_maps, n_selected, 2), or
        one map of shape (n_selected, 2). Every map must extend to the declared
        chemical context and respect all anchors; an invalid map raises.
        None enumerates all chemical correspondences compatible with the anchors.

    Returns
    -------
    dict
        Detached int64 atom_correspondences of shape (n_matches, n_selected, 2),
        complete-context witnesses, source atom axes and selected populations,
        chemical states, graph digests, search completeness, software and
        bibliography. Column 0 is the query source index; column 1 is the
        reference source index. Zero matches retain defined shapes. No units
        apply. Equivalent projections are deduplicated and sorted lexically.
        search_scope distinguishes unrestricted, anchored and supplied-map sets;
        search_complete applies only to that declared scope. Constraints are
        detached and included in the consistency digest.

    Raises
    ------
    ArgumentError
        If anchors or proposed maps have invalid indices, duplicate endpoints,
        incomplete selected populations or conflicting declarations.
    StructuralInconsistencyError
        If required chemistry is missing, incomplete, changed by conversion,
        potentially stereogenic but unassigned, or outside the supported scope.
    UnsupportedHeavyOperationError
        If candidate enumeration exceeds max_matches.
    MemoryBudgetExceededError
        If the candidate working estimate exceeds configured RAM.

    Notes
    -----
    Positional atom/structure indices require plain integer values; quantity
    wrappers are rejected, including explicit dimensionless quantities.

    Experimental MolSysMT profile inspired by graph-isomorphism pose comparison
    in Bell and Zhang (2019) and Meli and Biggin (2020), not a faithful reproduction
    of DockRMSD or sPyRMSD. RDKit executes stereochemical substructure matching;
    MolSysMT additionally checks exact atom/bond labels and selection membership.
    Formal charge, isotope labels, radical counts, stored H counts and implicit-H
    policy, aromaticity, bond order and assigned tetrahedral/double-bond stereo
    are preserved. An absent isotope label denotes an unlabeled isotope.
    Dative/enhanced/non-tetrahedral stereo and resonance normalization are refused.
    Both sources require the same indexed-H representation and stored H policy;
    explicit/implicit H encodings are not normalized by this profile.
    Chemistry is never inferred from coordinates. Counts bound candidate output,
    not wall-clock time or total process RSS. Results may be reused after coordinate
    changes; chemistry, selected populations or axis changes invalidate reuse.
    Digests detect consistency changes and do not authenticate system identity.

    Assigned stereo uses RDKit's implementation of the Hanson et al. (2018) CIP
    algorithm, DOI 10.1021/acs.jcim.8b00324, through the shared stereo helper.
    This executed scientific criterion is credited separately from RMSD inspiration.

    See Also
    --------
    molsysmt.structure.get_symmetry_corrected_rmsd
        Evaluate admitted mappings without ligand superposition.
    get_substructure_matches
        Recognize uniquified SMARTS substructures.

    Examples
    --------
    >>> import molsysmt as msm
    >>> result = msm.topology.get_atom_correspondences('smiles:c1ccccc1')
    >>> result['atom_correspondences'].shape
    (12, 6, 2)
    >>> anchored = msm.topology.get_atom_correspondences(
    ...     'smiles:c1ccccc1', fixed_atom_correspondence=[[0, 0]])
    >>> anchored['atom_correspondences'].shape
    (2, 6, 2)
    >>> proposed = msm.topology.get_atom_correspondences(
    ...     'smiles:c1ccccc1',
    ...     candidate_atom_correspondences=result['atom_correspondences'][0])
    >>> proposed['search_scope']
    'supplied_atom_correspondences'

    .. admonition:: User guide

       See :ref:`Tutorial_Get_atom_correspondences`.

    .. versionadded:: 1.0.0
    """
    from rdkit import rdBase

    from molsysmt import __version__, configure
    from molsysmt._private.scientific_attribution import attach_graph_attribution

    from ._atom_correspondences import ChemicalGraph, correspondence_digest
    from ._correspondence_constraints import (
        candidate_witness,
        constrained_matches,
        prepare_constraints,
    )

    caller = "molsysmt.topology.get_atom_correspondences"
    reference = (
        molecular_system
        if reference_molecular_system is None
        else reference_molecular_system
    )
    reference_selection = (
        selection if reference_selection is None else reference_selection
    )
    first = ChemicalGraph(
        molecular_system, selection, structure_indices, chemical_state, syntax, caller
    )
    second = ChemicalGraph(
        reference,
        reference_selection,
        reference_structure_indices,
        reference_chemical_state,
        syntax,
        caller,
    )
    fixed, candidates = prepare_constraints(
        first, second, fixed_atom_correspondence, candidate_atom_correspondences, caller
    )
    width = len(first.atoms)
    budget = configure.max_ram_usage // 4
    # Include candidate tuples, projected keys, both output tables and packing.
    per_match = 256 + 192 * width
    bound = min(max_matches, budget // per_match)
    if bound < 1:
        raise MemoryBudgetExceededError(
            reason="One chemical correspondence exceeds the candidate working budget.",
            predicted_bytes=per_match,
            available_bytes=budget,
            caller=caller,
        )
    raw = (
        constrained_matches(first, second, fixed, bound + 1)
        if candidates is None
        else candidates
    )
    if len(raw) > bound:
        if bound < max_matches:
            raise MemoryBudgetExceededError(
                reason="Chemical correspondence enumeration exceeds the candidate working budget.",
                predicted_bytes=len(raw) * per_match,
                available_bytes=budget,
                caller=caller,
            )
        raise UnsupportedHeavyOperationError(
            operation=caller,
            form="chemical graph correspondences",
            reason="Candidate search exceeds max_matches; no partial result is returned.",
        )
    retained = {}
    if candidates is not None:
        for candidate in candidates:
            projected = tuple(candidate[:, 1])
            retained[projected] = candidate_witness(
                first, second, fixed, candidate, caller
            )
    else:
        for match in raw:
            if first.admits(second, match):
                projected = tuple(
                    second.atoms[np.asarray(match)[first.selected_positions]]
                )
                if projected not in retained or match < retained[projected]:
                    retained[projected] = match
    ordered = sorted(retained)
    count = len(ordered)
    selected_maps = np.empty((count, len(first.selected), 2), dtype=np.int64)
    context_maps = np.empty((count, width, 2), dtype=np.int64)
    for row, projected in enumerate(ordered):
        selected_maps[row, :, 0], selected_maps[row, :, 1] = first.selected, projected
        context_maps[row, :, 0] = first.atoms
        context_maps[row, :, 1] = second.atoms[np.asarray(retained[projected])]
    result = dict(
        schema="molsysmt.atom_correspondences@1",
        atom_correspondences=selected_maps,
        context_atom_correspondences=context_maps,
        selection_atom_indices=first.selected.copy(),
        reference_selection_atom_indices=second.selected.copy(),
        n_atoms=first.n_atoms,
        reference_n_atoms=second.n_atoms,
        chemical_state_index=first.state_index,
        reference_chemical_state_index=second.state_index,
        chemical_state_id=first.state_id,
        reference_chemical_state_id=second.state_id,
        source_graph_digest=first.digest,
        reference_graph_digest=second.digest,
        method=method,
        rule_version="declared_graph_isomorphism@1",
        search_complete=True,
        search_scope="supplied_atom_correspondences"
        if candidates is not None
        else "anchored_chemical_correspondences"
        if len(fixed)
        else "all_chemical_correspondences",
        fixed_atom_correspondence=fixed.copy(),
        candidate_atom_correspondences=None
        if candidates is None
        else candidates.copy(),
        n_candidate_matches=len(raw),
        max_matches=max_matches,
        evidence=dict(
            kind="declared_complete_covalent_graph",
            chemical_state_provenance_index=first.provenance_index,
            reference_chemical_state_provenance_index=second.provenance_index,
            cip_labeling=first.uses_cip or second.uses_cip,
        ),
        software=dict(molsysmt=__version__, rdkit=rdBase.rdkitVersion),
    )
    result["correspondence_digest"] = correspondence_digest(result)
    attach_graph_attribution(result, caller)
    return result
