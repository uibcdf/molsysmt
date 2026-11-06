"""Check actual OpenMM compositions instead of argument-forwarding mocks."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError

puw = msm.pyunitwizard


@pytest.fixture(scope="module")
def solute():
    pytest.importorskip("openmm")
    return msm.build.add_missing_terminal_cappings(msm.build.build_peptide("AlaValPro"))


@pytest.mark.parametrize("positive,negative", [(0, 0), (2, 2), (1, 0), (0, 1)])
def test_openmm_applies_explicit_ion_counts(solute, positive, negative):
    before = puw.get_value(solute.structures.coordinates).copy()
    result = msm.build.solvate(
        solute,
        engine="OpenMM",
        box_shape="cubic",
        clearance="0.6 nm",
        n_cations=positive,
        n_anions=negative,
        ionic_strength="0 molar",
        random_seed=13,
    )
    assert msm.get(result, n_ions=True) == positive + negative
    ions = msm.get(
        result, element="group", selection='group_type == "ion"', group_name=True
    )
    assert sum(name == "NA" for name in ions) == positive
    assert sum(name == "CL" for name in ions) == negative
    report = result.chemical_states._states[0]._preparation_history[-1]["report"]
    assert report["solvation"]["engine"] == "OpenMM"
    assert report["solvation"]["charge_source"] == "not_required"
    np.testing.assert_array_equal(puw.get_value(solute.structures.coordinates), before)
    assert msm.get(solute, n_ions=True) == 0


@pytest.mark.parametrize("sequence,sign", [("AlaLysPro", 1), ("AlaAspPro", -1)])
def test_openmm_mixed_neutralization_uses_parameterized_charge(sequence, sign):
    pytest.importorskip("openmm")
    solute = msm.build.add_missing_terminal_cappings(msm.build.build_peptide(sequence))
    kwargs = (
        dict(n_cations=2, n_anions="neutralize")
        if sign > 0
        else dict(n_anions=2, n_cations="neutralize")
    )
    result = msm.build.solvate(
        solute,
        engine="OpenMM",
        box_shape="cubic",
        clearance="0.7 nm",
        random_seed=3,
        **kwargs,
    )
    report = result.chemical_states._states[0]._preparation_history[-1]["report"]
    assert report["charge"]["total_elementary_charge"] == sign
    assert report["charge"]["output_total_elementary_charge"] == 0
    assert report["solvation"]["charge_source"] == "forcefield"
    # Independently parameterize the actual returned atom inventory.
    system = msm.convert(
        result, to_form="openmm.System", forcefield="AMBER14", water_model="TIP3P"
    )
    charge = msm.physchem.get_charge(system, definition="OpenMM", element="system")
    assert abs(float(puw.get_value(charge, to_unit="elementary_charge"))) < 1e-4


@pytest.mark.parametrize(
    "shape", ["cubic", "truncated octahedral", "rhombic dodecahedral"]
)
def test_openmm_native_placement_shapes_and_equivalent_units(solute, shape):
    first = msm.build.solvate(
        solute,
        engine="OpenMM",
        box_shape=shape,
        clearance="0.7 nm",
        n_cations=1,
        n_anions=1,
        random_seed=12,
    )
    second = msm.build.solvate(
        solute,
        engine="OpenMM",
        box_shape=shape,
        clearance="7 angstrom",
        n_cations=1,
        n_anions=1,
        random_seed=12,
    )
    assert msm.get(first, n_ions=True) == 2
    np.testing.assert_allclose(
        puw.get_value(first.structures.coordinates),
        puw.get_value(second.structures.coordinates),
        atol=1e-12,
    )
    assert first.structures.box.shape == (1, 3, 3)


def test_openmm_explicit_counts_and_salt_are_additive(solute):
    result = msm.build.solvate(
        solute,
        engine="OpenMM",
        box_shape="cubic",
        clearance="0.8 nm",
        n_cations=1,
        n_anions=1,
        ionic_strength="0.4 molar",
        random_seed=5,
    )
    report = result.chemical_states._states[0]._preparation_history[-1]["report"]
    pairs = report["added"]["salt_pairs"]
    assert pairs > 0
    assert msm.get(result, n_ions=True) == 2 + 2 * pairs


def test_four_site_waters_are_replaced_completely(solute):
    plain = msm.build.solvate(
        solute,
        engine="OpenMM",
        box_shape="cubic",
        clearance="0.7 nm",
        n_cations=0,
        n_anions=0,
        water_model="TIP4P-EW",
        random_seed=2,
    )
    result = msm.build.add_ions(
        plain, n_cations=1, n_anions=1, random_seed=3, return_report=True
    )
    assert len(result["report"]["removed_atom_indices"]) == 8
    assert msm.get(result["molecular_system"], n_ions=True) == 2


def test_native_default_charge_approximation_is_explicit():
    solute = msm.build.add_missing_terminal_cappings(
        msm.build.build_peptide("AlaLysPro")
    )
    result = msm.build.solvate(
        solute, engine="MolSysMT", box_shape="cubic", clearance="0.7 nm", random_seed=8
    )
    report = result.chemical_states._states[0]._preparation_history[-1]["report"]
    assert (
        report["solvation"]["charge_source"] == "tabulated_physical_pH7_approximation"
    )
    assert report["charge"]["total_elementary_charge"] == 1
    assert msm.get(result, n_ions=True) == 1


def test_pdbfixer_default_route_still_constructs_solvent(solute):
    pytest.importorskip("pdbfixer")
    output = msm.build.solvate(
        solute, engine="PDBFixer", box_shape="cubic", clearance="0.5 nm"
    )
    assert msm.get(output, n_waters=True) > 0
    assert msm.get(solute, n_ions=True) == 0


@pytest.mark.parametrize(
    "counts", [dict(n_anions=2, n_cations=2), dict(n_anions=0), dict(random_seed=3)]
)
def test_pdbfixer_rejects_unsupported_controls_before_construction(
    solute, monkeypatch, counts
):
    pytest.importorskip("pdbfixer")
    from pdbfixer import PDBFixer

    def forbidden(*args, **kwargs):
        raise AssertionError("Unsupported controls reached solvent construction")

    monkeypatch.setattr(PDBFixer, "addSolvent", forbidden)
    with pytest.raises(ArgumentError, match="PDBFixer supports only"):
        msm.build.solvate(solute, engine="PDBFixer", **counts)


@pytest.mark.parametrize(
    "counts",
    [
        dict(n_anions=-1),
        dict(n_cations=True),
        dict(n_cations=1.5),
        dict(ionic_strength="-1 molar"),
    ],
)
def test_invalid_requests_fail_before_openmm_construction(solute, monkeypatch, counts):
    from openmm.app import Modeller

    def forbidden(*args, **kwargs):
        raise AssertionError("Invalid controls reached solvent construction")

    monkeypatch.setattr(Modeller, "addSolvent", forbidden)
    with pytest.raises(ArgumentError):
        msm.build.solvate(solute, engine="OpenMM", **counts)
