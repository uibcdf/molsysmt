"""Resolve crystallographic observations consistently before publishing edits."""

from copy import deepcopy

import numpy as np
import pytest

import molsysmt as msm

puw = msm.pyunitwizard
solve = msm.build.solve_atoms_with_alternate_location


@pytest.fixture
def molsys():
    builder = msm.MolSysBuilder()
    for atom in range(3):
        builder.add_atom(atom_name=f"C{atom}", atom_type="C", atom_id=str(atom * 10))
    builder.set_coordinates(puw.quantity(np.zeros((4, 3, 3)), "nm"))
    result = builder.build()
    result.structures.b_factor = puw.quantity(np.full((4, 3), 0.1), "nm**2")
    result.structures.occupancy = np.full((4, 3), 0.4)
    result.structures.alternate_location = [
        {
            atom: {
                "location_id": np.array(["A", "B"]),
                "occupancy": np.array([0.2, 0.5]),
                "atom_id": np.array([str(atom * 10 + 1), str(atom * 10 + 2)]),
                "coordinates": puw.quantity(
                    [
                        [structure + atom + 0.1, 0.2, 0.3],
                        [structure + atom + 0.4, 0.5, 0.6],
                    ],
                    "nm",
                ),
                "b_factor": puw.quantity([0.12, 0.24], "nm**2"),
            }
            for atom in (0, 2)
        }
        for structure in range(4)
    ]
    result.interactions = {
        "test": msm.Interactions.from_records(
            [],
            n_atoms=3,
            n_structures=4,
            evaluated_structure_indices=[0, 1, 2, 3],
            method="test.alternates",
        )
    }
    return result


def snapshot(molsys):
    return (
        puw.get_value(molsys.structures.coordinates, to_unit="nm").copy(),
        puw.get_value(molsys.structures.b_factor, to_unit="nm**2").copy(),
        molsys.structures.occupancy.copy(),
        msm.get(molsys, element="atom", atom_id=True),
        molsys.interactions["test"],
        deepcopy(molsys.structures.alternate_location),
    )


def assert_unchanged(molsys, before):
    current = snapshot(molsys)
    for actual, expected in zip(current[:4], before[:4], strict=True):
        np.testing.assert_equal(actual, expected)
    assert current[4] is before[4]
    for actual, expected in zip(current[5], before[5], strict=True):
        for atom in expected:
            for name, value in expected[atom].items():
                if puw.is_quantity(value):
                    np.testing.assert_equal(
                        puw.get_value(actual[atom][name], to_unit=puw.get_unit(value)),
                        puw.get_value(value),
                    )
                else:
                    np.testing.assert_equal(actual[atom][name], value)


@pytest.mark.parametrize(
    "labels,occupancies,expected",
    [
        (["A", "B"], [0.2, 0.5], "B"),
        (["B", "A"], [0.5, 0.2], "B"),
        (["B", "A"], [0.5, 0.5], "A"),
        (["B", "A"], [0.5, 0.49], "B"),
        (["C", "B"], [0.5, 0.5], "C"),
        (["B", "A"], [0.3, 0.3], "B"),
        (["A", "B"], [np.nan, 0.5], "B"),
    ],
)
def test_maximum_occupancy_only_prefers_a_when_it_shares_the_half_tie(
    molsys, labels, occupancies, expected
):
    site = molsys.structures.alternate_location[0][0]
    site["location_id"] = np.array(labels)
    site["occupancy"] = np.array(occupancies)
    expected_position = labels.index(expected)
    expected_coordinates = puw.get_value(site["coordinates"], to_unit="nm")[
        expected_position
    ]
    expected_id = site["atom_id"][expected_position]
    solve(molsys, selection=[0], structure_indices=[0])
    np.testing.assert_allclose(
        puw.get_value(molsys.structures.coordinates, to_unit="nm")[0, 0],
        expected_coordinates,
    )
    assert msm.get(molsys, element="atom", selection=[0], atom_id=True) == [expected_id]


@pytest.mark.parametrize("location", ["B", "occupancy"])
def test_selected_primary_observation_includes_its_occupancy(molsys, location):
    solve(molsys, selection=[0], structure_indices=[2, 0, 2], location_id=location)
    np.testing.assert_equal(molsys.structures.occupancy[:, 0], [0.5, 0.4, 0.5, 0.4])
    np.testing.assert_equal(molsys.structures.occupancy[:, 1:], np.full((4, 2), 0.4))
    np.testing.assert_equal(
        puw.get_value(molsys.structures.b_factor, to_unit="nm**2")[:, 0],
        [0.24, 0.1, 0.24, 0.1],
    )
    np.testing.assert_array_equal(
        molsys.interactions["test"].evaluated_structure_indices, [1, 3]
    )


def test_invalid_later_structure_is_rejected_before_any_publication(molsys):
    molsys.structures.alternate_location[2][0]["location_id"] = np.array(["A", "C"])
    before = snapshot(molsys)
    with pytest.raises(msm.ArgumentChoiceError) as refusal:
        solve(molsys, selection=[0], structure_indices=[0, 2], location_id="B")
    assert refusal.value.extra["argument"] == "location_id"
    assert refusal.value.extra["choices"] == ["A", "C"]
    assert_unchanged(molsys, before)


@pytest.mark.parametrize("structures", [[2, 0], [0, 2, 0], [2]])
def test_missing_first_or_later_location_preserves_the_complete_input(
    molsys, structures
):
    molsys.structures.alternate_location[2][2]["location_id"] = np.array(["A", "C"])
    before = snapshot(molsys)
    with pytest.raises(msm.ArgumentChoiceError):
        solve(molsys, selection=[2, 0], structure_indices=structures, location_id="B")
    assert_unchanged(molsys, before)


@pytest.mark.parametrize("field", ["occupancy", "coordinates", "b_factor"])
def test_invalid_later_site_payload_is_preflighted(molsys, field):
    site = molsys.structures.alternate_location[2][0]
    if field == "occupancy":
        site[field] = np.array([-0.1, 0.5])
    elif field == "coordinates":
        site[field] = puw.quantity([[0.1, 0.2, 0.3], [np.nan, 0.5, 0.6]], "nm")
    else:
        site[field] = puw.quantity([0.12], "nm**2")
    before = snapshot(molsys)
    with pytest.raises(msm.ArgumentError):
        solve(molsys, selection=[0], structure_indices=[0, 2], location_id="B")
    assert_unchanged(molsys, before)


def test_location_vector_follows_selection_order(molsys):
    solve(molsys, selection=[2, 0], structure_indices=[0], location_id=["A", "B"])
    assert msm.get(molsys, element="atom", atom_id=True) == ["2", "10", "21"]


def test_wrong_location_vector_length_has_an_argument_diagnostic(molsys):
    before = snapshot(molsys)
    with pytest.raises(msm.ArgumentLengthError):
        solve(molsys, selection=[2, 0], location_id=["A"])
    assert_unchanged(molsys, before)


@pytest.mark.parametrize("indices", [[0, 9], [0, -1]])
def test_out_of_bounds_structure_request_is_rejected_before_writes(molsys, indices):
    before = snapshot(molsys)
    with pytest.raises(msm.ArgumentError):
        solve(molsys, structure_indices=indices, location_id="B")
    assert_unchanged(molsys, before)


@pytest.mark.parametrize(
    "occupancy", [None, [np.nan, np.nan], [0.2, np.inf], [0.2, 1.1]]
)
def test_occupancy_policy_refuses_unavailable_or_invalid_evidence(molsys, occupancy):
    molsys.structures.alternate_location[2][0]["occupancy"] = occupancy
    before = snapshot(molsys)
    with pytest.raises(msm.ArgumentError):
        solve(molsys, selection=[0], structure_indices=[0, 2])
    assert_unchanged(molsys, before)


def test_explicit_location_can_preserve_unknown_occupancy(molsys):
    molsys.structures.alternate_location[0][0]["occupancy"] = None
    solve(molsys, selection=[0], structure_indices=[0], location_id="B")
    assert np.isnan(molsys.structures.occupancy[0, 0])


@pytest.mark.parametrize("attribute", ["occupancy", "b_factor"])
def test_absent_or_integer_primary_storage_retains_fractional_values(molsys, attribute):
    setattr(molsys.structures, attribute, None)
    coordinates = molsys.structures._coordinates
    solve(molsys, selection=[0], structure_indices=[0], location_id="B")
    values = getattr(molsys.structures, attribute)
    if attribute == "b_factor":
        values = puw.get_value(values, to_unit="nm**2")
    assert values[0, 0] == (0.5 if attribute == "occupancy" else 0.24)
    assert np.isnan(values[3, 2])
    assert molsys.structures._coordinates is not coordinates
    values = np.ones((4, 3), dtype=int)
    setattr(
        molsys.structures,
        attribute,
        values if attribute == "occupancy" else puw.quantity(values, "nm**2"),
    )
    solve(molsys, selection=[0], structure_indices=[0], location_id="B")
    actual = getattr(molsys.structures, attribute)
    if attribute == "b_factor":
        actual = puw.get_value(actual, to_unit="nm**2")
    assert actual[0, 0] == (0.5 if attribute == "occupancy" else 0.24)
    assert actual[3, 2] == 1


def test_missing_stable_domain_rejects_before_geometry_changes(molsys):
    from molsysmt._private.smonitor import NotWithThisFormError

    before = snapshot(molsys)
    with pytest.raises(NotWithThisFormError):
        solve(molsys.structures, selection=[0], structure_indices=[0], location_id="B")
    assert_unchanged(molsys, before)


def test_alternate_quantity_units_are_converted_explicitly(molsys):
    site = molsys.structures.alternate_location[0][0]
    site["coordinates"] = puw.quantity([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], "angstrom")
    site["b_factor"] = puw.quantity([12.0, 24.0], "angstrom**2")
    with puw.context(standard_units=["pm", "fs"]):
        solve(molsys, selection=[0], structure_indices=[0], location_id="B")
    np.testing.assert_allclose(
        puw.get_value(molsys.structures.coordinates, to_unit="nm")[0, 0],
        [0.4, 0.5, 0.6],
    )
    assert puw.get_value(molsys.structures.b_factor, to_unit="nm**2")[
        0, 0
    ] == pytest.approx(0.24)


@pytest.mark.parametrize("skip", [False, True])
def test_validated_delegation_keeps_site_preflight(molsys, skip):
    molsys.structures.alternate_location[2][0]["location_id"] = np.array(["A", "C"])
    before = snapshot(molsys)
    with pytest.raises(msm.ArgumentChoiceError):
        solve(
            molsys,
            selection=[0],
            structure_indices=[0, 2],
            location_id="B",
            skip_digestion=skip,
        )
    assert_unchanged(molsys, before)


def test_missing_selected_b_factor_becomes_unknown(molsys):
    molsys.structures.alternate_location[0][0]["b_factor"] = None
    solve(molsys, selection=[0], structure_indices=[0], location_id="B")
    assert np.isnan(puw.get_value(molsys.structures.b_factor, to_unit="nm**2")[0, 0])


@pytest.mark.parametrize(
    "field,unit,values",
    [
        ("coordinates", "nm**2", [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]]),
        ("b_factor", "nm", [0.1, 0.2]),
    ],
)
def test_incompatible_alternate_units_have_prewrite_catalog_diagnostics(
    molsys, field, unit, values
):
    molsys.structures.alternate_location[2][0][field] = puw.quantity(values, unit)
    before = snapshot(molsys)
    with pytest.raises(msm.ArgumentError) as refusal:
        solve(molsys, selection=[0], structure_indices=[0, 2], location_id="B")
    assert refusal.value.extra["argument"] == "alternate_location"
    assert_unchanged(molsys, before)


@pytest.mark.parametrize("locations", [["A", "B"], np.array([["A"], ["B"]])])
def test_conflicting_repeated_atoms_and_nonflat_labels_reject(molsys, locations):
    before = snapshot(molsys)
    with pytest.raises(msm.ArgumentError):
        solve(molsys, selection=[0, 0], location_id=locations)
    assert_unchanged(molsys, before)


def test_distinct_structure_atom_labels_require_a_stable_choice(molsys):
    molsys.structures.alternate_location[2][0]["atom_id"][1] = "99"
    before = snapshot(molsys)
    with pytest.raises(msm.ArgumentError):
        solve(molsys, selection=[0], structure_indices=[2, 0], location_id="B")
    assert_unchanged(molsys, before)


def test_composite_forms_use_their_existing_attribute_owners(molsys):
    solve(
        [molsys.topology, molsys.structures],
        selection=[0],
        structure_indices=[2],
        location_id="B",
    )
    assert molsys.topology.atoms.atom_id.tolist()[0] == "2"
    assert molsys.structures.occupancy[2, 0] == 0.5


@pytest.mark.parametrize("empty", ["atoms", "structures"])
def test_empty_selection_changes_no_domain(molsys, empty):
    before = snapshot(molsys)
    solve(
        molsys, **({"selection": []} if empty == "atoms" else {"structure_indices": []})
    )
    assert_unchanged(molsys, before)


def test_resolution_preserves_source_alternate_records_and_serialization(
    molsys, tmp_path
):
    records = deepcopy(molsys.structures.alternate_location)
    solve(molsys, selection=[0], structure_indices=[2, 0], location_id="B")
    filename = tmp_path / "alternate.h5msm"
    msm.convert(molsys, to_form=filename)
    restored = msm.convert(filename)
    np.testing.assert_equal(restored.structures.occupancy, molsys.structures.occupancy)
    for structure in range(4):
        np.testing.assert_equal(
            molsys.structures.alternate_location[structure][0]["occupancy"],
            records[structure][0]["occupancy"],
        )
        np.testing.assert_equal(
            restored.structures.alternate_location[structure][0]["occupancy"],
            records[structure][0]["occupancy"],
        )
