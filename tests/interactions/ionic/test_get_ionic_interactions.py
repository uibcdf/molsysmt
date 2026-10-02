"""Checking the bounded ionic criterion against explicit analytical geometry."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import (
    ArgumentError,
    NotImplementedMethodError,
    StructuralInconsistencyError,
    UnsupportedHeavyOperationError,
)
from molsysmt.native import MolSys, Topology


def _system(elements, charges, xyz, bonds=(), orders=(), box=None):
    molsys = MolSys()
    molsys.topology = Topology(n_atoms=len(elements))
    molsys.topology.atoms["atom_type"] = elements
    molsys.topology.atoms["atom_id"] = [f"atom-{100 + i}" for i in range(len(elements))]
    msm.set(molsys, element="atom", formal_charge=charges)
    if bonds:
        molsys.topology._append_chemical_state_bonds(
            bonds, orders=orders, types="covalent"
        )
    molsys.topology._reference_chemical_state.connectivity_completeness = "complete"
    molsys.structures.append(
        coordinates=puw.quantity(np.asarray(xyz, dtype=float), "nm"),
        box=None if box is None else puw.quantity(np.asarray(box, dtype=float), "nm"),
    )
    return molsys


def _ions():
    xyz = [
        [[0, 0, 0], [0.3, 0, 0], [0.6, 0, 0]],
        [[0, 0, 0], [2, 0, 0], [4, 0, 0]],
        [[0, 0, 0], [0.2, 0, 0], [0.8, 0, 0]],
    ]
    molsys = _system(["Na", "Cl", "K"], [1, -1, 1], xyz)
    molsys.structures.structure_id = np.array(["frame-90", "frame-12", "frame-500"])
    return molsys


def _calculate(molsys, **kwargs):
    return msm.interactions.ionic.get_ionic_interactions(
        molsys, "0.4 nm", pbc=False, **kwargs
    )


def test_nonconsecutive_repeated_frames_variable_counts_and_empty_coverage():
    result = _calculate(_ions(), structure_indices=[2, 0, 2, 1])
    assert result.evaluated_structure_indices.tolist() == [0, 1, 2]
    assert result.occurrence_structures.tolist() == [0, 0, 2]
    assert result.n_structures == 3 and result.n_atoms == 3
    np.testing.assert_allclose(result.measurements["distance"], [0.3, 0.3, 0.2])
    assert result.query(structure_indices=1).n_interactions == 0
    assert result.query(structure_indices=1).to_dict()[
        "evaluated_structure_indices"
    ].tolist() == [1]
    assert result.participant_roles == ("positive", "negative", "positive", "negative")
    assert result.atom_source_indices.tolist() == [0, 1, 2]
    assert result.software["molsysmt"] == msm.__version__
    assert result.measure_units == {
        "distance": "nm",
        "positive_charge": "e",
        "negative_charge": "e",
    }


@pytest.mark.parametrize(
    ("mode", "selection", "second", "count"),
    [
        ("internal", [0], None, 0),
        ("internal", [0, 1], None, 2),
        ("incident", [1], None, 3),
        ("incident", [2], None, 1),
        ("between", [0, 2], [1], 3),
        ("between", [0], [2], 0),
    ],
)
def test_calculation_scope_and_combined_queries(mode, selection, second, count):
    result = _calculate(
        _ions(), selection=selection, selection_2=second, selection_mode=mode
    )
    assert result.n_interactions == count
    assert result.evaluation_mode == mode
    assert (
        result.query(structure_indices=[2, 0], atom_indices=[0]).n_interactions <= count
    )


def test_minimum_distance_uses_oxygen_references_but_queries_include_whole_center():
    # Carbon is closer to Na than either oxygen; only oxygen distances count.
    xyz = [[[0.1, 0, 0], [0.3, 0, 0], [0.3, 0.1, 0], [0, 0, 0]]]
    molsys = _system(
        ["C", "O", "O", "Na"], [0, -1, 0, 1], xyz, [(0, 1), (0, 2)], [1, 2]
    )
    result = _calculate(molsys)
    assert result.n_interactions == 1
    assert result.relation(0)["participants"][1]["atom_indices"].tolist() == [0, 1, 2]
    np.testing.assert_allclose(result.measurements["distance"], [0.3])
    np.testing.assert_allclose(result.measurements["positive_charge"], [1])
    np.testing.assert_allclose(result.measurements["negative_charge"], [-1])
    assert result.query(atom_indices=[0], mode="incident").n_interactions == 1
    assert result.query(atom_indices=[0, 1, 2], mode="internal").n_interactions == 0
    with pytest.raises(ArgumentError, match="cuts a compound"):
        _calculate(molsys, selection=[1, 2], selection_mode="incident")
    assert not molsys.interactions


@pytest.mark.parametrize("distance", [0.399999, 0.4, 0.400001])
def test_cutoff_is_inclusive_and_threshold_units_are_explicit(distance):
    molsys = _system(["Na", "Cl"], [1, -1], [[[0, 0, 0], [distance, 0, 0]]])
    result = msm.interactions.ionic.get_ionic_interactions(
        molsys, "4 angstrom", pbc=False
    )
    assert result.n_interactions == int(distance <= 0.4)
    assert result.parameters["distance_threshold"]["unit"] == "nm"
    assert result.parameters["distance_threshold"]["value"] == pytest.approx(0.4)


@pytest.mark.parametrize(
    "box",
    [
        np.eye(3),
        np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]]),
        np.array([[1, 0, 0], [0.2, 0.9, 0], [0.1, 0.2, 0.8]]),
    ],
)
def test_periodic_images_reproduce_observed_distance_in_original_box(box):
    fractional = np.array([[0.1, 0.1, 0.1], [0.9, 0.1, 0.1]])
    xyz = fractional @ box
    molsys = _system(["Na", "Cl"], [1, -1], [xyz], box=[box])
    result = msm.interactions.ionic.get_ionic_interactions(molsys, "0.4 nm")
    assert result.n_interactions == 1
    assert result.image_vectors.tolist() == [[0, 0, 0], [-1, 0, 0]]
    displayed = xyz + result.image_vectors @ box
    np.testing.assert_allclose(
        np.linalg.norm(displayed[1] - displayed[0]), result.measurements["distance"][0]
    )
    np.testing.assert_allclose(result.measurements["distance"], [0.2])


def test_periodic_compound_participant_is_preserved_or_rejected_when_split():
    xyz = [[[0.95, 0, 0], [0.96, 0, 0], [0.94, 0.02, 0], [0.1, 0, 0]]]
    molsys = _system(
        ["C", "O", "O", "Na"], [0, -1, 0, 1], xyz, [(0, 1), (0, 2)], [1, 2], [np.eye(3)]
    )
    result = msm.interactions.ionic.get_ionic_interactions(molsys, "0.4 nm")
    assert result.n_interactions == 1
    assert result.image_vectors.tolist() == [[0, 0, 0], [-1, 0, 0]]
    coords = np.asarray(xyz)[0]
    oxygens = coords[[1, 2]] + result.image_vectors[1] @ np.eye(3)
    np.testing.assert_allclose(
        np.linalg.norm(oxygens - coords[3], axis=1).min(),
        result.measurements["distance"][0],
    )
    changed = np.asarray(xyz).copy()
    changed[0, 1, 0] = 0.01
    msm.set(molsys, coordinates=puw.quantity(changed, "nm"))
    with pytest.raises(NotImplementedMethodError):
        msm.interactions.ionic.get_ionic_interactions(molsys, "0.4 nm")


def test_empty_results_and_missing_chemistry_are_distinct():
    neutral = _system(["N", "O"], [1, -1], [[[0, 0, 0], [0.1, 0, 0]]], [(0, 1)], [1])
    result = _calculate(neutral)
    assert result.n_interactions == 0
    assert result.evaluated_structure_indices.tolist() == [0]
    assert all(values.shape == (0,) for values in result.measurements.values())
    msm.set(neutral, element="atom", formal_charge=[None, -1])
    with pytest.raises(StructuralInconsistencyError):
        _calculate(neutral)


def test_intramolecular_centers_are_included_but_direct_covalent_links_are_excluded():
    molsys = _system(
        ["N", "C", "O"],
        [1, 0, -1],
        [[[0, 0, 0], [0.1, 0, 0], [0.2, 0, 0]]],
        [(0, 1), (1, 2)],
        [1, 1],
    )
    assert _calculate(molsys).n_interactions == 1
    # A neutral COO motif separates charged atoms into two nonzero centers.
    molsys = _system(
        ["C", "O", "O", "N"],
        [0, -1, 0, 1],
        [[[0, 0, 0], [0.1, 0, 0], [0, 0.1, 0], [0.2, 0, 0]]],
        [(0, 1), (0, 2), (0, 3)],
        [1, 2, 1],
    )
    assert _calculate(molsys).n_interactions == 0


@pytest.mark.parametrize(
    "options",
    [
        {"selection_mode": "wrong"},
        {"selection_mode": "between"},
        {"selection_2": [1]},
        {"selection_mode": "between", "selection": [0, 1], "selection_2": [1]},
        {"method": "energy"},
        {"output_type": "tuple"},
        {"structure_indices": [10]},
    ],
)
def test_invalid_scopes_and_methods_fail(options):
    with pytest.raises(ArgumentError):
        _calculate(_ions(), **options)


@pytest.mark.parametrize(
    "threshold",
    [0.4, "-1 nm", "0 nm", "1 ps", "nan nm", puw.quantity([0.4, 0.5], "nm")],
)
def test_invalid_thresholds_do_not_return_plausible_observations(threshold):
    with pytest.raises((ArgumentError, ValueError)):
        msm.interactions.ionic.get_ionic_interactions(_ions(), threshold)


def test_selected_chemical_state_and_missing_complete_connectivity():
    molsys = _ions()
    second = molsys.chemical_states.append_state()
    molsys.topology._chemical_states[second].connectivity_completeness = "complete"
    msm.set(molsys, element="atom", formal_charge=[0, 0, 0], chemical_state=second)
    assert _calculate(molsys, chemical_state=second).n_interactions == 0
    assert _calculate(molsys, chemical_state=0).n_interactions == 3
    molsys.topology._reference_chemical_state.connectivity_completeness = "partial"
    with pytest.raises(StructuralInconsistencyError):
        _calculate(molsys)
    result = _calculate(molsys, assume_complete_connectivity=True)
    assert result.parameters["charge_evidence"]["assume_complete_connectivity"] is True


def test_dictionary_and_named_h5msm_round_trips_preserve_observations(tmp_path):
    molsys = _ions()
    result = _calculate(molsys)
    dictionary = _calculate(molsys, output_type="molsysmt.InteractionsDict")
    restored = msm.convert(dictionary, to_form="molsysmt.Interactions")
    np.testing.assert_array_equal(
        restored.occurrence_structures, result.occurrence_structures
    )
    np.testing.assert_allclose(
        restored.measurements["distance"], result.measurements["distance"]
    )
    molsys.interactions = {"ionic": result}
    path = str(tmp_path / "ionic.h5msm")
    msm.convert(molsys, to_form=path)
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    saved = loaded.interactions["ionic"]
    assert saved.parameters == result.parameters and saved.software == result.software
    np.testing.assert_array_equal(
        saved.query().to_dict()["occurrence_indices"],
        result.query().to_dict()["occurrence_indices"],
    )
    calculated = _calculate(path)
    np.testing.assert_allclose(
        calculated.measurements["distance"], result.measurements["distance"]
    )


def test_large_input_is_rejected_before_loading_coordinates(monkeypatch):
    from molsysmt.basic import get

    def checked_get(*args, **kwargs):
        if kwargs.get("coordinates"):
            raise AssertionError(
                "Coordinate loading must follow the eager budget check."
            )
        return get(*args, **kwargs)

    monkeypatch.setattr(msm.basic, "get", checked_get)
    monkeypatch.setattr(msm.configure, "max_ram_usage", 1)
    with pytest.raises(UnsupportedHeavyOperationError):
        _calculate(_ions())


def test_guandinium_carboxylate_pair_is_one_observation_with_whole_participants():
    xyz = [
        [
            [0, 0, 0],
            [0, 0.05, 0],
            [0, -0.05, 0],
            [0.05, 0, 0],
            [0.3, 0, 0],
            [0.25, 0, 0],
            [0.35, 0, 0],
        ]
    ]
    molsys = _system(
        ["C", "N", "N", "N", "C", "O", "O"],
        [0, 1, 0, 0, 0, -1, 0],
        xyz,
        [(0, 1), (0, 2), (0, 3), (4, 5), (4, 6)],
        [2, 1, 1, 1, 2],
    )
    result = _calculate(molsys)
    assert result.n_interactions == 1
    assert result.participant_atoms.tolist() == list(range(7))
    assert result.participant_atom_offsets.tolist() == [0, 4, 7]
    np.testing.assert_allclose(result.measurements["distance"], [0.2])


def test_alternate_state_connectivity_is_used_for_covalent_exclusion():
    molsys = _system(
        ["C", "O", "O", "N"],
        [0, -1, 0, 1],
        [[[0, 0, 0], [0.1, 0, 0], [0, 0.1, 0], [0.2, 0, 0]]],
        [(0, 1), (0, 2)],
        [1, 2],
    )
    second = molsys.chemical_states.append_state()
    msm.set(molsys, element="atom", formal_charge=[0, -1, 0, 1], chemical_state=second)
    molsys.topology._append_chemical_state_bonds(
        [(0, 1), (0, 2), (0, 3)], orders=[1, 2, 1], types="covalent", state_index=second
    )
    molsys.topology._chemical_states[second].connectivity_completeness = "complete"
    assert _calculate(molsys, chemical_state=0).n_interactions == 1
    assert _calculate(molsys, chemical_state=second).n_interactions == 0
    molsys._set_structure_chemical_state_indices([second])
    assert _calculate(molsys, chemical_state="structure").n_interactions == 0


def test_periodic_dictionary_round_trip_and_extract_remap(tmp_path):
    molsys = _system(
        ["Na", "Cl"], [1, -1], [[[0.1, 0, 0], [0.9, 0, 0]]], box=[np.eye(3)]
    )
    result = msm.interactions.ionic.get_ionic_interactions(molsys, "0.4 nm")
    molsys.interactions = {"ionic": result}
    path = str(tmp_path / "periodic_ions.h5msm")
    msm.convert(molsys, to_form=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys").interactions["ionic"]
    np.testing.assert_array_equal(restored.image_vectors, result.image_vectors)
    reordered = msm.extract(molsys, selection=[1, 0], structure_indices=[0])
    assert reordered.interactions["ionic"].n_interactions == 1
    remapped = result.remap(atom_indices=[1, 0])
    assert remapped.atom_source_indices.tolist() == [1, 0]
    coords = puw.get_value(msm.get(molsys, coordinates=True), to_unit="nm")[0, [1, 0]]
    relation = remapped.relation(0)
    observed = [
        coords[part["atom_indices"]] + image @ np.eye(3)
        for part, image in zip(relation["participants"], remapped.image_vectors)
    ]
    np.testing.assert_allclose(np.linalg.norm(observed[1] - observed[0]), [0.2])


def test_units_are_explicit_under_a_nondefault_session():
    molsys = _ions()
    puw.configure.set_standard_units(
        [
            "angstrom",
            "ps",
            "K",
            "mole",
            "dalton",
            "e",
            "kJ/mol",
            "kJ/(mol*nm)",
            "kJ/(mol*nm**2)",
            "radians",
        ]
    )
    result = _calculate(molsys)
    assert result.measure_units["distance"] == "nm"
    np.testing.assert_allclose(result.measurements["distance"], [0.3, 0.3, 0.2])


@pytest.mark.parametrize("bad", ["coordinates", "box"])
def test_nonfinite_geometry_fails_instead_of_claiming_empty_coverage(bad):
    molsys = _system(["Na", "Cl"], [1, -1], [[[0, 0, 0], [0.2, 0, 0]]], box=[np.eye(3)])
    if bad == "coordinates":
        coords = puw.get_value(msm.get(molsys, coordinates=True), to_unit="nm").copy()
        coords[0, 1, 0] = np.nan
        msm.set(molsys, coordinates=puw.quantity(coords, "nm"))
    else:
        msm.set(molsys, box=puw.quantity(np.zeros((1, 3, 3)), "nm"))
    with pytest.raises(StructuralInconsistencyError):
        msm.interactions.ionic.get_ionic_interactions(molsys, "0.4 nm")


def test_empty_frame_and_atom_selections_are_typed_and_do_not_attach():
    molsys = _ions()
    result = _calculate(molsys, structure_indices=[])
    assert result.n_interactions == 0 and result.evaluated_structure_indices.shape == (
        0,
    )
    result = _calculate(molsys, selection=[])
    assert (
        result.n_interactions == 0
        and result.evaluated_structure_indices.tolist() == [0, 1, 2]
    )
    assert result.participant_atoms.dtype == np.int64
    assert not molsys.interactions


def test_modular_file_budget_is_checked_before_materializing_domains(
    tmp_path, monkeypatch
):
    from molsysmt.form import _h5msm05_modular

    path = str(tmp_path / "preflight.h5msm")
    msm.convert(_ions(), to_form=path)

    def forbidden(*args, **kwargs):
        raise AssertionError(
            "Domain arrays must not load before the source budget check."
        )

    monkeypatch.setattr(_h5msm05_modular, "read_molsys_file", forbidden)
    monkeypatch.setattr(msm.configure, "max_ram_usage", 1)
    with pytest.raises(UnsupportedHeavyOperationError):
        _calculate(path, chemical_state=0, structure_indices=[0])


def test_modular_file_prepares_chemistry_once_without_materializing_structures(
    tmp_path, monkeypatch
):
    from molsysmt.form import _h5msm05_modular

    molsys = _ions()
    second = molsys.chemical_states.append_state()
    msm.set(molsys, element="atom", formal_charge=[2, -1, 1], chemical_state=second)
    molsys.topology._chemical_states[second].connectivity_completeness = "complete"
    path = str(tmp_path / "states.h5msm")
    msm.convert(molsys, to_form=path)
    original = _h5msm05_modular._read_calculation_chemistry
    calls = []

    def counted(filename, **kwargs):
        calls.append(filename)
        return original(filename, **kwargs)

    def forbidden(*args, **kwargs):
        raise AssertionError(
            "Ionic detection must not materialize full structural or interaction domains."
        )

    monkeypatch.setattr(_h5msm05_modular, "read_molsys_file", forbidden)
    monkeypatch.setattr(_h5msm05_modular, "read_independent_structures", forbidden)
    monkeypatch.setattr(_h5msm05_modular, "read_named_analyses", forbidden)
    monkeypatch.setattr(_h5msm05_modular, "_read_calculation_chemistry", counted)
    result = _calculate(path, chemical_state=second)
    assert len(calls) == 1
    assert result.parameters["chemical_state_index"] == second
    np.testing.assert_allclose(result.measurements["positive_charge"], [2, 1, 2])


def test_incident_scope_does_not_generate_unrelated_candidate_pairs(monkeypatch):
    from molsysmt.structure import _group_minimum_contacts

    original = _group_minimum_contacts.group_minimum_contacts
    counts = []

    def counted(first, labels_a, second, labels_b, *args):
        counts.append((len(first), len(second)))
        return original(first, labels_a, second, labels_b, *args)

    monkeypatch.setattr(_group_minimum_contacts, "group_minimum_contacts", counted)
    result = _calculate(_ions(), selection=[0], selection_mode="incident")
    assert result.n_interactions == 2
    assert counts == [(1, 1)] * 3
