"""Columnar dictionary form for sparse interaction results."""

from copy import deepcopy
from dataclasses import dataclass

import numpy as np


@dataclass
class InteractionsDict:
    """Holding a lossless, versioned columnar interaction payload.

    The dictionary contains NumPy arrays. It is suitable for Python and
    HDF5-backed interchange; it is not a JSON-compatible list of records.
    """

    data: dict

    def to_dict(self, copy=True):
        """Returning the underlying columnar payload."""

        return deepcopy(self.data) if copy else self.data

    def copy(self):
        """Returning an independent columnar payload."""

        return InteractionsDict(deepcopy(self.data))


def _encode_interactions(result):
    if not result._is_full:
        raise ValueError("An InteractionsDict requires a full interaction result.")
    arrays = (
        "evaluated_structure_indices",
        "atom_source_indices",
        "structure_source_indices",
        "evaluation_atom_indices",
        "evaluation_atom_indices_b",
        "evaluation_universe_indices",
        "relation_participant_offsets",
        "participant_atom_offsets",
        "participant_atoms",
        "occurrence_structures",
        "occurrence_relations",
        "occurrence_evidence",
        "occurrence_image_offsets",
        "image_vectors",
    )
    data = {
        "schema": "molsysmt.interactions_dict",
        "version": 1,
        "n_atoms": result.n_atoms,
        "n_structures": result.n_structures,
        "source_n_atoms": result.source_n_atoms,
        "source_n_structures": result.source_n_structures,
        "evaluation_mode": result.evaluation_mode,
        "relation_types": tuple(result.relation_types),
        "participant_roles": tuple(result.participant_roles),
        "evidence_labels": tuple(result.evidence_labels),
        "measurements": {
            name: values.copy() for name, values in result.measurements.items()
        },
        "measure_units": dict(result.measure_units),
        "method": result.method,
        "parameters": deepcopy(result.parameters),
        "source_id": result.source_id,
        "software": result.software.copy(),
    }
    data.update(
        (name, None if getattr(result, name) is None else getattr(result, name).copy())
        for name in arrays
    )
    if np.array_equal(result.atom_source_indices, np.arange(result.n_atoms)):
        data["atom_source_indices"] = None
    if np.array_equal(
        result.structure_source_indices, np.arange(result.n_structures)
    ):
        data["structure_source_indices"] = None
    return InteractionsDict(data)


def _decode_interactions(payload):
    from molsysmt.interactions.result import Interactions

    data = payload.data
    if data.get("schema") != "molsysmt.interactions_dict" or data.get("version") != 1:
        raise ValueError("Unsupported InteractionsDict schema or version.")
    labels = tuple(data["evidence_labels"])
    codes = np.asarray(data["occurrence_evidence"], dtype=np.int64)
    if np.any(codes < 0) or np.any(codes >= len(labels)):
        raise ValueError("InteractionsDict evidence codes are outside the label table.")
    return Interactions(
        n_atoms=data["n_atoms"],
        n_structures=data["n_structures"],
        source_n_atoms=data.get("source_n_atoms", data["n_atoms"]),
        source_n_structures=data.get("source_n_structures", data["n_structures"]),
        evaluation_mode=data.get("evaluation_mode", "internal"),
        evaluation_atom_indices=(
            None if data.get("evaluation_atom_indices") is None
            else data["evaluation_atom_indices"].copy()
        ),
        evaluation_atom_indices_b=(
            None if data.get("evaluation_atom_indices_b") is None
            else data["evaluation_atom_indices_b"].copy()
        ),
        evaluation_universe_indices=(
            None if data.get("evaluation_universe_indices") is None
            else data["evaluation_universe_indices"].copy()
        ),
        atom_source_indices=(
            None if data.get("atom_source_indices") is None
            else data["atom_source_indices"].copy()
        ),
        structure_source_indices=(
            None if data.get("structure_source_indices") is None
            else data["structure_source_indices"].copy()
        ),
        evaluated_structure_indices=data["evaluated_structure_indices"].copy(),
        relation_types=tuple(data["relation_types"]),
        relation_participant_offsets=data["relation_participant_offsets"].copy(),
        participant_roles=tuple(data["participant_roles"]),
        participant_atom_offsets=data["participant_atom_offsets"].copy(),
        participant_atoms=data["participant_atoms"].copy(),
        occurrence_structures=data["occurrence_structures"].copy(),
        occurrence_relations=data["occurrence_relations"].copy(),
        occurrence_evidence=codes.copy(),
        evidence_labels=labels,
        measurements={
            name: values.copy() for name, values in data["measurements"].items()
        },
        measure_units=dict(data["measure_units"]),
        method=data["method"],
        parameters=deepcopy(data["parameters"]),
        source_id=data["source_id"],
        software=data.get("software"),
        occurrence_image_offsets=(
            None if data["occurrence_image_offsets"] is None
            else data["occurrence_image_offsets"].copy()
        ),
        image_vectors=(
            None if data["image_vectors"] is None else data["image_vectors"].copy()
        ),
    )
