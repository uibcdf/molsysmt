"""Adapt detected hydrogen-bond observations without changing their criteria."""

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import InternalAlgorithmError, NotImplementedMethodError
from molsysmt._private.variables import is_all


def to_buch_interactions(
    molecular_system,
    structure_indices,
    donors,
    acceptors,
    atoms,
    distances,
    distance_threshold,
    pbc,
    donors_2=None,
    acceptors_2=None,
):
    """Describe the scope and H-A images of observed Buch triples."""
    return _to_hbond_interactions(
        "buch",
        molecular_system,
        structure_indices,
        donors,
        acceptors,
        atoms,
        distances,
        distance_threshold,
        pbc,
        donors_2,
        acceptors_2,
    )


def to_luzard_chandler_interactions(
    molecular_system,
    structure_indices,
    donors,
    acceptors,
    atoms,
    distances,
    angles,
    distance_threshold,
    angle_threshold,
    pbc,
    donors_2=None,
    acceptors_2=None,
):
    """Describe the scope and D-H/D-A images of observed angular triples."""
    return _to_hbond_interactions(
        "luzard_chandler",
        molecular_system,
        structure_indices,
        donors,
        acceptors,
        atoms,
        distances,
        distance_threshold,
        pbc,
        donors_2,
        acceptors_2,
        angles=angles,
        angle_threshold=angle_threshold,
    )


def _to_hbond_interactions(
    method,
    molecular_system,
    structure_indices,
    donors,
    acceptors,
    atoms,
    distances,
    distance_threshold,
    pbc,
    donors_2=None,
    acceptors_2=None,
    *,
    angles=None,
    angle_threshold=None,
):
    """Pack common participant roles and each method's observed measures."""
    from molsysmt import __version__
    from molsysmt.basic import get
    from molsysmt.interactions.result import Interactions

    from .get_acceptor_atoms import acceptor_exclusion_rules, acceptor_inclusion_rules
    from .get_donor_atoms import donor_exclusion_rules, donor_inclusion_rules

    n_atoms, n_structures = get(molecular_system, n_atoms=True, n_structures=True)
    frames = (
        np.arange(n_structures, dtype=np.int64)
        if is_all(structure_indices)
        else np.atleast_1d(structure_indices)
    )
    first = np.union1d(np.asarray(donors).ravel(), acceptors).astype(np.int64)
    second = None
    mode = "internal"
    universe = first
    if donors_2 is not None:
        second = np.union1d(np.asarray(donors_2).ravel(), acceptors_2).astype(np.int64)
        same_roles = np.array_equal(donors, donors_2) and np.array_equal(
            acceptors, acceptors_2
        )
        if not same_roles:
            if np.intersect1d(first, second).size:
                raise NotImplementedMethodError(
                    method=f"{method} Interactions output",
                    arguments="partially overlapping participant universes",
                    caller=f"molsysmt.interactions.hbonds.get_{method}_hbonds",
                )
            mode = "between"
            universe = np.union1d(first, second)
        else:
            second = None

    records = []
    visited = set()
    for position, (frame, triples, frame_distances) in enumerate(
        zip(frames, atoms, distances)
    ):
        frame = int(frame)
        if frame in visited:
            continue
        visited.add(frame)
        triples = np.asarray(triples, dtype=np.int64).reshape(-1, 3)
        if not len(triples):
            continue
        values = np.asarray(puw.get_value(frame_distances, to_unit="nanometers"))
        triples, first_observations = np.unique(triples, axis=0, return_index=True)
        values = values[first_observations]
        angle_values = (
            None
            if angles is None
            else np.asarray(puw.get_value(angles[position], to_unit="radians"))[
                first_observations
            ]
        )
        images = None
        if pbc:
            images = (
                _buch_images(molecular_system, frame, triples, values)
                if angle_values is None
                else _luzard_chandler_images(
                    molecular_system, frame, triples, values, angle_values
                )
            )
        for index, triple in enumerate(triples):
            record = {
                "structure_index": frame,
                "interaction_type": "hbond",
                "participants": [
                    {"role": role, "atom_indices": [int(atom)]}
                    for role, atom in zip(("donor", "hydrogen", "acceptor"), triple)
                ],
                "measurements": {"distance": float(values[index])},
                "evidence": "observed_geometry",
            }
            if images is not None:
                record["images"] = images[index].tolist()
            if angle_values is not None:
                record["measurements"]["angle"] = float(angle_values[index])
            records.append(record)

    parameters = {
        "distance_threshold_nm": float(
            puw.get_value(distance_threshold, to_unit="nanometers")
        ),
        "distance_definition": "hydrogen_acceptor"
        if angles is None
        else "donor_acceptor",
        "pbc": bool(pbc),
        "exclude_self_donor_acceptor": True,
        "role_identification": {
            "donor_inclusion_rules": list(donor_inclusion_rules),
            "donor_exclusion_rules": list(donor_exclusion_rules),
            "acceptor_inclusion_rules": list(acceptor_inclusion_rules),
            "acceptor_exclusion_rules": list(acceptor_exclusion_rules),
            "hydrogens": "covalently_bonded_to_selected_donors",
        },
        "image_policy": (
            "donor_hydrogen_then_hydrogen_acceptor_mic"
            if angles is None
            else "donor_hydrogen_and_donor_acceptor_mic"
        ),
    }
    units = {"distance": "nm"}
    if angles is not None:
        units["angle"] = "rad"
        parameters.update(
            {
                "angle_threshold_rad": float(
                    puw.get_value(angle_threshold, to_unit="radians")
                ),
                "angle_definition": "hydrogen_donor_acceptor",
                "angle_comparison": "strictly_less_than",
            }
        )
    return Interactions.from_records(
        records,
        n_atoms=n_atoms,
        n_structures=n_structures,
        evaluated_structure_indices=frames,
        method=f"molsysmt.interactions.hbonds.get_{method}_hbonds",
        software={"molsysmt": __version__},
        parameters=parameters,
        measure_units=units,
        evaluation_mode=mode,
        evaluation_atom_indices=first,
        evaluation_atom_indices_b=second,
        evaluation_universe_indices=universe,
    )


def _buch_images(molecular_system, frame, triples, expected_distances):
    """Anchor the donor, unwrap D-H, then use the detector's H-A MIC image."""
    from molsysmt._private.rust_backend import get_mic_pair_observations
    from molsysmt.basic import get

    box = get(molecular_system, structure_indices=frame, box=True)
    if box is None or box[0] is None:
        return None
    box_nm = np.asarray(puw.get_value(box, to_unit="nanometers"))
    atoms = np.unique(triples)
    coordinates = get(
        molecular_system,
        element="atom",
        selection=atoms,
        structure_indices=frame,
        coordinates=True,
    )
    coordinates_nm = np.asarray(puw.get_value(coordinates, to_unit="nanometers"))[0]
    positions = np.searchsorted(atoms, triples)
    local_frames = np.zeros(len(triples), dtype=np.int64)
    _, hydrogen_images = get_mic_pair_observations(
        coordinates_nm[positions[:, 0]],
        coordinates_nm[positions[:, 1]],
        box_nm,
        local_frames,
    )
    observed, acceptor_images = get_mic_pair_observations(
        coordinates_nm[positions[:, 1]],
        coordinates_nm[positions[:, 2]],
        box_nm,
        local_frames,
    )
    if not np.allclose(observed, expected_distances, atol=1e-8, rtol=1e-8):
        raise InternalAlgorithmError(
            reason="periodic Buch images disagree with detected H-A distances",
            caller="molsysmt.interactions.hbonds.get_buch_hbonds",
        )
    images = np.zeros((len(triples), 3, 3), dtype=np.int64)
    images[:, 1] = hydrogen_images
    images[:, 2] = hydrogen_images.astype(np.int64) + acceptor_images
    limits = np.iinfo(np.int32)
    if np.any(images < limits.min) or np.any(images > limits.max):
        raise InternalAlgorithmError(
            reason="periodic hydrogen-bond image exceeds the int32 range",
            caller="molsysmt.interactions.hbonds.get_buch_hbonds",
        )
    return images.astype(np.int32)


def _luzard_chandler_images(
    molecular_system, frame, triples, expected_distances, expected_angles
):
    """Anchor D and reproduce the independently wrapped D-H and D-A vectors."""
    from molsysmt._private.rust_backend import get_mic_pair_observations
    from molsysmt.basic import get

    box = get(molecular_system, structure_indices=frame, box=True)
    if box is None or box[0] is None:
        return None
    box_nm = np.asarray(puw.get_value(box, to_unit="nanometers"))
    atoms = np.unique(triples)
    coordinates = get(
        molecular_system,
        element="atom",
        selection=atoms,
        structure_indices=frame,
        coordinates=True,
    )
    coordinates_nm = np.asarray(puw.get_value(coordinates, to_unit="nanometers"))[0]
    positions = np.searchsorted(atoms, triples)
    local_frames = np.zeros(len(triples), dtype=np.int64)
    _, hydrogen_images = get_mic_pair_observations(
        coordinates_nm[positions[:, 0]],
        coordinates_nm[positions[:, 1]],
        box_nm,
        local_frames,
    )
    distances, acceptor_images = get_mic_pair_observations(
        coordinates_nm[positions[:, 0]],
        coordinates_nm[positions[:, 2]],
        box_nm,
        local_frames,
    )
    images = np.zeros((len(triples), 3, 3), dtype=np.int32)
    images[:, 1] = hydrogen_images
    images[:, 2] = acceptor_images
    observed = coordinates_nm[positions] + images @ box_nm[0]
    donor_hydrogen = observed[:, 1] - observed[:, 0]
    donor_acceptor = observed[:, 2] - observed[:, 0]
    angles = np.arctan2(
        np.linalg.norm(np.cross(donor_hydrogen, donor_acceptor), axis=1),
        np.einsum("ij,ij->i", donor_hydrogen, donor_acceptor),
    )
    # Acos in the detector can lose precision near collinear vectors.
    if (
        not np.allclose(distances, expected_distances, atol=1e-8, rtol=1e-8)
        or not np.allclose(
            np.linalg.norm(donor_acceptor, axis=1),
            expected_distances,
            atol=1e-8,
            rtol=1e-8,
        )
        or not np.allclose(angles, expected_angles, atol=1e-7, rtol=1e-8)
    ):
        raise InternalAlgorithmError(
            reason="periodic Luzard-Chandler images disagree with detected D-A distances or H-D-A angles",
            caller="molsysmt.interactions.hbonds.get_luzard_chandler_hbonds",
        )
    return images
