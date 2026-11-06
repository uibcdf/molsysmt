"""Independent composition, geometry and ownership checks for native ion addition."""

from itertools import product

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError

puw = msm.pyunitwizard


@pytest.fixture
def water():
    return msm.build.make_water_box(puw.quantity(2 * np.eye(3), "nm"))


def small_water(points, box=None):
    source = msm.build.make_water_box(puw.quantity(2 * np.eye(3), "nm"))
    source = msm.extract(source, selection=np.arange(3 * len(points)))
    xyz = np.asarray(points)[:, None, :] + np.array(
        [[0, 0, 0], [0.04, 0, 0], [0, 0.04, 0]]
    )
    source.structures.coordinates = puw.quantity(xyz.reshape(1, -1, 3), "nm")
    source.structures.box = puw.quantity(
        np.asarray(3 * np.eye(3) if box is None else box)[None, :, :], "nm"
    )
    return source


def test_exact_counts_whole_waters_and_maps(water):
    before = puw.get_value(water.structures.coordinates).copy()
    result = msm.build.add_ions(
        water, n_cations=np.int64(2), n_anions=3, random_seed=19, return_report=True
    )
    output, report = result["molecular_system"], result["report"]
    assert msm.get(output, n_ions=True, n_waters=True, n_atoms=True) == [5, 263, 794]
    assert report["added"] == dict(cation=2, anion=3, salt_pairs=0, total=5)
    removed = report["removed_atom_indices"]
    assert len(removed) == 15
    old2new, new2old = (
        report["source_to_output_atom_indices"],
        report["output_to_source_atom_indices"],
    )
    assert old2new.shape == (804,)
    assert new2old.shape == (794,)
    assert np.all(old2new[removed] == -1)
    assert np.all(new2old[-5:] == -1)
    retained = new2old[new2old >= 0]
    np.testing.assert_array_equal(old2new[retained], np.arange(len(retained)))
    np.testing.assert_array_equal(
        puw.get_value(output.structures.coordinates)[0, : len(retained)],
        before[0, retained],
    )
    np.testing.assert_array_equal(puw.get_value(water.structures.coordinates), before)
    assert water.chemical_states._states[0]._preparation_history == []
    assert (
        output.topology.atoms["atom_id"].map(lambda value: isinstance(value, str)).all()
    )
    np.testing.assert_array_equal(
        output.chemical_states._states[0].atom_attributes["formal_charge"].tail(5),
        [1, 1, -1, -1, -1],
    )
    assert output.molecular_mechanics.partial_charge is None
    composed = msm.basic.compose_atom_maps([report])
    np.testing.assert_array_equal(composed["source_to_output_atom_indices"], old2new)
    report["source_to_output_atom_indices"][:] = -3
    assert not np.any(
        output.chemical_states._states[0]._preparation_history[-1]["report"][
            "source_to_output_atom_indices"
        ]
        == -3
    )


def test_reproducible_seed_and_fresh_seed_report(water):
    first = msm.build.add_ions(water, n_cations=3, random_seed=12, return_report=True)
    second = msm.build.add_ions(water, n_cations=3, random_seed=12)
    np.testing.assert_array_equal(
        puw.get_value(first["molecular_system"].structures.coordinates),
        puw.get_value(second.structures.coordinates),
    )
    fresh = msm.build.add_ions(water, n_anions=2, return_report=True)
    repeated = msm.build.add_ions(
        water, n_anions=2, random_seed=int(fresh["report"]["random"]["seed"])
    )
    np.testing.assert_array_equal(
        puw.get_value(fresh["molecular_system"].structures.coordinates),
        puw.get_value(repeated.structures.coordinates),
    )


@pytest.mark.parametrize("charge,counts", [(0, [0, 0]), (2, [0, 2]), (-2, [2, 0])])
def test_neutralization_declared_and_stored(water, charge, counts):
    water.topology.molecules.loc[0, "molecule_type"] = "small molecule"
    water.topology.groups.loc[0, "group_type"] = "small molecule"
    values = np.zeros(water.topology.n_atoms, dtype=np.int16)
    values[0] = charge
    water.chemical_states._states[0].set_atom_attribute("formal_charge", values)
    result = msm.build.add_ions(
        water,
        n_anions="neutralize",
        n_cations="neutralize",
        random_seed=4,
        return_report=True,
    )
    report = result["report"]
    assert [report["added"]["cation"], report["added"]["anion"]] == counts
    assert report["charge"]["source"] == "chemical_states.formal_charge"
    assert report["charge"]["output_total_elementary_charge"] == 0
    charges = (
        result["molecular_system"]
        .chemical_states._states[0]
        .atom_attributes["formal_charge"]
    )
    assert charges.sum() == 0
    explicit = msm.build.add_ions(
        water,
        n_anions="neutralize",
        n_cations="neutralize",
        expected_total_charge=charge,
        random_seed=4,
        return_report=True,
    )
    assert explicit["report"]["charge"]["source"] == "caller_declaration"


def test_mixed_counts_and_charge_constraints(water):
    result = msm.build.add_ions(
        water,
        n_cations=2,
        n_anions="neutralize",
        expected_total_charge=1,
        random_seed=8,
        return_report=True,
    )
    assert result["report"]["added"]["anion"] == 3
    with pytest.raises(StructuralInconsistencyError, match="cannot neutralize"):
        msm.build.add_ions(
            water, n_anions="neutralize", n_cations=0, expected_total_charge=-1
        )
    with pytest.raises(
        StructuralInconsistencyError, match="requires complete formal charges"
    ):
        msm.build.add_ions(water, n_anions="neutralize", n_cations="neutralize")
    with pytest.raises(StructuralInconsistencyError, match="fractional"):
        msm.build.add_ions(
            water, n_anions="neutralize", expected_total_charge=puw.quantity(0.2, "e")
        )


def test_additional_salt_water_count_convention(water):
    result = msm.build.add_ions(
        water,
        n_cations=1,
        n_anions=1,
        ionic_strength="0.55 molar",
        random_seed=3,
        return_report=True,
    )
    # 266 remaining waters * 0.55/55.4 = 2.64079..., rounded half up to 3.
    assert result["report"]["added"] == dict(cation=4, anion=4, salt_pairs=3, total=8)
    assert msm.get(result["molecular_system"], n_ions=True) == 8


def test_periodic_ion_clearance_and_bounded_failure():
    water = small_water([[0.05, 1, 1], [1, 1, 1], [2, 1, 1], [2.95, 1, 1]])
    before = puw.get_value(water.structures.coordinates).copy()
    # Opposite faces are only 0.1 nm apart; Euclidean-only placement would fit 4.
    with pytest.raises(StructuralInconsistencyError, match="bounded random greedy"):
        msm.build.add_ions(
            water, n_cations=4, min_ion_distance="0.3 nm", random_seed=2, max_attempts=2
        )
    np.testing.assert_array_equal(puw.get_value(water.structures.coordinates), before)
    assert water.chemical_states._states[0]._preparation_history == []
    output = msm.build.add_ions(
        water, n_cations=3, min_ion_distance="0.3 nm", random_seed=2
    )
    xyz = puw.get_value(output.structures.coordinates)[0, -3:]
    shifts = np.array(list(product([-1, 0, 1], repeat=3))) @ (3 * np.eye(3))
    for i in range(3):
        for j in range(i):
            assert np.linalg.norm(xyz[i] - xyz[j] + shifts, axis=1).min() > 0.3


def test_source_clearance_uses_periodic_image():
    water = small_water([[2.95, 1, 1], [0.05, 1, 1], [1.5, 1, 1]])
    water.topology.molecules.loc[0, "molecule_type"] = "small molecule"
    water.topology.groups.loc[0, "group_type"] = "small molecule"
    result = msm.build.add_ions(
        water,
        n_anions=1,
        min_solute_distance="0.3 nm",
        random_seed=9,
        return_report=True,
    )
    np.testing.assert_array_equal(
        result["report"]["removed_water_molecule_indices"], [2]
    )
    np.testing.assert_allclose(
        puw.get_value(result["molecular_system"].structures.coordinates)[0, -1],
        [1.5, 1, 1],
    )


@pytest.mark.parametrize(
    "name,value",
    [
        ("n_cations", -1),
        ("n_anions", True),
        ("n_anions", 1.2),
        ("random_seed", -1),
        ("random_seed", False),
        ("max_attempts", 0),
        ("min_solute_distance", "0 nm"),
        ("min_ion_distance", "1 ps"),
        ("ionic_strength", "-0.1 molar"),
        ("cation", "Ca2+"),
        ("charge_source", "guess"),
        ("skip_digestion", 1),
    ],
)
def test_invalid_requests(water, name, value):
    with pytest.raises(ArgumentError):
        msm.build.add_ions(water, **{name: value})


def test_zero_and_capacity_preserve_source(water):
    no_op = msm.build.add_ions(water, random_seed=0, return_report=True)
    assert no_op["molecular_system"] is not water
    assert no_op["report"]["random"]["attempts"] == 0
    np.testing.assert_array_equal(
        no_op["report"]["source_to_output_atom_indices"], np.arange(804)
    )
    with pytest.raises(StructuralInconsistencyError, match="exceeds"):
        msm.build.add_ions(water, n_anions=269)
    assert msm.get(water, n_atoms=True) == 804


def test_foreign_form_and_equivalent_units(water):
    pytest.importorskip("mdtraj")
    other = msm.convert(water, to_form="mdtraj.Trajectory")
    expected = msm.build.add_ions(water, n_cations=2, random_seed=6)
    observed = msm.build.add_ions(
        other,
        n_cations=2,
        random_seed=6,
        min_solute_distance="5 angstrom",
        min_ion_distance="5 angstrom",
    )
    np.testing.assert_allclose(
        puw.get_value(expected.structures.coordinates),
        puw.get_value(observed.structures.coordinates),
        atol=1e-7,
    )
    assert puw.get_unit(observed.structures.coordinates) == puw.unit("nm")


def test_report_persists_in_h5msm(water, tmp_path):
    result = msm.build.add_ions(water, n_anions=1, random_seed=5, return_report=True)
    path = str(tmp_path / "ions.h5msm")
    msm.convert(result["molecular_system"], to_form=path)
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    record = loaded.chemical_states._states[0]._preparation_history[-1]["report"]
    assert record["schema"] == "molsysmt.ion_replacement@1"
    assert record["random"] == result["report"]["random"]
    assert record["software"] == result["report"]["software"]
    np.testing.assert_array_equal(
        record["source_to_output_atom_indices"],
        result["report"]["source_to_output_atom_indices"],
    )


def test_stored_partial_charge_and_conflicting_declaration(water):
    water.topology.molecules.loc[0, "molecule_type"] = "small molecule"
    charges = np.zeros(water.topology.n_atoms)
    charges[0] = -1
    msm.set(water, partial_charge=puw.quantity(charges, "e"))
    result = msm.build.add_ions(
        water,
        n_anions="neutralize",
        n_cations="neutralize",
        charge_source="partial_charge",
        random_seed=4,
        return_report=True,
    )
    assert result["report"]["charge"]["source"] == "molecular_mechanics.partial_charge"
    assert result["report"]["added"]["cation"] == 1
    water.chemical_states._states[0].set_atom_attribute(
        "formal_charge", charges.astype(np.int16)
    )
    with pytest.raises(StructuralInconsistencyError, match="conflicts"):
        msm.build.add_ions(water, n_cations="neutralize", expected_total_charge=0)


def test_declared_charged_water_is_not_neutral_solvent(water):
    charges = np.zeros(water.topology.n_atoms, dtype=np.int16)
    charges[0] = 1
    water.chemical_states._states[0].set_atom_attribute("formal_charge", charges)
    with pytest.raises(StructuralInconsistencyError, match="charged water"):
        msm.build.add_ions(water, n_anions=1)


def test_named_analyses_are_invalidated_only_after_actual_atom_edits(water):
    analysis = msm.Interactions.from_records(
        [],
        n_atoms=804,
        n_structures=1,
        evaluated_structure_indices=[0],
        method="synthetic_empty_coverage",
    )
    water.interactions = {"observations": analysis}
    unchanged = msm.build.add_ions(water, random_seed=1)
    changed = msm.build.add_ions(water, n_cations=1, random_seed=1)
    assert unchanged.interactions["observations"].query([0]).to_dict()[
        "evaluated_structure_indices"
    ].tolist() == [0]
    assert changed.interactions["observations"].n_atoms == 802
    assert (
        changed.interactions["observations"]
        .query([0])
        .to_dict()["evaluated_structure_indices"]
        .size
        == 0
    )
    assert water.interactions["observations"].query([0]).to_dict()[
        "evaluated_structure_indices"
    ].tolist() == [0]


def test_tilted_periodic_ion_geometry_uses_lattice_images():
    box = np.array([[3.0, 0.0, 0.0], [1.0, 2.8, 0.0], [0.5, 0.3, 2.5]])
    fractions = np.array(
        [[0.02, 0.5, 0.5], [0.98, 0.5, 0.5], [0.5, 0.2, 0.2], [0.5, 0.8, 0.8]]
    )
    source = small_water(fractions @ box, box=box)
    result = msm.build.add_ions(
        source, n_cations=3, min_ion_distance="0.4 nm", random_seed=7
    )
    points = puw.get_value(result.structures.coordinates)[0, -3:]
    shifts = np.array(list(product([-2, -1, 0, 1, 2], repeat=3))) @ box
    for i in range(3):
        for j in range(i):
            assert np.linalg.norm(points[i] - points[j] + shifts, axis=1).min() > 0.4


def test_invalid_source_axes_and_box(water):
    with pytest.raises(StructuralInconsistencyError, match="exactly one structure"):
        msm.build.add_ions(msm.convert(water, structure_indices=[]))
    water.structures.box = None
    with pytest.raises(StructuralInconsistencyError):
        msm.build.add_ions(water, n_cations=1)


def test_attribution_reports_inspiration_without_executing_openmm(water, monkeypatch):
    from molsysmt import _ackredit

    calls = []
    monkeypatch.setattr(
        _ackredit,
        "credit",
        lambda provider, items, target, **kw: calls.append((items, target)),
    )
    result = msm.build.add_ions(water, n_cations=1, random_seed=2, return_report=True)
    assert len(calls) == 1
    reference = result["report"]["references"][0]
    assert reference["roles"] == ["methodological_inspiration"]
    assert "ba0aa236" in reference["url"]
    assert set(result["report"]["software"]) == {"molsysmt", "numpy"}
    assert calls[0][1] == "molsysmt.build.add_ions"


@pytest.mark.parametrize("length_unit", ["nm", "angstrom", "pm"])
def test_application_unit_policy_is_preserved(water, length_unit):
    expected = msm.build.add_ions(water, n_anions=2, random_seed=11)
    with puw.context(standard_units=[length_unit, "ps", "radians"]):
        policy = puw.configure.get_standard_units()
        observed = msm.build.add_ions(
            water,
            n_anions=2,
            random_seed=11,
            min_ion_distance="5 angstrom",
            min_solute_distance="500 pm",
        )
        assert puw.configure.get_standard_units() == policy
        assert puw.get_unit(observed.structures.coordinates) == puw.unit("nm")
    np.testing.assert_allclose(
        puw.get_value(expected.structures.coordinates),
        puw.get_value(observed.structures.coordinates),
        atol=1e-12,
    )


@pytest.mark.parametrize(
    "species,element,charge",
    [
        ("Na+", "Na", 1),
        ("K+", "K", 1),
        ("Li+", "Li", 1),
        ("Rb+", "Rb", 1),
        ("Cs+", "Cs", 1),
        ("Cl-", "Cl", -1),
        ("Br-", "Br", -1),
        ("F-", "F", -1),
        ("I-", "I", -1),
    ],
)
def test_supported_monatomic_species(water, species, element, charge):
    request = (
        dict(cation=species, n_cations=1)
        if charge > 0
        else dict(anion=species, n_anions=1)
    )
    output = msm.build.add_ions(water, random_seed=9, **request)
    assert msm.get(output, n_ions=True) == 1
    assert output.topology.atoms.iloc[-1]["atom_type"] == element
    assert (
        output.chemical_states._states[0].atom_attributes.iloc[-1]["formal_charge"]
        == charge
    )


def test_counts_are_additional_and_respect_existing_ions(water):
    first = msm.build.add_ions(water, n_cations=1, random_seed=4)
    second = msm.build.add_ions(first, n_cations=1, random_seed=4)
    assert msm.get(first, n_ions=True) == 1
    assert msm.get(second, n_ions=True) == 2
    positions = puw.get_value(second.structures.coordinates)[0, -2:]
    shifts = np.array(list(product([-1, 0, 1], repeat=3))) @ (2 * np.eye(3))
    assert np.linalg.norm(positions[1] - positions[0] + shifts, axis=1).min() > 0.5
