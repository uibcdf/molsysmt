"""Preserve public reference requests when aromatic detectors use external syntax."""

from copy import deepcopy

import numpy as np
import pandas as pd
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, UnsupportedHeavyOperationError

PROFILES = [
    ("pi_pi", "centroid_angle_offset", "least_squares"),
    ("pi_pi", "centroid_angle_offset", "three_atom_plane"),
    ("pi_pi", "plane_angle_intersection", "smarts_5_6"),
    ("pi_pi", "plane_angle_intersection", "aromatic_cycles"),
    ("cation_pi", "centroid_angle_offset", "least_squares"),
    ("cation_pi", "centroid_distance_offset", "three_atom_plane"),
    ("cation_pi", "centroid_distance_angle", "smarts_5_6"),
]


@pytest.fixture(params=PROFILES)
def aromatic_case(request):
    family, method, profile = request.param
    source = msm.convert(
        Chem.MolFromSmiles(
            "c1ccccc1.c1ccccc1" if family == "pi_pi" else "c1ccccc1.[NH4+]"
        )
    )
    angle = np.arange(6) * np.pi / 3
    ring = np.column_stack((0.14 * np.cos(angle), 0.14 * np.sin(angle), np.zeros(6)))
    partner = ring if family == "pi_pi" else np.zeros((1, 3))
    coordinates = np.asarray(
        [
            np.vstack((ring, partner + offset))
            for offset in ([0, 0, 0.35], [0, 0, 2], [0.05, 0, 0.36])
        ]
    )
    source.structures.append(coordinates=msm.pyunitwizard.quantity(coordinates, "nm"))
    source.chemical_states.append_state()
    source.chemical_states._states[1] = deepcopy(source.chemical_states._states[0])
    source.chemical_states._reference_index = 1
    source._set_structure_chemical_state_indices([0, 0, 0])
    return source, family, method, profile


def calculate(case, source, **kwargs):
    _, family, method, profile = case
    options = dict(
        method=method, profile=profile, pbc=False, structure_indices=[2, 0, 2, 1]
    )
    if profile == "least_squares":
        options.update(
            distance_threshold=".6 nm",
            angle_threshold="30 degrees",
            offset_threshold=".2 nm",
            planarity_threshold=".02 nm",
        )
    options.update(kwargs)
    name = (
        "get_pi_pi_interactions" if family == "pi_pi" else "get_cation_pi_interactions"
    )
    return getattr(getattr(msm.interactions, family), name)(source, **options)


def same_result(actual, expected):
    for field in (
        "participant_atoms",
        "participant_atom_offsets",
        "occurrence_structures",
        "occurrence_relations",
        "evaluated_structure_indices",
        "atom_source_indices",
        "structure_source_indices",
    ):
        np.testing.assert_array_equal(getattr(actual, field), getattr(expected, field))
    assert actual.participant_roles == expected.participant_roles
    assert actual.relation_types == expected.relation_types
    assert actual.measure_units == expected.measure_units
    assert actual.parameters == expected.parameters
    assert actual.software == expected.software
    for key, values in expected.measurements.items():
        np.testing.assert_allclose(actual.measurements[key], values, atol=1e-12, rtol=0)


def external(indices):
    return "index " + " ".join(map(str, indices))


@pytest.mark.parametrize("form", ["native", "h5msm", "composite"])
@pytest.mark.parametrize("reference", [None, "reference"])
@pytest.mark.parametrize(
    "mode,slot",
    [
        ("internal", "first"),
        ("incident", "first"),
        ("between", "first"),
        ("between", "second"),
        ("between", "both"),
    ],
)
def test_reference_mdtraj_selections_match_numeric_queries(
    aromatic_case, form, reference, mode, slot, tmp_path
):
    source, family, _, _ = aromatic_case
    atoms = source.topology.atoms.copy(deep=True)
    bonds = [state.bonds.copy(deep=True) for state in source.chemical_states._states]
    first, second = list(range(6)), list(range(6, source.topology.n_atoms))
    if mode == "internal":
        first = first + second
    kwargs = dict(selection=first, selection_mode=mode, chemical_state=reference)
    if mode == "between":
        kwargs["selection_2"] = second
    if form == "h5msm":
        item = str(tmp_path / "rings.h5msm")
        msm.convert(source, to_form=item)
        original = (tmp_path / "rings.h5msm").read_bytes()
    elif form == "composite":
        item = [source.topology, source.chemical_states, source.structures]
    else:
        item = source
    expected = calculate(aromatic_case, item, **kwargs)
    assert expected.n_interactions == 2
    if slot in {"first", "both"}:
        kwargs["selection"] = external(first)
    if slot in {"second", "both"}:
        kwargs["selection_2"] = external(second)
    actual = calculate(aromatic_case, item, syntax="MDTraj", **kwargs)
    same_result(actual, expected)
    assert actual.evaluated_structure_indices.tolist() == [0, 1, 2]
    assert actual.query(structure_indices=1).n_interactions == 0
    if form == "h5msm":
        assert (tmp_path / "rings.h5msm").read_bytes() == original
    pd.testing.assert_frame_equal(source.topology.atoms, atoms, check_frame_type=False)
    for state, before in zip(source.chemical_states._states, bonds):
        pd.testing.assert_frame_equal(state.bonds, before, check_frame_type=False)
    assert source.chemical_states.reference_chemical_state_index == 1
    assert source._get_structure_chemical_state_indices(resolved=True).tolist() == [
        0,
        0,
        0,
    ]


@pytest.mark.parametrize("chemical_state", [0, 1, "structure"])
def test_external_explicit_state_restriction_remains(aromatic_case, chemical_state):
    source = aromatic_case[0]
    indices = list(range(source.topology.n_atoms))
    assert (
        calculate(
            aromatic_case, source, selection=indices, chemical_state=chemical_state
        ).n_interactions
        == 2
    )
    with pytest.raises(ArgumentError):
        calculate(
            aromatic_case,
            source,
            selection=external(indices),
            syntax="MDTraj",
            chemical_state=chemical_state,
        )
    assert source.chemical_states.reference_chemical_state_index == 1


def test_rich_h5msm_selection_still_rejects_forced_streaming(aromatic_case, tmp_path):
    source = aromatic_case[0]
    filename = str(tmp_path / "rings.h5msm")
    msm.convert(source, to_form=filename)
    with pytest.raises(UnsupportedHeavyOperationError):
        calculate(
            aromatic_case,
            filename,
            selection=external(range(source.topology.n_atoms)),
            syntax="MDTraj",
            heavy_mode="force",
        )
