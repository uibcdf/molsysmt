"""Assembling explicitly selected peptide chemistry from versioned fragments."""

import json
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
from importlib.resources import files

import numpy as np
import pandas as pd

from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError


@lru_cache(maxsize=1)
def _fragments():
    raw = (
        files("molsysmt.data")
        .joinpath("databases/peptide_templates/residue_fragments.json")
        .read_bytes()
    )
    data = json.loads(raw)
    if data["schema"] != "molsysmt.peptide_fragments@1" or data.get("units") != {
        "formal_charge": "elementary_charge"
    }:
        raise StructuralInconsistencyError(
            reason="The peptide fragment schema or formal-charge unit is unsupported.",
            caller="molsysmt.physchem.get_peptide_chemical_template",
        )
    return data, sha256(raw).hexdigest()


def assemble(
    residue_names, n_terminal_state, c_terminal_state, disulfide_group_pairs, caller
):
    """Close every declared port before claiming complete peptide connectivity."""
    from molsysmt import __version__, _ackredit
    from molsysmt._private.scientific_citations import SOFTWARE
    from molsysmt.native import MolSys, Topology

    library, library_sha256 = _fragments()
    unsupported = [name for name in residue_names if name not in library["residues"]]
    if unsupported:
        raise ArgumentError(
            "residue_names",
            value=residue_names,
            caller=caller,
            message=f"Unsupported explicit residue states: {unsupported}. HIS requires HID, HIE or HIP.",
        )
    pairs = (
        np.empty((0, 2), dtype=np.int64)
        if disulfide_group_pairs is None
        else np.asarray(disulfide_group_pairs)
    )
    pairs = np.sort(pairs, axis=1)
    pairs = pairs[np.lexsort((pairs[:, 1], pairs[:, 0]))]
    cyx = {i for i, name in enumerate(residue_names) if name == "CYX"}
    participants = pairs.ravel().tolist()
    if (
        any(i >= len(residue_names) for i in participants)
        or len(set(participants)) != len(participants)
        or set(participants) != cyx
    ):
        raise ArgumentError(
            "disulfide_group_pairs",
            value=pairs,
            caller=caller,
            message="Every CYX group must occur in exactly one declared disulfide pair; no other state can participate.",
        )
    atoms, bonds, ports = [], [], []
    backbone_carbonyls = set()
    for group_index, name in enumerate(residue_names):
        fragment = deepcopy(library["residues"][name])
        local = {}
        for atom in fragment["atoms"]:
            index = len(atoms)
            local[atom["name"]] = index
            atoms.append(dict(**atom, group_index=group_index))
        for bond in fragment["bonds"]:
            a, b = [local[name] for name in bond.pop("atom_names")]
            bonds.append(dict(atom1_index=a, atom2_index=b, **bond))
        ports.append({role: local[name] for role, name in fragment["ports"].items()})
        backbone_carbonyls.add(tuple(sorted((local["C"], local["O"]))))
    for i in range(len(residue_names) - 1):
        bonds.append(
            dict(
                atom1_index=ports[i]["peptide_C"],
                atom2_index=ports[i + 1]["peptide_N"],
                bond_order=1,
                is_aromatic=False,
                is_conjugated=True,
            )
        )
    for first, second in pairs:
        bonds.append(
            dict(
                atom1_index=ports[first]["disulfide_S"],
                atom2_index=ports[second]["disulfide_S"],
                bond_order=1,
                is_aromatic=False,
                is_conjugated=False,
            )
        )
    nitrogen = atoms[ports[0]["peptide_N"]]
    nitrogen["formal_charge"] = 1 if n_terminal_state == "ammonium" else 0
    nitrogen["hydrogen_count"] += 2 if n_terminal_state == "ammonium" else 1
    oxygen_index = len(atoms)
    atoms.append(
        dict(
            name="OXT",
            element="O",
            group_index=len(residue_names) - 1,
            formal_charge=-1 if c_terminal_state == "carboxylate" else 0,
            hydrogen_count=0 if c_terminal_state == "carboxylate" else 1,
            is_aromatic=False,
        )
    )
    bonds.append(
        dict(
            atom1_index=ports[-1]["peptide_C"],
            atom2_index=oxygen_index,
            bond_order=1,
            is_aromatic=False,
            is_conjugated=True,
        )
    )
    # Every backbone carbonyl now belongs to a declared amide or carboxyl group.
    # Other fragment conjugation assignments retain the offline curation model.
    for bond in bonds:
        if (
            tuple(sorted((bond["atom1_index"], bond["atom2_index"])))
            in backbone_carbonyls
        ):
            bond["is_conjugated"] = True
    definition = dict(
        residue_names=residue_names,
        n_terminal_state=n_terminal_state,
        c_terminal_state=c_terminal_state,
        disulfide_group_pairs=pairs.tolist(),
        atoms=atoms,
        bonds=bonds,
        fragment_sha256=library_sha256,
        rule_version=1,
    )
    checksum = sha256(
        json.dumps(definition, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    topology = Topology(
        n_atoms=len(atoms),
        n_groups=len(residue_names),
        n_molecules=1,
        n_chains=1,
        n_entities=1,
    )
    topology.atoms["atom_id"] = [str(i) for i in range(len(atoms))]
    topology.atoms["atom_name"] = [atom["name"] for atom in atoms]
    topology.atoms["atom_type"] = [atom["element"] for atom in atoms]
    topology.atoms["group_index"] = [atom["group_index"] for atom in atoms]
    topology.atoms["chain_index"] = [0] * len(atoms)
    topology.groups["group_id"] = [str(i) for i in range(len(residue_names))]
    topology.groups["group_name"] = residue_names
    topology.groups["group_type"] = ["amino acid"] * len(residue_names)
    topology.groups["molecule_index"] = [0] * len(residue_names)
    topology.molecules["molecule_id"] = ["0"]
    topology.molecules["entity_index"] = [0]
    topology.chains["chain_id"] = ["0"]
    topology.entities["entity_id"] = ["0"]
    table = pd.DataFrame(bonds)
    table["bond_type"] = "covalent"
    table["joins_components"] = True
    table["evidence"] = "user_defined"
    topology.bonds = Topology._coerce_bond_table(table)
    state = topology._chemical_states_domain._states[0]
    for field, values in {
        "formal_charge": [atom["formal_charge"] for atom in atoms],
        "is_aromatic": [atom["is_aromatic"] for atom in atoms],
        "n_explicit_hydrogens": [atom["hydrogen_count"] for atom in atoms],
        "n_implicit_hydrogens": [0] * len(atoms),
        "n_unpaired_electrons": [0] * len(atoms),
        "allows_implicit_hydrogens": [False] * len(atoms),
    }.items():
        state.set_atom_attribute(field, values)
    state.connectivity_completeness = "complete"
    topology.rebuild_components(redefine_types=False, redefine_names=False)
    template = MolSys._from_partial_domains(
        topology=topology, chemical_states=topology._chemical_states_domain
    )
    provenance = dict(
        identity="Explicit peptide chemical template",
        version="1",
        source_uri=library["source"]["url"],
        checksum=checksum,
        checksum_kind="graph_definition_sha256",
        hydrogen_policy="stored_counts",
        residue_names=list(residue_names),
        n_terminal_state=n_terminal_state,
        c_terminal_state=c_terminal_state,
        disulfide_group_pairs=pairs.tolist(),
        source=deepcopy(library["source"]),
        fragment_sha256=library_sha256,
        curation=deepcopy(library["curation"]),
        stereochemistry="unspecified",
    )
    items = [
        dict(
            id=f"software:molsysmt:{__version__}",
            type="software",
            **deepcopy(SOFTWARE["molsysmt"]),
            version=__version__,
            roles=["executed_software"],
        ),
        dict(
            id=f"dataset:meeko-residue-templates:{library['source']['sha256']}",
            type="dataset",
            title=library["source"]["title"],
            url=library["source"]["url"],
            version=library["source"]["commit"],
            roles=["chemical_reference_data"],
        ),
    ]
    report = dict(
        schema="molsysmt.peptide_template@1",
        method="declared_residue_fragment_assembly",
        rule_version=1,
        status="constructed",
        n_atoms=len(atoms),
        n_groups=len(residue_names),
        n_indexed_hydrogens=0,
        n_stored_hydrogens=sum(atom["hydrogen_count"] for atom in atoms),
        peptide_bond_pairs=np.asarray(
            [
                [ports[i]["peptide_C"], ports[i + 1]["peptide_N"]]
                for i in range(len(residue_names) - 1)
            ],
            dtype=np.int64,
        ).reshape(-1, 2),
        disulfide_bond_pairs=np.asarray(
            [[ports[a]["disulfide_S"], ports[b]["disulfide_S"]] for a, b in pairs],
            dtype=np.int64,
        ).reshape(-1, 2),
        units={"formal_charge": "elementary_charge"},
        software={"molsysmt": __version__},
        unassessed_checks=[
            "stereochemistry",
            "environmental_protonation",
            "geometry",
            "force_field_coverage",
        ],
        attribution=dict(
            schema="molsysmt.scientific_attribution@1", target=caller, items=items
        ),
    )
    with _ackredit.scope(caller) as provider:
        _ackredit.credit(provider, items, caller)
    return dict(template=template, template_provenance=provenance, report=report)
