"""Construct detached native templates from explicitly acquired CCD chemistry."""

import re
from copy import deepcopy
from importlib.metadata import version

import numpy as np
import pandas as pd

from molsysmt._private.ccd_reference import CALLER, read_definition
from molsysmt._private.smonitor import FileContentError, StructuralInconsistencyError


def value(table, field, row=0):
    if table is None or not table.hasAttribute(field):
        return None
    result = table.getValue(field, row)
    return None if result in {None, "", ".", "?"} else result


def _integer(raw, field):
    if raw is None:
        return None
    if not isinstance(raw, str) or re.fullmatch(r"[+-]?[0-9]+", raw) is None:
        raise FileContentError(
            f"CCD {field} must be an integer or unknown", caller=CALLER
        )
    try:
        return int(raw)
    except (ValueError, TypeError) as error:
        raise FileContentError(
            f"CCD {field} must be an integer or unknown", caller=CALLER
        ) from error


def _flag(raw, field):
    if raw is None:
        return None
    if raw.upper() not in {"Y", "N"}:
        raise FileContentError(f"Unsupported CCD {field} flag {raw!r}", caller=CALLER)
    return raw.upper() == "Y"


def _issue(issues, reason, *, axis=None, index=None, field=None, status="unassessed"):
    issues.append(
        dict(reason=reason, axis=axis, index=index, field=field, status=status)
    )


def _tables(block, component_id, issues):
    from molsysmt.element.atom import is_atom_type, normalize_atom_types
    from molsysmt.native._chemical_state import _ChemicalStateStorage

    atom_table = block.getObj("chem_comp_atom")
    bond_table = block.getObj("chem_comp_bond")
    if atom_table is None or atom_table.getRowCount() == 0:
        raise FileContentError("A nonempty CCD atom table is required", caller=CALLER)
    names = [value(atom_table, "atom_id", i) for i in range(atom_table.getRowCount())]
    if None in names or len(set(names)) != len(names):
        raise FileContentError("CCD atom IDs must be present and unique", caller=CALLER)
    source_types = [value(atom_table, "type_symbol", i) for i in range(len(names))]
    symbols = [
        symbol[0].upper() + symbol[1:].lower() if symbol else ""
        for symbol in source_types
    ]
    known = np.asarray(is_atom_type(symbols)) | np.asarray(
        [symbol in {"D", "T"} for symbol in symbols]
    )
    normalized, isotopes = normalize_atom_types(
        [symbol for symbol, ok in zip(symbols, known) if ok]
    )
    normalized = iter(zip(normalized, isotopes))
    atoms = []
    for index, name in enumerate(names):
        declared_id = value(atom_table, "comp_id", index)
        if (
            declared_id is not None
            and declared_id.casefold() != component_id.casefold()
        ):
            raise FileContentError(
                "A CCD atom belongs to another component", caller=CALLER
            )
        symbol, isotope = next(normalized) if known[index] else (None, None)
        atom = dict(
            name=name,
            symbol=symbol,
            isotope=isotope,
            charge=_integer(value(atom_table, "charge", index), "atom charge"),
            aromatic=_flag(
                value(atom_table, "pdbx_aromatic_flag", index), "atom aromatic"
            ),
            stereo=value(atom_table, "pdbx_stereo_config", index),
            ordinal=value(atom_table, "pdbx_ordinal", index),
        )
        if atom["stereo"] is not None:
            atom["stereo"] = atom["stereo"].upper()
        if atom["stereo"] not in {None, "N", "R", "S"}:
            raise FileContentError(
                "Unsupported CCD atom stereo declaration", caller=CALLER
            )
        for field in ("symbol", "charge", "aromatic"):
            if atom[field] is None:
                _issue(
                    issues,
                    "missing_atom_declaration",
                    axis="atom",
                    index=index,
                    field=field,
                )
        atoms.append(atom)
    try:
        _ChemicalStateStorage._coerce_atom_attribute(
            "formal_charge", [atom["charge"] for atom in atoms]
        )
    except StructuralInconsistencyError as error:
        raise FileContentError(
            "CCD formal charge cannot be represented by native ChemicalStates",
            caller=CALLER,
        ) from error
    declared_charge = _integer(
        value(block.getObj("chem_comp"), "pdbx_formal_charge"),
        "component formal charge",
    )
    atom_charge = (
        sum(atom["charge"] for atom in atoms)
        if all(atom["charge"] is not None for atom in atoms)
        else None
    )
    component_charge = dict(
        declared=declared_charge, atom_sum=atom_charge, unit="elementary_charge"
    )
    if (
        declared_charge is not None
        and atom_charge is not None
        and declared_charge != atom_charge
    ):
        _issue(
            issues,
            "component_formal_charge_conflict",
            field="formal_charge",
            status="conflict",
        )
    by_name = {name: i for i, name in enumerate(names)}
    pairs, bonds = set(), []
    orders = {"SING": 1, "DOUB": 2, "TRIP": 3, "QUAD": 4}
    if bond_table is None and len(atoms) > 1:
        _issue(issues, "missing_bond_table", axis="bond")
    for index in range(0 if bond_table is None else bond_table.getRowCount()):
        declared_id = value(bond_table, "comp_id", index)
        if (
            declared_id is not None
            and declared_id.casefold() != component_id.casefold()
        ):
            raise FileContentError(
                "A CCD bond belongs to another component", caller=CALLER
            )
        names_pair = [
            value(bond_table, field, index) for field in ("atom_id_1", "atom_id_2")
        ]
        if any(name not in by_name for name in names_pair):
            raise FileContentError(
                "A CCD bond references an absent atom ID", caller=CALLER
            )
        pair = tuple(sorted(by_name[name] for name in names_pair))
        if pair[0] == pair[1] or pair in pairs:
            raise FileContentError(
                "CCD bonds must be unique non-self pairs", caller=CALLER
            )
        pairs.add(pair)
        order = value(bond_table, "value_order", index)
        order = order.upper() if order else None
        aromatic = _flag(
            value(bond_table, "pdbx_aromatic_flag", index), "bond aromatic"
        )
        stereo = value(bond_table, "pdbx_stereo_config", index)
        stereo = stereo.upper() if stereo is not None else None
        if stereo not in {None, "N", "E", "Z"}:
            raise FileContentError(
                "Unsupported CCD bond stereo declaration", caller=CALLER
            )
        bonds.append(
            dict(
                pair=pair,
                order=orders.get(order),
                fractional=1.5 if order == "AROM" else None,
                order_token=order,
                aromatic=aromatic,
                stereo=stereo,
                ordinal=value(bond_table, "pdbx_ordinal", index),
            )
        )
        if order not in {*orders, "AROM"}:
            _issue(
                issues,
                "unsupported_bond_order",
                axis="bond",
                index=index,
                field="order",
            )
        if aromatic is None:
            _issue(
                issues,
                "missing_bond_declaration",
                axis="bond",
                index=index,
                field="aromatic",
            )
        if (
            order == "AROM"
            and aromatic is False
            or aromatic is True
            and any(atoms[i]["aromatic"] is False for i in pair)
        ):
            _issue(
                issues,
                "contradictory_aromatic_declarations",
                axis="bond",
                index=index,
                status="conflict",
            )
        if aromatic is True and order in {"TRIP", "QUAD"}:
            _issue(
                issues,
                "unsupported_aromatic_bond_order",
                axis="bond",
                index=index,
                field="order",
            )
    return atoms, bonds, component_charge


def _hydrogen_projection(atoms, bonds, policy):
    indexed_h = {i for i, atom in enumerate(atoms) if atom["symbol"] == "H"}
    counts = np.zeros(len(atoms), dtype=np.int64)
    if policy == "explicit_atoms":
        return np.arange(len(atoms), dtype=np.int64), counts
    neighbors = {index: [] for index in indexed_h}
    for bond in bonds:
        first, second = bond["pair"]
        if first in indexed_h:
            neighbors[first].append((second, bond))
        if second in indexed_h:
            neighbors[second].append((first, bond))
    for index in indexed_h:
        atom, links = atoms[index], neighbors[index]
        if (
            atom["isotope"] is not None
            or atom["charge"] != 0
            or len(links) != 1
            or links[0][0] in indexed_h
            or links[0][1]["order"] != 1
        ):
            raise StructuralInconsistencyError(
                reason="Stored H counts cannot represent this CCD H atom without loss; request hydrogen_policy='explicit_atoms'.",
                caller=CALLER,
            )
        counts[links[0][0]] += 1
    retained = np.asarray(
        [i for i in range(len(atoms)) if i not in indexed_h], dtype=np.int64
    )
    return retained, counts


def construct(
    component_id, source, method, hydrogen_policy, descriptor_program, max_matches
):
    from molsysmt import __version__, _ackredit
    from molsysmt._private.preparation_history import append_report
    from molsysmt._private.scientific_attribution import executed_software_reference
    from molsysmt._private.scientific_citations import ARTICLES
    from molsysmt.native import MolSys
    from molsysmt.native._chemical_state import _coerce_bond_table

    block, source_record = read_definition(component_id, source)
    issues = []
    atoms, bonds, component_charge = _tables(block, component_id, issues)
    retained, hydrogen_counts = _hydrogen_projection(atoms, bonds, hydrogen_policy)
    old_to_new = np.full(len(atoms), -1, dtype=np.int64)
    old_to_new[retained] = np.arange(len(retained), dtype=np.int64)
    software = dict(molsysmt=__version__, mmcif=version("mmcif"))
    interpreted = None
    descriptor_report = None
    if method == "ccd_canonical_descriptor":
        from molsysmt._private.ccd_descriptor import interpret

        interpreted, descriptor_report = interpret(
            block,
            atoms,
            bonds,
            descriptor_program,
            max_matches,
            table_conflicts=any(item["status"] == "conflict" for item in issues),
        )
        issues.extend(descriptor_report["issues"])
        software.update(descriptor_report["software"])
    else:
        _issue(issues, "radical_and_conjugation_not_declared_by_ccd_tables")
        _issue(issues, "stereo_flags_not_independently_interpreted")

    template = MolSys(
        n_atoms=len(retained), n_groups=1, n_molecules=1, n_chains=1, n_entities=1
    )
    template.structures = None
    topology = template.topology
    topology.atoms["atom_id"] = [atoms[i]["name"] for i in retained]
    topology.atoms["atom_name"] = [atoms[i]["name"] for i in retained]
    topology.atoms["atom_type"] = [atoms[i]["symbol"] for i in retained]
    topology.atoms["isotope"] = pd.array(
        [atoms[i]["isotope"] for i in retained], dtype="UInt16"
    )
    topology.atoms["group_index"] = [0] * len(retained)
    topology.atoms["chain_index"] = [0] * len(retained)
    topology.groups["group_id"] = [source_record["component_id"]]
    topology.groups["group_name"] = [source_record["component_id"]]
    topology.groups["molecule_index"] = [0]
    topology.set_group_naming_schemes("ccd")
    topology.molecules["molecule_id"] = [source_record["component_id"]]
    topology.molecules["entity_index"] = [0]
    topology.chains["chain_id"] = ["A"]
    topology.entities["entity_id"] = [source_record["component_id"]]
    state = template.chemical_states._states[0]
    columns = dict(
        formal_charge=[atom["charge"] for atom in atoms],
        is_aromatic=[atom["aromatic"] for atom in atoms],
        n_unpaired_electrons=[None] * len(atoms),
        n_implicit_hydrogens=[0] * len(atoms),
        n_explicit_hydrogens=hydrogen_counts.tolist(),
        allows_implicit_hydrogens=[False] * len(atoms),
        stereochemistry=[
            atom["stereo"] if atom["stereo"] in {"R", "S"} else None for atom in atoms
        ],
    )
    if interpreted is not None:
        columns.update(interpreted["atoms"])
    for field, values in columns.items():
        state.set_atom_attribute(field, [values[i] for i in retained])
    rows, source_bonds = [], {}
    for index, bond in enumerate(bonds):
        first, second = (int(old_to_new[i]) for i in bond["pair"])
        if first < 0 or second < 0:
            continue
        row = dict(
            atom1_index=first,
            atom2_index=second,
            bond_type="covalent",
            bond_order=bond["order"],
            fractional_bond_order=bond["fractional"],
            is_aromatic=bond["aromatic"],
            joins_components=True,
            evidence="explicit",
        )
        if interpreted is not None:
            assigned = interpreted["bonds"][index]
            row.update(is_conjugated=assigned["is_conjugated"])
            if assigned["stereochemistry"] is not None:
                references = [int(old_to_new[i]) for i in assigned["stereo_atoms"]]
                if min(references) < 0:
                    _issue(
                        issues,
                        "stereo_reference_removed_by_h_projection",
                        axis="bond",
                        index=index,
                    )
                else:
                    row.update(
                        stereochemistry=assigned["stereochemistry"],
                        stereo_atom1_index=references[0],
                        stereo_atom2_index=references[1],
                    )
        rows.append(row)
        source_bonds[(first, second)] = index
    table = (
        pd.DataFrame(rows)
        if rows
        else pd.DataFrame(columns=["atom1_index", "atom2_index"])
    )
    template.chemical_states._set_chemical_state_bonds(_coerce_bond_table(table))
    state = template.chemical_states._states[0]
    state.connectivity_completeness = (
        "complete"
        if not any(i["reason"] == "missing_bond_table" for i in issues)
        else "partial"
    )
    template.rebuild_components(redefine_types=False, redefine_names=False)
    output_pairs = state.bonds[["atom1_index", "atom2_index"]].to_numpy(dtype=np.int64)
    bond_source_indices = np.asarray(
        [source_bonds[tuple(pair)] for pair in output_pairs], dtype=np.int64
    )
    source_to_output_bonds = np.full(len(bonds), -1, dtype=np.int64)
    source_to_output_bonds[bond_source_indices] = np.arange(
        len(bond_source_indices), dtype=np.int64
    )
    provenance = dict(
        identity=f"CCD {source_record['component_id']} reference",
        version=source_record["version"],
        source_uri=source_record["resource"],
        checksum=source_record["definition_sha256"],
        checksum_kind="selected_definition_sha256",
        hydrogen_policy=hydrogen_policy,
        method=method,
        source=deepcopy(source_record),
        descriptor=deepcopy(descriptor_report),
        software=software.copy(),
        coordinate_policy="no_coordinates_in_reference_template",
    )
    items = [
        executed_software_reference(name, used_version)
        for name, used_version in software.items()
    ]
    article = deepcopy(ARTICLES["westbrook_2015"])
    items.append(
        dict(
            id="doi:" + article["doi"],
            type="article",
            **article,
            roles=["chemical_reference_data"],
        )
    )
    items.append(
        dict(
            id="dataset:ccd:" + source_record["definition_sha256"],
            type="dataset",
            title=f"CCD component definition {source_record['component_id']}",
            **(
                {"url": source_record["resource"]}
                if source_record["kind"] == "rcsb"
                else {}
            ),
            version=source_record["version"],
            roles=["chemical_reference_data"],
        )
    )
    if descriptor_report is not None:
        items.extend(deepcopy(descriptor_report["references"]))
    report = dict(
        schema="molsysmt.chemical_reference_template@1",
        method=method,
        rule_version=1,
        status="conflict"
        if any(i["status"] == "conflict" for i in issues)
        else "unassessed"
        if issues
        else "constructed",
        template_provenance=deepcopy(provenance),
        source=deepcopy(source_record),
        n_atoms=len(retained),
        n_source_atoms=len(atoms),
        n_source_bonds=len(bonds),
        component_formal_charge=component_charge,
        source_atom_ids=[atom["name"] for atom in atoms],
        source_atom_ordinals=[atom["ordinal"] for atom in atoms],
        source_bond_ordinals=[bond["ordinal"] for bond in bonds],
        atom_map=dict(
            schema="molsysmt.atom_map@1",
            n_source_atoms=len(atoms),
            n_output_atoms=len(retained),
            source_to_output_atom_indices=old_to_new,
            output_to_source_atom_indices=retained,
        ),
        source_to_output_bond_indices=source_to_output_bonds,
        output_to_source_bond_indices=bond_source_indices,
        n_indexed_hydrogens=sum(atoms[i]["symbol"] == "H" for i in retained),
        n_stored_hydrogens=int(
            sum(columns["n_explicit_hydrogens"][i] for i in retained)
        ),
        issues=issues,
        descriptor=descriptor_report,
        units=dict(formal_charge="elementary_charge"),
        software=software,
        unassessed_checks=[
            "environmental_protonation",
            "geometry",
            "force_field_coverage",
        ],
        attribution=dict(
            schema="molsysmt.scientific_attribution@1", target=CALLER, items=items
        ),
    )
    with _ackredit.scope(CALLER) as provider:
        _ackredit.credit(
            provider,
            items,
            CALLER,
            contextual=True,
            context=dict(method=method, hydrogen_policy=hydrogen_policy),
        )
    append_report(state, report, 0)
    return dict(template=template, template_provenance=provenance, report=report)
