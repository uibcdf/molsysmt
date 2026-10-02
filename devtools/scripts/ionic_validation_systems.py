"""Prepare fixed molecular coordinates and a separately declared ionic reference.

These are developer validation fixtures, not production protonation tools.
The manifest fixes membership independently of MolSysMT recognition. RDKit
reads PDB connectivity/bond orders, while every formal charge is declared.
"""

import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "devtools/data/ionic_validation_systems.json"


def prepare_system(name):
    from rdkit import Chem

    import molsysmt as msm

    manifest = json.loads(MANIFEST.read_text())
    reference = manifest["systems"][name]
    path = ROOT / reference["path"]
    if hashlib.sha256(path.read_bytes()).hexdigest() != reference["sha256"]:
        raise ValueError(
            "Ionic validation source checksum disagrees with the manifest."
        )
    molecule = Chem.MolFromPDBFile(str(path), removeHs=False)
    if molecule is None or molecule.GetNumAtoms() != reference["atoms"]:
        raise ValueError("RDKit cannot read the declared validation atom axis.")
    if molecule.GetNumConformers() != reference["structures"]:
        raise ValueError("The validation structure axis changed.")
    for atom in molecule.GetAtoms():
        charge = reference["charge_atoms"].get(str(atom.GetIdx()), 0)
        atom.SetFormalCharge(charge)
        if charge < 0:
            atom.SetNoImplicit(True)
    Chem.SanitizeMol(molecule)
    reference_coordinates = np.asarray(
        [conformer.GetPositions() / 10.0 for conformer in molecule.GetConformers()]
    )
    system = msm.convert(molecule, to_form="molsysmt.MolSys")
    return system, reference, reference_coordinates, molecule


def cartesian_reference(
    reference,
    coordinates,
    threshold,
    *,
    frames=None,
    selected=None,
    second=None,
    scope="internal",
):
    """Enumerate small reference center pairs without MolSysMT geometry helpers.

    Membership and reference atoms come from the manifest; the independent
    algorithm evaluates every applicable reference-atom displacement directly.
    Output keys are (source structure index, positive label, negative label).
    """
    centers = reference["centers"]
    selected = set(range(reference["atoms"])) if selected is None else set(selected)
    second = set() if second is None else set(second)
    frames = range(len(coordinates)) if frames is None else sorted(set(frames))
    observations = {}
    for positive in centers:
        if positive["charge"] <= 0:
            continue
        for negative in centers:
            if negative["charge"] >= 0:
                continue
            p, n = set(positive["atoms"]), set(negative["atoms"])
            if scope == "internal":
                include = p <= selected and n <= selected
            elif scope == "incident":
                include = bool((p | n) & selected)
            elif scope == "between":
                include = (p <= selected and n <= second) or (
                    n <= selected and p <= second
                )
            else:
                raise ValueError("Unknown validation scope.")
            if not include:
                continue
            for frame in frames:
                delta = (
                    coordinates[frame, positive["geometry"]][:, None]
                    - coordinates[frame, negative["geometry"]][None]
                )
                distance = float(np.sqrt((delta * delta).sum(axis=-1)).min())
                if distance <= threshold:
                    observations[frame, positive["label"], negative["label"]] = distance
    return observations


def observation_columns(result, reference):
    """Translate actual typed rows to independent reference labels for comparison."""
    labels = {
        tuple(center["atoms"]): center["label"] for center in reference["centers"]
    }
    relations = []
    for relation in range(len(result.relation_types)):
        start, stop = result.relation_participant_offsets[relation : relation + 2]
        roles = {}
        for participant in range(start, stop):
            a, b = result.participant_atom_offsets[participant : participant + 2]
            roles[result.participant_roles[participant]] = labels[
                tuple(result.participant_atoms[a:b])
            ]
        relations.append((roles["positive"], roles["negative"]))
    return {
        (int(frame), *relations[relation]): float(distance)
        for frame, relation, distance in zip(
            result.occurrence_structures,
            result.occurrence_relations,
            result.measurements["distance"],
        )
    }
