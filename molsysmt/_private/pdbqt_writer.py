"""Serializing validated native data into a bounded AutoDock4 PDBQT profile."""

import numpy as np
import pandas as pd

from molsysmt import pyunitwizard as puw
from molsysmt._private.autodock_types import decode_atom_ff_type
from molsysmt._private.pdbqt import fail, parse


def validate_tree(tree, atom_ids):
    """Validate a rooted fragment tree bound to the exact selected atom inventory."""
    if (
        not isinstance(tree, dict)
        or tree.get("schema_version") != "molsysmt.pdbqt-torsion-tree@1"
    ):
        fail("torsion_tree must use the molsysmt.pdbqt-torsion-tree@1 schema.")
    if not np.array_equal(tree.get("atom_ids"), atom_ids):
        fail(
            "torsion_tree atom_ids must match the selected native atom axis exactly; explicitly remap after extraction or reordering."
        )
    arrays = {}
    for name in (
        "fragment_atom_indices",
        "fragment_offsets",
        "branch_atom_pairs",
        "branch_fragment_pairs",
    ):
        value = np.asarray(tree.get(name))
        if value.dtype.kind not in "iu":
            fail(f"torsion_tree {name} must be an integer array.")
        arrays[name] = value
    packed, offsets = arrays["fragment_atom_indices"], arrays["fragment_offsets"]
    n_atoms = len(atom_ids)
    if packed.shape != (n_atoms,) or not np.array_equal(
        np.sort(packed), np.arange(n_atoms)
    ):
        fail(
            "torsion_tree fragment memberships must partition the complete selected atom axis."
        )
    if (
        offsets.ndim != 1
        or len(offsets) < 2
        or offsets[0] != 0
        or offsets[-1] != n_atoms
        or np.any(np.diff(offsets) <= 0)
    ):
        fail("torsion_tree offsets must delimit nonempty, disjoint fragments.")
    n_fragments = len(offsets) - 1
    atom_pairs, fragment_pairs = (
        arrays["branch_atom_pairs"],
        arrays["branch_fragment_pairs"],
    )
    if atom_pairs.shape != (n_fragments - 1, 2) or fragment_pairs.shape != (
        n_fragments - 1,
        2,
    ):
        fail("torsion_tree needs one aligned branch per non-root fragment.")
    if (
        np.any(atom_pairs < 0)
        or np.any(atom_pairs >= n_atoms)
        or np.any(fragment_pairs < 0)
        or np.any(fragment_pairs >= n_fragments)
    ):
        fail("torsion_tree branch indices are out of range.")
    if tree.get("root_fragment_index") != 0:
        fail("The supported PDBQT torsion tree uses root_fragment_index=0.")
    torsdof = tree.get("torsdof")
    if (
        isinstance(torsdof, (bool, np.bool_))
        or not isinstance(torsdof, (int, np.integer))
        or torsdof < 0
    ):
        fail("torsion_tree torsdof must be a nonnegative integer.")
    labels = np.empty(n_atoms, dtype=np.int64)
    for fragment in range(n_fragments):
        labels[packed[offsets[fragment] : offsets[fragment + 1]]] = fragment
    if not np.array_equal(labels[atom_pairs], fragment_pairs):
        fail("torsion_tree branch endpoints must belong to their declared fragments.")
    if not np.array_equal(np.sort(fragment_pairs[:, 1]), np.arange(1, n_fragments)):
        fail("Each non-root fragment must have exactly one incoming branch.")
    children = [[] for _ in range(n_fragments)]
    for branch, (parent, child) in enumerate(fragment_pairs):
        children[parent].append((int(child), branch))
    reached, pending = set(), [0]
    while pending:
        fragment = pending.pop()
        if fragment in reached:
            fail("torsion_tree cannot contain cycles.")
        reached.add(fragment)
        pending.extend(child for child, _ in children[fragment])
    if len(reached) != n_fragments:
        fail("torsion_tree must connect every fragment to ROOT.")
    return packed, offsets, atom_pairs, children, int(torsdof)


def _field(value, width, name, *, integer=False):
    if pd.isna(value):
        return " " * width
    text = str(value)
    if integer:
        try:
            number = int(text)
        except ValueError:
            fail(f"PDBQT {name} must be an integer string.")
        if str(number) != text:
            fail(f"PDBQT {name} must have a canonical integer representation.")
    if len(text) > width or any(char.isspace() for char in text) or not text.isascii():
        fail(f"PDBQT {name} cannot fit its {width}-column field.")
    return text.rjust(width)


def serialize(item, *, typing_scheme, torsion_tree=None):
    """Validate all inputs before producing text; preserve every present hydrogen."""
    if typing_scheme != "autodock4":
        fail(
            "PDBQT writing requires explicit typing_scheme='autodock4'. No atom types are assigned."
        )
    from molsysmt._private.partial_charges import validate_assignment

    validate_assignment(item)
    topology, structures, mechanics = (
        item.topology,
        item.structures,
        item.molecular_mechanics,
    )
    if (
        topology is None
        or structures is None
        or structures.n_structures != 1
        or structures.coordinates is None
    ):
        fail(
            "PDBQT output requires topology and exactly one selected structure with coordinates."
        )
    n_atoms = topology.n_atoms
    if not n_atoms:
        fail("PDBQT output requires at least one atom.")
    coordinates = puw.get_value(structures.coordinates, to_unit="angstrom")
    if coordinates.shape != (1, n_atoms, 3) or not np.isfinite(coordinates).all():
        fail("PDBQT coordinates must be finite and aligned with the atom axis.")
    if (
        mechanics is None
        or mechanics.atom_ff_type is None
        or mechanics.partial_charge is None
    ):
        fail(
            "PDBQT output requires explicit AutoDock4 atom_ff_type and partial_charge for every atom."
        )
    types = mechanics.atom_ff_type
    try:
        charges = np.asarray(mechanics.partial_charge, dtype=float)
    except (ValueError, TypeError):
        fail("PDBQT partial charges must be finite native values in elementary charge.")
    if (
        len(types) != n_atoms
        or charges.shape != (n_atoms,)
        or not np.isfinite(charges).all()
    ):
        fail(
            "PDBQT types and partial charges must be finite and aligned with the atom axis."
        )
    atom_ids = topology.atoms["atom_id"].astype(str).to_numpy()
    try:
        serials = np.asarray([int(value) for value in atom_ids], dtype=np.int64)
    except (ValueError, OverflowError):
        fail("PDBQT writing requires unique canonical integer atom IDs in [1, 99999].")
    if (
        np.any(serials < 1)
        or np.any(serials > 99999)
        or len(np.unique(serials)) != n_atoms
        or any(str(serial) != atom_id for serial, atom_id in zip(serials, atom_ids))
    ):
        fail("PDBQT writing requires unique canonical integer atom IDs in [1, 99999].")
    isotope = topology.atoms["isotope"]
    if isotope.notna().any():
        fail("PDBQT cannot encode explicit isotope assignments.")
    lines = []
    for index, atom in topology.atoms.iterrows():
        try:
            element = decode_atom_ff_type(types[index], typing_scheme)
        except ValueError as error:
            fail(str(error))
        if element != atom["atom_type"]:
            fail(f"AutoDock4 type and chemical element disagree at atom index {index}.")
        name = _field(atom["atom_name"], 4, "atom_name")
        if not name.strip():
            fail("PDBQT writing requires atom names.")
        group = (
            topology.groups.loc[atom["group_index"]]
            if pd.notna(atom["group_index"])
            else {}
        )
        chain = (
            topology.chains.loc[atom["chain_index"]]
            if pd.notna(atom["chain_index"])
            else {}
        )
        group_name = _field(group.get("group_name", pd.NA), 3, "group_name")
        group_id = _field(group.get("group_id", pd.NA), 4, "group_id", integer=True)
        chain_id = _field(chain.get("chain_id", pd.NA), 1, "chain_id")
        geometry = "".join(f"{value:8.3f}" for value in coordinates[0, index])
        charge = f"{charges[index]:8.3f}"
        if len(geometry) != 24 or len(charge) != 8:
            fail("PDBQT coordinates or charges exceed their fixed-column fields.")
        fields = []
        for attribute, unit in (("occupancy", None), ("b_factor", "angstrom**2")):
            value = getattr(structures, attribute, None)
            if value is None:
                fields.append(" " * 6)
                continue
            values = puw.get_value(value, to_unit=unit) if unit else value
            if np.shape(values) != (1, n_atoms):
                fail(f"PDBQT {attribute} must align with the selected atom axis.")
            number = values[0, index]
            field = " " * 6 if np.isnan(number) else f"{number:6.2f}"
            if len(field) != 6 or np.isinf(number):
                fail(f"PDBQT {attribute} exceeds its fixed-column field.")
            fields.append(field)
        lines.append(
            f"ATOM  {serials[index]:5d} {name} {group_name} {chain_id}{group_id}    {geometry}{fields[0]}{fields[1]}  {charge} {types[index]}"
        )
    if torsion_tree is None:
        payload = "\n".join([*lines, "END", ""])
    else:
        packed, offsets, pairs, children, torsdof = validate_tree(
            torsion_tree, atom_ids
        )
        states = item.chemical_states
        state = (
            states._states[states._reference_index]
            if states is not None and states.n_chemical_states
            else None
        )
        if state is not None and state.connectivity_completeness == "complete":
            from molsysmt.topology import get_rigid_fragments

            lookup = {
                tuple(sorted((int(row.atom1_index), int(row.atom2_index)))): index
                for index, row in state.bonds.iterrows()
                if row.bond_type == "covalent"
            }
            try:
                cuts = [lookup[tuple(sorted(pair))] for pair in pairs]
            except KeyError:
                fail(
                    "Every tree branch must be a declared covalent bond in the complete native graph."
                )
            fragments = get_rigid_fragments(item, bond_indices=cuts)
            actual = fragments["atom_fragment_indices"]
            expected_groups = [
                packed[offsets[i] : offsets[i + 1]] for i in range(len(offsets) - 1)
            ]
            if len(fragments["fragment_offsets"]) != len(offsets) or any(
                len(np.unique(actual[group])) != 1 for group in expected_groups
            ):
                fail(
                    "torsion_tree fragments must agree with the complete native graph after cutting its branch bonds."
                )
        # An explicit stack also handles deeply nested trees without Python's
        # recursion limit; child atoms lead each branch body as Vina requires.
        output = ["ROOT"]
        output.extend(lines[atom] for atom in packed[offsets[0] : offsets[1]])
        output.append("ENDROOT")
        pending = [("open", child, branch) for child, branch in reversed(children[0])]
        while pending:
            action, fragment, branch = pending.pop()
            parent_atom, child_atom = pairs[branch]
            endpoints = f"{serials[parent_atom]} {serials[child_atom]}"
            if action == "close":
                output.append(f"ENDBRANCH {endpoints}")
                continue
            output.append(f"BRANCH {endpoints}")
            members = packed[offsets[fragment] : offsets[fragment + 1]]
            output.append(lines[child_atom])
            output.extend(lines[atom] for atom in members if atom != child_atom)
            pending.append(("close", fragment, branch))
            pending.extend(
                ("open", child, edge) for child, edge in reversed(children[fragment])
            )
        output.append(f"TORSDOF {torsdof}")
        payload = "\n".join([*output, ""])
    parse(payload)
    report = getattr(mechanics, "partial_charge_assignment", None)
    if report is not None:
        import json

        provenance = {
            name: report[name]
            for name in (
                "method",
                "engine",
                "software",
                "chemical_state_index",
                "charge_unit",
                "status",
            )
        }
        provenance.update(
            source_coverage=report["coverage"],
            n_source_atoms=report["n_atoms"],
            n_written_atoms=n_atoms,
            total_charge_before_rounding=float(np.sum(charges)),
            decimal_places=3,
            parameters=report["parameters"],
        )
        payload = (
            "REMARK MOLSYSMT_PARTIAL_CHARGES "
            + json.dumps(provenance, sort_keys=True, separators=(",", ":"))
            + "\n"
            + payload
        )
    return payload
