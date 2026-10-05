"""Generating bounded template candidates without assigning chemistry."""

from copy import deepcopy

import numpy as np
from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "build", "diagnostics"])
@arg_digest()
def get_covalent_bond_candidates(
    molecular_system,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    syntax="MolSysMT",
    skip_digestion=False,
):
    """Getting exact heavy-atom group-template covalent candidates.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form providing atom names, elements
        and group membership. PDB inputs are converted with inference disabled.
    selection : str, list, tuple or numpy.ndarray, default='all'
        Atom selection. Integer values are source atom indices. Whole containing
        groups are audited, but both endpoints of each candidate must be selected.
        Defaults to 'all'.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based). Choose one when structures exist; a topology
        without structures can also be assessed. Defaults to 'all'.
    chemical_state : str, int or None, default='reference'
        Stored state to inspect, or 'structure' for the selected structure's
        association. Ambiguous states remain unassessed. Defaults to 'reference'.
    syntax : str, default='MolSysMT'
        Syntax used for atom selection. Defaults to 'MolSysMT'.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    dict
        Detached ``molsysmt.covalent_bond_candidates@1`` report. Sorted source
        ``bonded_atom_pairs`` have shape (n_candidates, 2) and dtype int64;
        ``group_indices`` and ``missing_mask`` align with those rows. Each group
        retains template identity, source indices, exclusions and coverage.
        Missing means no stored edge has those endpoints; it does not certify
        existing edge types or chemistry. Producer versions are recorded at
        calculation time. Empty arrays retain their shapes and dtypes.

    Raises
    ------
    ArgumentError
        If selections or state/structure indices are invalid, or multiple
        structures are selected.
    NotWithThisFormError
        If required group hierarchy is unavailable.
    StructuralInconsistencyError
        If atom/group membership or domain correspondence is invalid.

    Notes
    -----
    The method ``exact_heavy_group_templates`` reuses the residue-coverage
    auditor and its exact amino-acid and curated modified-group templates.
    It never substitutes a sequence parent. Only unambiguous mapped heavy-atom
    edges are proposed. Missing heavy atoms can leave a partial candidate set;
    duplicate/unexpected names, unknown/conflicting heavy elements, unresolved
    states and contradictory stored intra-group chemistry block a group.
    Unsupported groups, including water, ions, lipids and arbitrary small
    molecules, remain explicit in this first bounded method.

    No geometry is used to propose bonds. Hydrogen edges, inter-group polymer
    links, disulfides, metal coordination, bond orders, protonation and valence
    certification are unassessed. Coordinates, existing chemical assignments
    and named interactions are unchanged. PDB parsing remains eager; native
    H5MSM 0.5 numeric/all coverage reads only the selected coordinate structure.

    See Also
    --------
    get_residue_chemical_coverage : Audit exact group-template coverage.
    get_missing_bonds : Obtain legacy template/geometric missing-pair lists.

    Examples
    --------
    >>> import molsysmt as msm
    >>> report = msm.build.get_covalent_bond_candidates(
    ...     msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'],
    ...     selection='group_index==1', structure_indices=0)
    >>> report['bonded_atom_pairs'].tolist()
    [[6, 8], [8, 10], [8, 14], [14, 15]]
    >>> report['missing_mask'].tolist()
    [False, False, False, False]

    .. admonition:: User guide

       See :ref:`Tutorial_Covalent_Bond_Candidates` for coverage and exclusions.

    .. versionadded:: 1.0.0
    """
    # Remove when the public ArgDigest floor includes uibcdf/argdigest#17.
    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(
            skip_digestion, caller="molsysmt.build.get_covalent_bond_candidates"
        )
    from molsysmt._private.covalent_candidates import prepare_source
    from molsysmt.basic import get
    from molsysmt.build import get_residue_chemical_coverage

    source_forms, source, selection_source, atoms = prepare_source(
        molecular_system,
        selection,
        structure_indices,
        chemical_state,
        syntax,
        "molsysmt.build.get_covalent_bond_candidates",
    )
    membership = get(
        selection_source,
        element="atom",
        selection=atoms,
        group_index=True,
        skip_digestion=True,
    )
    groups = sorted(set(index for index in membership if index is not None))
    coverage = get_residue_chemical_coverage(
        source,
        selection=groups,
        structure_indices=structure_indices,
        chemical_state=chemical_state,
        skip_digestion=True,
    )
    selected = set(atoms)
    readiness = coverage["chemical_readiness"]
    stored = {tuple(pair) for pair in readiness["bonded_atom_pairs"].tolist()}
    candidates = []
    reports = []
    for group in coverage["groups"]:
        heavy = group["heavy_atoms"]
        connectivity = group["connectivity"]
        hydrogen_atoms = set(group["hydrogens"]["observed_atom_indices"].tolist())
        reasons = []
        if group["template"] is None:
            reasons.append("no_exact_group_template")
        else:
            if (
                heavy["duplicate_atom_names"]
                or "ambiguous_atom_names" in group["reason_codes"]
            ):
                reasons.append("ambiguous_atom_names")
            if heavy["unexpected_atom_names"]:
                reasons.append("unexpected_heavy_atoms")
            for field, reason in (
                ("element_conflict_atom_indices", "heavy_element_conflict"),
                ("element_unassessed_atom_indices", "heavy_element_unassessed"),
            ):
                if set(heavy[field].tolist()) - hydrogen_atoms:
                    reasons.append(reason)
            if readiness["chemical_state_status"] != "resolved":
                reasons.append("chemical_state_" + readiness["chemical_state_status"])
            if connectivity.get("reason_code") in (
                "ambiguous_template_connectivity",
                "no_compatible_template_variant",
            ):
                reasons.append(connectivity["reason_code"])
            if (
                len(connectivity.get("unexpected_bond_indices", []))
                or len(connectivity.get("conflict_bond_type_indices", []))
                or len(
                    connectivity.get("bond_order", {}).get("conflict_bond_indices", [])
                )
                or "invalid_stored_bonds" in group["reason_codes"]
            ):
                reasons.append("conflicting_stored_chemistry")
        pairs = (
            []
            if reasons
            else [
                tuple(pair)
                for pair in connectivity["expected_bonded_atom_pairs"].tolist()
                if set(pair) <= selected
            ]
        )
        candidates.extend((pair, group["group_index"]) for pair in pairs)
        blocked = deepcopy(connectivity.get("blocked_by_missing_atom_name_pairs", []))
        reports.append(
            {
                "group_index": group["group_index"],
                "group_id": group["group_id"],
                "group_name": group["group_name"],
                "status": "unassessed"
                if reasons
                else "partial"
                if blocked
                else "assessed",
                "reason_codes": reasons,
                "atom_indices": group["atom_indices"].copy(),
                "template": deepcopy(group["template"]),
                "blocked_by_missing_atom_name_pairs": blocked,
                "n_candidates": len(pairs),
            }
        )
    candidates.sort()
    pairs = np.asarray([pair for pair, _ in candidates], dtype=np.int64).reshape(-1, 2)
    return {
        "schema": "molsysmt.covalent_bond_candidates@1",
        "method": "exact_heavy_group_templates",
        "rule_version": 1,
        "software": deepcopy(readiness["software"]),
        "source_forms": deepcopy(source_forms),
        "n_atoms": readiness["n_atoms"],
        "atom_indices": np.asarray(atoms, dtype=np.int64).copy(),
        "structure_index": readiness["structure_index"],
        "chemical_state_index": readiness["chemical_state_index"],
        "bonded_atom_pairs": pairs,
        "group_indices": np.asarray([group for _, group in candidates], dtype=np.int64),
        "missing_mask": np.asarray(
            [tuple(pair) not in stored for pair in pairs], dtype=bool
        ),
        "evidence": "inferred_candidate",
        "groups": reports,
        "coverage": coverage,
        "unassessed_checks": [
            "hydrogen_edges",
            "inter_group_links",
            "disulfides",
            "metal_coordination",
            "bond_orders",
            "protonation",
            "valence",
        ],
    }
