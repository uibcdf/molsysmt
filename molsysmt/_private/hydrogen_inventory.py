"""Auditing stored virtual H counts separately from indexed hydrogen neighbors."""

import numpy as np

from molsysmt._private.chemical_readiness import _assess_from_domains, _domains


def inventory(
    molecular_system, selection, structure_indices, chemical_state, syntax, caller
):
    from molsysmt._private.variables import is_all
    from molsysmt.basic import select

    domains = _domains(molecular_system, caller)
    audit = _assess_from_domains(
        molecular_system,
        "all",
        structure_indices,
        chemical_state,
        syntax,
        caller,
        domains,
    )
    n_atoms = audit["n_atoms"]
    indices = np.arange(n_atoms, dtype=np.int64)
    if selection is not None and not is_all(selection):
        indices = np.asarray(
            select(
                molecular_system,
                selection=selection,
                structure_indices=structure_indices,
                chemical_state=chemical_state,
                syntax=syntax,
            ),
            dtype=np.int64,
        )
        indices = np.unique(indices)
    symbols = audit["fields"]["atom_type"]["values"]
    pairs = audit["bonded_atom_pairs"]
    issues = []

    def issue(reason, index=None):
        issues.append(
            {
                "reason_code": reason,
                "atom_index": index,
                "diagnostic_code": "MSM-ERR-STRUCT-003",
            }
        )

    if audit["chemical_state_status"] != "resolved":
        issue("unresolved_chemical_state")
    if audit["connectivity"]["declared_completeness"] != "complete":
        issue("incomplete_connectivity")
    invalid = audit["connectivity"]["invalid_bond_indices"]
    state_index = audit["chemical_state_index"]
    if domains[2] is not None and state_index is not None:
        raw = domains[2]._states[state_index].bonds[["atom1_index", "atom2_index"]]
        if any(
            isinstance(value, (bool, np.bool_))
            or not isinstance(value, (int, np.integer))
            for value in raw.to_numpy(dtype=object).flat
        ):
            invalid = np.arange(len(raw), dtype=np.int64)
    if len(invalid):
        issue("invalid_connectivity")
    virtual = np.full(n_atoms, -1, dtype=np.int64)
    selected = np.zeros(n_atoms, dtype=bool)
    selected[indices] = True
    implicit = audit["fields"]["n_implicit_hydrogens"]["values"]
    explicit = audit["fields"]["n_explicit_hydrogens"]["values"]
    for i, (a, b) in enumerate(zip(implicit, explicit)):
        if a is None or b is None:
            if selected[i]:
                issue("missing_stored_hydrogen_counts", i)
        elif (
            not isinstance(a, (int, np.integer))
            or isinstance(a, (bool, np.bool_))
            or not isinstance(b, (int, np.integer))
            or isinstance(b, (bool, np.bool_))
            or a < 0
            or b < 0
        ):
            issue("invalid_stored_hydrogen_counts", i)
        else:
            virtual[i] = int(a) + int(b)
    observed = np.zeros(n_atoms, dtype=np.int64)
    parent_pairs = []
    hydrogen = np.asarray(symbols == "H", dtype=bool)
    degrees = np.zeros(n_atoms, dtype=np.int64)
    if not len(invalid):
        kinds = audit["fields"]["bond_type"]["values"]
        for k, (a, b) in enumerate(pairs):
            if kinds[k] != "covalent":
                issue("unsupported_relationship")
                continue
            degrees[[a, b]] += 1
            if hydrogen[a] != hydrogen[b]:
                parent, h = (b, a) if hydrogen[a] else (a, b)
                observed[parent] += 1
                parent_pairs.append((parent, h))
            elif hydrogen[a]:
                issue("hydrogen_to_hydrogen_relationship", int(a))
        for h in np.flatnonzero(hydrogen):
            if degrees[h] != 1 or virtual[h] > 0:
                issue("invalid_indexed_hydrogen", int(h))
    if any(value is None for value in symbols):
        issue("missing_elements")
    elif audit["fields"]["atom_type"]["status"] != "present":
        issue("unsupported_elements")
    parent_pairs = np.asarray(parent_pairs, dtype=np.int64).reshape(-1, 2)
    if len(parent_pairs):
        parent_pairs = parent_pairs[np.isin(parent_pairs[:, 0], indices)]
    conflict = any(
        entry["reason_code"]
        in {
            "invalid_connectivity",
            "invalid_stored_hydrogen_counts",
            "invalid_indexed_hydrogen",
            "hydrogen_to_hydrogen_relationship",
        }
        for entry in issues
    )
    return dict(
        schema="molsysmt.hydrogen_inventory@1",
        method="stored_hydrogen_inventory",
        atom_indices=indices,
        chemical_state_index=audit["chemical_state_index"],
        structure_index=audit["structure_index"],
        status="empty"
        if not len(indices)
        else "conflict"
        if conflict
        else "unassessed"
        if issues
        else "available",
        indexed_hydrogen_counts=observed[indices],
        missing_hydrogen_counts=virtual[indices],
        total_hydrogen_counts=np.where(
            virtual[indices] >= 0, observed[indices] + virtual[indices], -1
        ),
        parent_hydrogen_pairs=parent_pairs,
        explicit_hydrogen_atom_indices=indices[hydrogen[indices]],
        issues=issues,
        count_convention="Stored implicit/explicit counts exclude indexed H neighbors; -1 is unknown.",
        unassessed_checks=["valence", "protonation", "coordinate_quality"],
        software=audit["software"],
    )
