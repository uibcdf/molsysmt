"""Prepare checksum-fixed molecular fixtures and an independent plane oracle.

The fixed aromatic memberships are separate from production perception. The
reference enumerates every small-fixture ring pair and fits covariance normals;
production uses packed rectangular SVD and bounded spatial neighbors.
"""

import hashlib
import json
from itertools import combinations
from pathlib import Path

import numpy as np

from devtools.scripts.ionic_validation_systems import prepare_system as prepare_protein

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "devtools/data/pi_pi_validation_systems.json"


def prepare_system(name):
    reference = json.loads(MANIFEST.read_text())["systems"][name]
    if hashlib.sha256((ROOT / reference["path"]).read_bytes()).hexdigest() != reference["sha256"]:
        raise ValueError("Pi-pi validation coordinates disagree with their checksum.")
    system, _, coordinates, molecule = prepare_protein(name)
    return system, reference, coordinates, molecule


def cartesian_reference(reference, coordinates, *, distance=.6, angle=np.pi / 6,
                        offset=.2, planarity=.02, frames=None):
    """Return exhaustive nonperiodic observations without production helpers."""
    rings = reference["rings"]
    observations = {}
    frames = range(len(coordinates)) if frames is None else sorted(set(frames))
    for frame in frames:
        planes = []
        for atoms in rings:
            xyz = coordinates[frame, atoms]
            center = xyz.mean(axis=0)
            centered = xyz - center
            _, vectors = np.linalg.eigh(centered.T @ centered)
            normal = vectors[:, 0]
            deviations = np.abs(centered @ normal)
            planes.append((center, normal, np.sqrt(np.mean(deviations ** 2)), deviations.max()))
        for a, b in combinations(range(len(rings)), 2):
            if set(rings[a]) & set(rings[b]):
                continue
            ca, na, ra, ma = planes[a]
            cb, nb, rb, mb = planes[b]
            d = cb - ca
            length = np.sqrt(np.dot(d, d))
            alpha = np.arccos(np.clip(abs(np.dot(na, nb)), 0, 1))
            oa = np.sqrt(np.dot(d - np.dot(d, na) * na, d - np.dot(d, na) * na))
            ob = np.sqrt(np.dot(d - np.dot(d, nb) * nb, d - np.dot(d, nb) * nb))
            parallel = alpha <= angle and oa <= offset and ob <= offset
            edge = np.pi / 2 - alpha <= angle and min(oa, ob) <= offset
            if 0 < length <= distance and max(ma, mb) <= planarity and (parallel or edge):
                observations[frame, tuple(rings[a]), tuple(rings[b])] = (
                    length, alpha, oa, ob, ra, rb, ma, mb, int(edge),
                )
    return observations


def observation_columns(result):
    relations = []
    for index in range(len(result.relation_types)):
        relation = result.relation(index)
        relations.append(tuple(tuple(part["atom_indices"]) for part in relation["participants"]))
    names = ("distance", "plane_angle", "offset_a", "offset_b", "rms_deviation_a",
             "rms_deviation_b", "max_deviation_a", "max_deviation_b")
    return {(int(frame), *relations[relation]): tuple(result.measurements[name][index] for name in names)
            + (int(result.occurrence_evidence[index]),)
            for index, (frame, relation) in enumerate(zip(result.occurrence_structures, result.occurrence_relations))}
