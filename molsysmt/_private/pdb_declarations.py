"""Resolving deposited PDB edges without guessing missing or conditional sites."""

from collections import defaultdict

import numpy as np


def resolve(content, canonical_atoms, variants):
    """Return explicit pairs and typed diagnostics on the first-model site axis.

    wwPDB PDB 3.3 sections 6 and 10 define the symbolic/serial endpoints.
    Alternate serials refer to canonical sites under the existing reader
    contract. Preserve that mapping and its conditional scope, without claiming
    a complete alternative chemical state. Symmetry images have no local atom
    counterpart and must not be projected onto the base-cell sites.
    """
    serial_sites = defaultdict(set)
    serial_locations = defaultdict(set)
    symbolic_sites = defaultdict(set)
    needs_serial = bool(content.conect)
    needs_symbolic = bool(content.links or content.ssbonds)
    site_variants = list(variants.values()) if needs_serial or needs_symbolic else []
    if needs_serial or needs_symbolic:
        for index, atom in enumerate(canonical_atoms):
            if needs_symbolic:
                symbolic_sites[
                    (
                        atom.chain_id,
                        atom.group_id,
                        atom.insertion_code,
                        atom.group_name,
                        atom.atom_name,
                    )
                ].add(index)
            if needs_serial:
                for variant in site_variants[index]:
                    serial_sites[variant.serial].add(index)
                    serial_locations[variant.serial].add(variant.alternate_location)

    rows = []
    pairs = set()
    redundant = False

    def add(
        record,
        kind,
        record_index,
        target_index,
        sources,
        targets,
        *,
        status=None,
        alternates=("", ""),
    ):
        nonlocal redundant
        endpoints = [sources, targets]
        indices = [
            next(iter(values)) if len(values) == 1 else -1 for values in endpoints
        ]
        if status is None:
            if any(len(values) > 1 for values in endpoints):
                status = "ambiguous_endpoint"
            elif any(not values for values in endpoints):
                status = "missing_endpoint"
            elif any(
                value not in {"", "1555"}
                for value in (
                    getattr(record, "symmetry1", ""),
                    getattr(record, "symmetry2", ""),
                )
            ):
                status = "unsupported_symmetry"
            elif any(
                alt
                and not any(
                    atom.alternate_location == alt for atom in site_variants[index]
                )
                for alt, index in zip(alternates, indices)
            ):
                status = "missing_alternate"
            elif indices[0] == indices[1]:
                status = "self_reference"
            else:
                status = "accepted"
        accepted = status == "accepted"
        conditional = accepted and any(
            len(site_variants[index]) > 1 for index in indices
        )
        pair = tuple(sorted(indices))
        if accepted:
            if pair in pairs:
                redundant = True
                status = "redundant"
            elif conditional:
                status = "conditional"
            pairs.add(pair)
        rows.append(
            dict(
                record_type=kind,
                record_index=record_index,
                target_index=target_index,
                line_number=record.line_number,
                record_text=record.record_text,
                atom_indices=indices,
                endpoint_match_counts=[len(sources), len(targets)],
                status=status,
                accepted=accepted,
                conditional=conditional,
                symmetry=(
                    getattr(record, "symmetry1", ""),
                    getattr(record, "symmetry2", ""),
                ),
                alternate_location=alternates,
            )
        )

    for index, record in enumerate(content.conect):
        if not record.target_serials:
            add(
                record,
                "CONECT",
                index,
                -1,
                serial_sites[record.source_serial],
                set(),
                status="missing_target",
            )
        for target_index, target in enumerate(record.target_serials):
            alternates = tuple(
                next(iter(serial_locations[serial]))
                if len(serial_locations[serial]) == 1
                else ""
                for serial in (record.source_serial, target)
            )
            add(
                record,
                "CONECT",
                index,
                target_index,
                serial_sites[record.source_serial],
                serial_sites[target],
                status="malformed_endpoint"
                if record.source_serial <= 0 or target <= 0
                else None,
                alternates=alternates,
            )

    for index, record in enumerate(content.links):
        add(
            record,
            "LINK",
            index,
            -1,
            symbolic_sites[record.endpoint1[:5]],
            symbolic_sites[record.endpoint2[:5]],
            alternates=(record.endpoint1[5], record.endpoint2[5]),
        )

    for index, record in enumerate(content.ssbonds):
        keys = [
            (*endpoint, "CYS", "SG")
            for endpoint in (record.endpoint1, record.endpoint2)
        ]
        malformed = bool(record.record_text) and any(
            record.record_text[start:stop].strip() != "CYS"
            for start, stop in [(11, 14), (25, 28)]
        )
        add(
            record,
            "SSBOND",
            index,
            -1,
            symbolic_sites[keys[0]],
            symbolic_sites[keys[1]],
            status="malformed_endpoint" if malformed else None,
        )

    # More than one declared sulfur partner is a conflict, not an invitation to
    # choose one by record order or distance. Preserve all literal declarations.
    sulfur_pairs = {
        pair
        for pair in pairs
        if all(
            canonical_atoms[index].group_name == "CYS"
            and canonical_atoms[index].atom_name == "SG"
            for index in pair
        )
    }
    sulfur_neighbors = defaultdict(set)
    for first, second in sulfur_pairs:
        sulfur_neighbors[first].add(second)
        sulfur_neighbors[second].add(first)
    conflicts = {
        pair
        for pair in sulfur_pairs
        if any(len(sulfur_neighbors[index]) > 1 for index in pair)
    }
    for row in rows:
        if row["accepted"] and tuple(sorted(row["atom_indices"])) in conflicts:
            row["status"] = "conflicting_disulfide_partners"
    rows.sort(key=lambda row: (row["line_number"], row["target_index"]))
    dtypes = dict(
        record_type="U6",
        record_index="int64",
        target_index="int64",
        line_number="int64",
        record_text="U80",
        atom_indices="int64",
        endpoint_match_counts="int64",
        status="U36",
        accepted="bool",
        conditional="bool",
        symmetry="U6",
        alternate_location="U1",
    )
    table = {
        name: np.asarray([row[name] for row in rows], dtype=dtype).reshape(
            (-1, 2)
            if name
            in {
                "atom_indices",
                "endpoint_match_counts",
                "symmetry",
                "alternate_location",
            }
            else (-1,)
        )
        for name, dtype in dtypes.items()
    }
    diagnostics = dict(
        schema="molsysmt.pdb_declarations@1",
        atom_index_scope="first_model_canonical_sites",
        unresolved=any(not row["accepted"] for row in rows),
        repeated_pairs=redundant,
        conditional_pairs=any(row["conditional"] for row in rows),
        conflicting_disulfide_partners=bool(conflicts),
        records=table,
        unassessed_checks=[
            "bond_orders",
            "bond_kinds",
            "valence",
            "symmetry_images",
            "alternate_specific_chemical_states",
        ],
        references=[
            "https://www.wwpdb.org/documentation/file-format-content/format33/sect6.html",
            "https://www.wwpdb.org/documentation/file-format-content/format33/sect10.html",
        ],
    )
    return sorted(pairs), diagnostics
