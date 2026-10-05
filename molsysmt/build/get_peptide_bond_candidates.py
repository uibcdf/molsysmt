"""Reporting bounded peptide candidates on the original group and atom axes."""

from collections import defaultdict
from copy import deepcopy
from numbers import Integral

import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError


@signal(tags=["api", "build", "diagnostics"])
@arg_digest()
def get_peptide_bond_candidates(
    molecular_system,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    max_bond_length="2 angstroms",
    pbc=False,
    syntax="MolSysMT",
    skip_digestion=False,
):
    """Getting adjacent backbone C-N distance candidates without changing chemistry.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form with atom names, elements and
        group/chain membership. PDB normalization disables reader inference.
    selection : str, list, tuple or numpy.ndarray, default='all'
        Atom selection. Integers are source atom indices. Both endpoints must
        be selected; containing groups are audited. Defaults to 'all'.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Source structure indices (0-based). Select one when structures exist.
        Without coordinates, eligible links remain unassessed. Defaults to 'all'.
    chemical_state : str, int or None, default='reference'
        Stored state to audit, or 'structure' for the selected structure's
        association. Unresolved states block candidates. Defaults to 'reference'.
    max_bond_length : quantity or str, default='2 angstroms'
        Positive finite scalar distance ceiling with length units. The effective
        ceiling also obeys the existing protein C-N threshold plus tolerance
        (0.153 nm). Defaults to '2 angstroms'.
    pbc : bool, default=False
        Whether to use minimum-image distances when a valid box exists.
        Defaults to False; a crystallographic box does not imply a polymer link.
    syntax : str, default='MolSysMT'
        Syntax used for atom selection. Defaults to 'MolSysMT'.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    dict
        Detached ``molsysmt.peptide_bond_candidates@1`` report. Sorted source
        ``bonded_atom_pairs`` and directional ``group_pairs`` have shape (n, 2)
        and dtype int64. Carbon/nitrogen indices, missing masks and distance
        quantities align with candidate rows. ``links`` records reasons for
        rejection or unassessed links; ``group_coverage`` retains the supporting
        exact heavy-template report. Empty arrays retain shapes and dtypes.

    Raises
    ------
    ArgumentError
        If indices, state, flags or the length ceiling are invalid, or multiple
        structures are selected.
    NotWithThisFormError
        If required group hierarchy is unavailable.
    StructuralInconsistencyError
        If stored domains or coordinate shapes are inconsistent.

    Notes
    -----
    The descriptive method ``adjacent_backbone_distance`` reuses exact group
    audits and ``structure.get_distances(pairs=True)``. Only consecutive source
    group indices in one defined chain are considered. Group IDs are labels.
    Supported groups must have unambiguous mapped C/N endpoints, compatible
    heavy chemistry and positive finite distances within the effective ceiling.
    An outgoing C in a group with OXT is excluded. Alternate-site evidence at
    either endpoint blocks this first policy rather than mixing conformers.

    Native PDB conversion separates TER segments even when chain labels repeat
    and keeps insertion-code groups distinct. This tool respects those source
    indices; it cannot recover file evidence discarded by another adapter.
    Numeric/all H5MSM 0.5 queries read only one coordinate structure and its
    sparse alternate-site evidence. Rich selections may require broader access.

    Terminal caps, nonpeptide polymer links, sequence completion, hydrogen
    placement, bond orders, valence and protonation are unassessed. Existing
    edges, coordinates and named interactions are unchanged. A candidate is
    inferred evidence, never a declaration of complete or validated chemistry.

    See Also
    --------
    get_covalent_bond_candidates : Get exact heavy intra-group candidates.
    get_missing_bonds : Get legacy missing-pair lists.
    molsysmt.structure.get_distances : Compute distances between explicit pairs.

    Examples
    --------
    >>> import molsysmt as msm
    >>> report = msm.build.get_peptide_bond_candidates(
    ...     msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'],
    ...     structure_indices=0)
    >>> report['bonded_atom_pairs'].shape
    (0, 2)
    >>> report['method']
    'adjacent_backbone_distance'

    .. admonition:: User guide

       See :ref:`Tutorial_Peptide_Bond_Candidates` for scope and exclusions.

    .. versionadded:: 1.0.0
    """
    caller = "molsysmt.build.get_peptide_bond_candidates"
    # Remove when the public ArgDigest floor includes uibcdf/argdigest#17.
    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(skip_digestion, caller=caller)
    if not isinstance(pbc, bool) or max_bond_length is None:
        raise ArgumentError(
            "pbc" if not isinstance(pbc, bool) else "max_bond_length", caller=caller
        )
    values = np.asarray(puw.get_value(max_bond_length, to_unit="nm"))
    if values.ndim != 0 or not np.isfinite(values) or values <= 0:
        raise ArgumentError("max_bond_length", value=max_bond_length, caller=caller)
    from molsysmt._private.covalent_candidates import prepare_source, read_geometry
    from molsysmt.basic import get
    from molsysmt.build import get_covalent_bond_candidates
    from molsysmt.element.bond import bond_length_tolerance, max_expected_bond_length
    from molsysmt.native import Structures
    from molsysmt.structure import get_distances

    reference_ceiling = (
        max_expected_bond_length["protein"]["C"]["N"] + bond_length_tolerance
    )
    ceiling = min(float(values), float(puw.get_value(reference_ceiling, to_unit="nm")))
    source_forms, source, axis_source, atoms = prepare_source(
        molecular_system, selection, structure_indices, chemical_state, syntax, caller
    )
    group_coverage = get_covalent_bond_candidates(
        source,
        selection=atoms,
        structure_indices=structure_indices,
        chemical_state=chemical_state,
        skip_digestion=True,
    )
    frame = group_coverage["structure_index"]
    groups = group_coverage["groups"]
    audit = group_coverage["coverage"]
    readiness = audit["chemical_readiness"]
    indices = [group["group_index"] for group in groups]
    chain_values, atom_names = get(
        axis_source,
        element="group",
        selection=indices,
        chain_index=True,
        atom_name=True,
        skip_digestion=True,
    )
    chains = dict(zip(indices, chain_values))
    names = dict(zip(indices, atom_names))
    selected = set(atoms)
    stored = {tuple(sorted(pair)) for pair in readiness["bonded_atom_pairs"].tolist()}
    stored_rows = list(
        zip(
            readiness["bonded_atom_pairs"],
            readiness["fields"]["bond_type"]["values"],
            readiness["fields"]["bond_order"]["values"],
        )
    )
    incident_rows = defaultdict(list)
    for row, (pair, _, _) in enumerate(stored_rows):
        for atom in pair:
            incident_rows[int(atom)].append(row)
    links = []
    eligible = []
    for left, right in zip(groups, groups[1:]):
        g, h = left["group_index"], right["group_index"]
        reasons = []
        if h != g + 1:
            reasons.append("nonconsecutive_source_groups")
        if not all(isinstance(chains[x], Integral) and chains[x] >= 0 for x in (g, h)):
            reasons.append("missing_or_ambiguous_chain")
        elif chains[g] != chains[h]:
            reasons.append("different_source_chains")
        if any(group["status"] == "unassessed" for group in (left, right)):
            reasons.append("group_template_unassessed")
        endpoints = []
        for group, role in ((left, "C"), (right, "N")):
            matches = [
                int(atom)
                for atom, name in zip(
                    group["atom_indices"], names[group["group_index"]]
                )
                if name == role
            ]
            endpoints.append(matches[0] if len(matches) == 1 else None)
        if any(atom is None for atom in endpoints):
            reasons.append("missing_or_ambiguous_backbone_endpoint")
        elif not set(endpoints) <= selected:
            reasons.append("endpoints_outside_selection")
        if all(atom is not None for atom in endpoints):
            expected_pair = tuple(sorted(endpoints))
            endpoint_rows = set().union(*(incident_rows[atom] for atom in endpoints))
            for row in sorted(endpoint_rows):
                pair, kind, order = stored_rows[row]
                stored_pair = tuple(sorted(pair.tolist()))
                if stored_pair == expected_pair:
                    if (kind is not None and kind != "covalent") or (
                        order is not None and order != 1
                    ):
                        reasons.append("conflicting_stored_peptide_edge")
                elif kind == "covalent" and any(
                    endpoint in pair and not set(pair) <= set(group["atom_indices"])
                    for endpoint, group in zip(endpoints, (left, right))
                ):
                    reasons.append("backbone_endpoint_already_linked")
            reasons = list(dict.fromkeys(reasons))
        if "OXT" in names[g]:
            reasons.append("outgoing_terminal_carboxyl_oxygen")
        link = {
            "group_pair": [g, h],
            "carbon_atom_index": endpoints[0],
            "nitrogen_atom_index": endpoints[1],
            "status": "unassessed",
            "reason_codes": reasons,
            "distance": None,
        }
        links.append(link)
        if not reasons:
            eligible.append(link)
    geometry = None
    endpoint_atoms = sorted(
        {
            atom
            for link in eligible
            for atom in (link["carbon_atom_index"], link["nitrogen_atom_index"])
        }
    )
    if eligible and frame is not None:
        geometry = read_geometry(source, endpoint_atoms, frame)
    pbc_applied = False
    if eligible and (geometry is None or geometry["coordinates"] is None):
        for link in eligible:
            link["reason_codes"].append("coordinates_unavailable")
        eligible = []
    if eligible:
        alternates = geometry["alternate_location"]
        unsupported_alternates = alternates is not None and not isinstance(
            alternates[0], dict
        )
        alternate_atoms = (
            set()
            if alternates is None or unsupported_alternates
            else set(alternates[0])
        )
        finite = set(readiness["fields"]["coordinates"]["present_indices"].tolist())
        for link in eligible:
            endpoints = {link["carbon_atom_index"], link["nitrogen_atom_index"]}
            if unsupported_alternates:
                link["reason_codes"].append("unsupported_alternate_site_evidence")
            if endpoints & alternate_atoms:
                link["reason_codes"].append("alternate_backbone_endpoint")
            if not endpoints <= finite:
                link["reason_codes"].append("nonfinite_or_missing_endpoint_coordinates")
        eligible = [link for link in eligible if not link["reason_codes"]]
        pbc_applied = bool(eligible and pbc and geometry["box"] is not None)
        if pbc_applied:
            box = puw.get_value(geometry["box"], to_unit="nm")
            if (
                box.shape != (1, 3, 3)
                or not np.isfinite(box).all()
                or np.linalg.det(box[0]) <= 0
            ):
                for link in eligible:
                    link["reason_codes"].append("invalid_periodic_box")
                eligible = []
                pbc_applied = False
    candidates = []
    if eligible:
        local = {atom: index for index, atom in enumerate(endpoint_atoms)}
        coordinate_source = Structures(
            coordinates=geometry["coordinates"],
            box=geometry["box"] if pbc_applied else None,
        )
        distances = get_distances(
            coordinate_source,
            selection=[local[link["carbon_atom_index"]] for link in eligible],
            selection_2=[local[link["nitrogen_atom_index"]] for link in eligible],
            structure_indices=[0],
            pairs=True,
            pbc=pbc_applied,
            skip_digestion=True,
        )
        for link, distance in zip(eligible, puw.get_value(distances, to_unit="nm")[0]):
            link["distance"] = puw.standardize(puw.quantity(float(distance), "nm"))
            if not np.isfinite(distance) or distance <= 0:
                link["reason_codes"].append("nonpositive_or_nonfinite_distance")
            elif distance > ceiling:
                link["status"] = "rejected"
                link["reason_codes"].append("distance_exceeds_ceiling")
            else:
                link["status"] = "candidate"
                candidates.append(link)
    candidates.sort(
        key=lambda link: sorted(
            (link["carbon_atom_index"], link["nitrogen_atom_index"])
        )
    )
    pairs = np.asarray(
        [
            sorted((link["carbon_atom_index"], link["nitrogen_atom_index"]))
            for link in candidates
        ],
        dtype=np.int64,
    ).reshape(-1, 2)
    return {
        "schema": "molsysmt.peptide_bond_candidates@1",
        "method": "adjacent_backbone_distance",
        "rule_version": 1,
        "software": deepcopy(group_coverage["software"]),
        "source_forms": deepcopy(source_forms),
        "n_atoms": group_coverage["n_atoms"],
        "atom_indices": group_coverage["atom_indices"].copy(),
        "structure_index": frame,
        "chemical_state_index": group_coverage["chemical_state_index"],
        "bonded_atom_pairs": pairs,
        "group_pairs": np.asarray(
            [link["group_pair"] for link in candidates], dtype=np.int64
        ).reshape(-1, 2),
        "carbon_atom_indices": np.asarray(
            [link["carbon_atom_index"] for link in candidates], dtype=np.int64
        ),
        "nitrogen_atom_indices": np.asarray(
            [link["nitrogen_atom_index"] for link in candidates], dtype=np.int64
        ),
        "missing_mask": np.asarray(
            [tuple(pair) not in stored for pair in pairs], dtype=bool
        ),
        "distances": puw.standardize(
            puw.quantity(
                np.asarray(
                    [
                        puw.get_value(link["distance"], to_unit="nm")
                        for link in candidates
                    ],
                    dtype=float,
                ),
                "nm",
            )
        ),
        "evidence": "inferred_candidate",
        "links": links,
        "group_coverage": group_coverage,
        "parameters": {
            "max_bond_length": puw.quantity(float(values), "nm"),
            "effective_max_bond_length": puw.quantity(ceiling, "nm"),
            "pbc": pbc,
        },
        "pbc_applied": pbc_applied,
        "unassessed_checks": [
            "terminal_caps",
            "nonpeptide_polymer_links",
            "sequence_completion",
            "hydrogen_edges",
            "bond_orders",
            "valence",
            "protonation",
        ],
    }
