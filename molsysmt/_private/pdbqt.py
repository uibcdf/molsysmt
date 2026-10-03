"""Reading a bounded AutoDock4 PDBQT profile without chemical preparation.

Fields and tree grammar follow the AutoDock4.2.6 manual and Vina's
parse_pdbqt.cpp. No third-party implementation is copied.
"""

from pathlib import Path

import numpy as np

from molsysmt._private.autodock_types import decode_atom_ff_type
from molsysmt._private.smonitor import FormatError

PREFIX = "pdbqt_text:"


def fail(reason):
    raise FormatError(reason=reason, caller="molsysmt._private.pdbqt")


def read(item, *, text=False):
    payload = item[len(PREFIX) :] if text else Path(item).read_bytes().decode("utf-8")
    return parse(payload)


def parse(payload):
    """Validate fixed-column atoms and a single, balanced ligand tree."""
    atoms, bodies, branches, stack, remarks = [], [[]], [], [], []
    serials = {}
    root_seen = root_closed = False
    torsdof = None
    body = 0
    ended = False
    for line_number, line in enumerate(payload.splitlines(), 1):
        tokens = line.split()
        if not tokens:
            continue
        kind = tokens[0]
        context = f"PDBQT line {line_number}"
        if ended and kind != "REMARK":
            fail(f"{context}: molecular records after END are unsupported.")
        if kind in {"ATOM", "HETATM"}:
            if root_seen and not stack and root_closed:
                fail(f"{context}: atoms outside ROOT or BRANCH.")
            if torsdof is not None:
                fail(f"{context}: atoms after TORSDOF.")
            try:
                serial = int(line[6:11])
                coordinates = [float(line[start : start + 8]) for start in (30, 38, 46)]
                charge = float(line[68:76])
                labels = line[77:].split()
                if len(labels) != 1:
                    raise ValueError("exactly one AutoDock atom type is required")
                label = labels[0]
                element = decode_atom_ff_type(label, "autodock4")
                occupancy = float(line[54:60]) if line[54:60].strip() else None
                b_factor = float(line[60:66]) if line[60:66].strip() else None
            except (ValueError, IndexError) as error:
                fail(f"{context}: invalid atom record ({error}).")
            if serial <= 0 or serial in serials:
                fail(f"{context}: atom serials must be unique positive integers.")
            if not np.isfinite([*coordinates, charge]).all() or any(
                value is not None and not np.isfinite(value)
                for value in (occupancy, b_factor)
            ):
                fail(f"{context}: non-finite atom fields.")
            if line[:6].strip() != kind or len(line) < 78 or line[76] != " ":
                fail(f"{context}: atom fields must use the fixed-column layout.")
            if line[16:17].strip() or line[26:27].strip() or line[66:68].strip():
                fail(
                    f"{context}: alternate locations, insertion codes and footnotes are unsupported."
                )
            name = line[12:16].strip()
            residue_id = line[22:26].strip()
            if not name or (residue_id and not residue_id.lstrip("-").isdigit()):
                fail(f"{context}: invalid atom name or residue serial.")
            index = len(atoms)
            serials[serial] = index
            bodies[body].append(index)
            atoms.append(
                {
                    "serial": serial,
                    "atom_name": name,
                    "element": element,
                    "group_name": line[17:20].strip(),
                    "chain_id": line[21:22].strip(),
                    "group_id": residue_id,
                    "coordinates": coordinates,
                    "partial_charge": charge,
                    "atom_ff_type": label,
                    "occupancy": occupancy,
                    "b_factor": b_factor,
                    "record": kind,
                }
            )
        elif kind == "REMARK":
            remarks.append(line)
        elif kind == "ROOT":
            if len(tokens) != 1 or root_seen or atoms or torsdof is not None:
                fail(f"{context}: ROOT must occur once, before ligand atoms.")
            root_seen = True
        elif kind == "ENDROOT":
            if (
                len(tokens) != 1
                or not root_seen
                or root_closed
                or stack
                or not bodies[0]
            ):
                fail(f"{context}: unmatched or empty ROOT.")
            root_closed = True
        elif kind in {"BRANCH", "ENDBRANCH"}:
            if len(tokens) != 3 or not root_closed or torsdof is not None:
                fail(f"{context}: invalid torsion record.")
            try:
                parent, child = (int(value) for value in tokens[1:])
            except ValueError:
                fail(f"{context}: torsion endpoints must be atom serials.")
            if parent == child or parent <= 0 or child <= 0:
                fail(f"{context}: torsion endpoints must be distinct positive serials.")
            if kind == "BRANCH":
                if (
                    parent not in serials
                    or serials[parent] not in bodies[body]
                    or child in serials
                ):
                    fail(
                        f"{context}: BRANCH parent must be in the current body and child must be new."
                    )
                new_body = len(bodies)
                bodies.append([])
                branches.append((parent, child, body, new_body))
                stack.append((parent, child, body))
                body = new_body
            else:
                if not stack or stack[-1][:2] != (parent, child):
                    fail(f"{context}: ENDBRANCH must match the most recent BRANCH.")
                if (
                    not bodies[body]
                    or child not in serials
                    or serials[child] != bodies[body][0]
                ):
                    fail(
                        f"{context}: the child must be the first atom of its branch body."
                    )
                body = stack.pop()[2]
        elif kind == "TORSDOF":
            if len(tokens) != 2 or not root_closed or stack or torsdof is not None:
                fail(f"{context}: invalid or duplicate TORSDOF.")
            if not tokens[1].isdigit():
                fail(f"{context}: TORSDOF must be a nonnegative integer.")
            torsdof = int(tokens[1])
        elif kind in {"TER", "END"}:
            if root_seen or len(tokens) != 1:
                fail(f"{context}: {kind} is only supported in rigid receptor files.")
            if kind == "END":
                ended = True
        else:
            fail(
                f"{context}: unsupported record {kind!r}; flexible receptors and MODEL ensembles need separate profiles."
            )
    if not atoms or stack or (root_seen and (not root_closed or torsdof is None)):
        fail(
            "PDBQT requires atoms and a complete balanced ligand tree when ROOT is present."
        )
    tree = None
    if root_seen:
        tree = {
            "schema_version": "molsysmt.pdbqt-torsion-tree@1",
            "atom_ids": np.asarray([str(atom["serial"]) for atom in atoms]),
            "fragment_atom_indices": np.asarray(
                [atom for fragment in bodies for atom in fragment], dtype=np.int64
            ),
            "fragment_offsets": np.asarray(
                [0, *np.cumsum([len(fragment) for fragment in bodies])], dtype=np.int64
            ),
            "branch_atom_pairs": np.asarray(
                [(serials[a], serials[b]) for a, b, _, _ in branches], dtype=np.int64
            ).reshape(-1, 2),
            "branch_fragment_pairs": np.asarray(
                [(a, b) for _, _, a, b in branches], dtype=np.int64
            ).reshape(-1, 2),
            "root_fragment_index": 0,
            "torsdof": torsdof,
            "evidence": "declared_pdbqt_torsion_tree",
        }
    return {
        "atoms": atoms,
        "torsion_tree": tree,
        "remarks": remarks,
        "payload": payload,
    }


def to_native(record, *, discard_torsion_tree=False):
    """Build native atom, chemistry, structure and explicit mechanical data."""
    import pandas as pd

    from molsysmt import pyunitwizard as puw
    from molsysmt.native import MolecularMechanics, MolSys, Structures, Topology

    if record["torsion_tree"] is not None and not discard_torsion_tree:
        fail(
            "Native MolSys has no torsion-tree store. Save get_torsion_tree() separately and explicitly set discard_torsion_tree=True."
        )
    atoms = record["atoms"]
    group_keys = list(
        dict.fromkeys((a["chain_id"], a["group_id"], a["group_name"]) for a in atoms)
    )
    chain_keys = list(dict.fromkeys(a["chain_id"] for a in atoms))
    groups = {key: i for i, key in enumerate(group_keys)}
    chains = {key: i for i, key in enumerate(chain_keys)}
    topology = Topology(n_atoms=len(atoms), n_groups=len(groups), n_chains=len(chains))
    for column, key in (
        ("atom_id", "serial"),
        ("atom_name", "atom_name"),
        ("atom_type", "element"),
    ):
        topology.atoms[column] = [str(a[key]) for a in atoms]
    topology.atoms["group_index"] = pd.array(
        [groups[(a["chain_id"], a["group_id"], a["group_name"])] for a in atoms],
        dtype="Int64",
    )
    topology.atoms["chain_index"] = pd.array(
        [chains[a["chain_id"]] for a in atoms], dtype="Int64"
    )
    topology.groups["group_id"] = [key[1] or pd.NA for key in group_keys]
    topology.groups["group_name"] = [key[2] or pd.NA for key in group_keys]
    topology.chains["chain_id"] = [key or pd.NA for key in chain_keys]
    tree = record["torsion_tree"]
    if tree is not None and len(tree["branch_atom_pairs"]):
        pairs = tree["branch_atom_pairs"]
        topology._set_chemical_state_bonds(
            pd.DataFrame(
                {
                    "atom1_index": pairs[:, 0],
                    "atom2_index": pairs[:, 1],
                    "bond_type": ["covalent"] * len(pairs),
                    "bond_order": pd.array([pd.NA] * len(pairs), dtype="UInt8"),
                    "evidence": ["explicit"] * len(pairs),
                }
            )
        )
    topology._chemical_states[0].connectivity_completeness = "partial"
    topology.rebuild_components()
    topology.rebuild_molecules()
    topology.rebuild_entities()
    structures = Structures()
    structures.append(
        coordinates=puw.standardize(
            puw.quantity(
                np.asarray([a["coordinates"] for a in atoms])[None, :, :], "angstrom"
            )
        ),
        structure_id=np.asarray(["0"]),
        skip_digestion=True,
    )
    for attribute in ("occupancy", "b_factor"):
        if any(a[attribute] is not None for a in atoms):
            values = np.asarray(
                [[np.nan if a[attribute] is None else a[attribute] for a in atoms]]
            )
            setattr(
                structures,
                attribute,
                puw.quantity(values, "angstrom**2")
                if attribute == "b_factor"
                else values,
            )
    output = MolSys()
    output.topology, output.structures = topology, structures
    output.molecular_mechanics = MolecularMechanics(
        partial_charge=[a["partial_charge"] for a in atoms],
        atom_ff_type=[a["atom_ff_type"] for a in atoms],
    )
    return output
