"""Testing exhaustive native MolSys-to-MolSysDict preflight reports."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.conversion_report import (
    _MOLSYS_TO_MOLSYS_DICT_PROFILE,
    get_conversion_audit_scopes,
    is_conversion_audit_exhaustive,
)
from molsysmt.native import MolSys


def test_profile_partitions_the_declared_molsys_contract():
    from molsysmt.form.molsysmt_MolSys.attributes import attributes

    declared = {name for name, available in attributes.items() if available}
    profile = _MOLSYS_TO_MOLSYS_DICT_PROFILE
    classified = (
        profile["directly_preserved"]
        | profile["derived_without_loss"]
        | set(profile["covered_by_dependencies"])
        | set(profile["loss_candidates"])
    )

    assert classified == declared


def test_static_route_coverage_is_exhaustive():
    source = "molsysmt.MolSys"
    target = "molsysmt.MolSysDict"

    assert get_conversion_audit_scopes(source, target) == ("all",)
    assert is_conversion_audit_exhaustive(source, target) is True


def test_empty_molsys_reports_equivalent_exhaustive_conversion():
    source = MolSys(skip_digestion=True)

    _, report = msm.convert(
        source,
        to_form="molsysmt.MolSysDict",
        return_report=True,
    )

    assert report.audited_scopes == ("all",)
    assert report.is_exhaustive is True
    assert report.outcome == "equivalent"
    assert report.issues == ()


def test_composed_profile_reports_structural_and_chemical_losses(rich_molsys):
    source = rich_molsys.copy()
    source._set_structure_chemical_state_indices([0, 0, 0])
    source.structures.velocities = puw.quantity(
        np.ones((3, 4, 3)),
        "nm/ps",
    )
    source.structures.bioassembly = {"1": []}
    source.chemical_states._resolve_chemical_state().state_id = "state-A"
    source.chemical_states._set_chemical_state_atom_attribute(
        "formal_charge",
        pd.array([1, 0, 0, -1], dtype="Int16"),
    )

    payload, report = msm.convert(
        source,
        to_form="molsysmt.MolSysDict",
        return_report=True,
    )

    assert report.audited_scopes == ("all",)
    assert report.is_exhaustive
    assert report.outcome == "equivalent"
    assert report.issues == ()
    restored = msm.convert(payload, to_form="molsysmt.MolSys")
    assert msm.get(restored, formal_charge=True) == [1, 0, 0, -1]
    assert restored.chemical_states._states[0].state_id == "state-A"
    np.testing.assert_array_equal(
        puw.get_value(restored.structures.velocities, to_unit="nm/ps"),
        np.ones((3, 4, 3)),
    )
    assert restored.structures.bioassembly == {"1": []}
    assert msm.get(restored, structure_chemical_state_index=True) == [0, 0, 0]
    assert (
        msm.convert(source, to_form="molsysmt.MolSysDict", strict=True).data
        == payload.data
    )


def test_all_mechanical_fields_are_reported(rich_molsys):
    source = rich_molsys.copy()
    mechanics = source.molecular_mechanics
    mechanics.partial_charge = [0.1, 0.2, -0.2, -0.1]
    mechanics.atom_ff_type = ["N", "CT", "C", "O"]
    for attribute in (
        "forcefield",
        "non_bonded_method",
        "cutoff_distance",
        "switch_distance",
        "dispersion_correction",
        "ewald_error_tolerance",
        "hydrogen_mass",
        "constraints",
        "flexible_constraints",
        "water_model",
        "rigid_water",
        "implicit_solvent",
        "solute_dielectric",
        "solvent_dielectric",
        "salt_concentration",
        "kappa",
    ):
        setattr(mechanics, attribute, 1)

    from molsysmt._private.conversion_report import build_conversion_report

    report = build_conversion_report(source, "molsysmt.MolSys", "molsysmt.MolSysDict")
    with pytest.raises(ValueError, match="does not persist MolecularMechanics"):
        msm.convert(source, to_form="molsysmt.MolSysDict")
    with pytest.raises(msm.NotCompatibleConversionError):
        msm.convert(source, to_form="molsysmt.MolSysDict", strict=True)

    expected = {
        "partial_charge",
        "atom_ff_type",
        "forcefield",
        "non_bonded_method",
        "cutoff_distance",
        "switch_distance",
        "dispersion_correction",
        "ewald_error_tolerance",
        "hydrogen_mass",
        "constraints",
        "flexible_constraints",
        "water_model",
        "rigid_water",
        "implicit_solvent",
        "solute_dielectric",
        "solvent_dielectric",
        "salt_concentration",
        "kappa",
    }
    issues = {
        issue.attribute: issue for issue in report.issues if issue.attribute in expected
    }
    assert set(issues) == expected
    assert all(issue.scope == "molecular_mechanics" for issue in issues.values())


def test_all_structural_schema_losses_are_reported(rich_molsys):
    source = rich_molsys.copy()
    source.structures.velocities = puw.quantity(
        np.ones((3, 4, 3)),
        "nm/ps",
    )
    source.structures.b_factor = puw.quantity(
        np.ones((3, 4)),
        "nm**2",
    )
    source.structures.alternate_location = [{}, {}, {}]
    source.structures.bioassembly = {"1": []}
    source.structures.temperature = puw.quantity(
        np.full(3, 300.0),
        "K",
    )
    source.structures.potential_energy = puw.quantity(
        np.full(3, -10.0),
        "kJ/mol",
    )
    source.structures.kinetic_energy = puw.quantity(
        np.full(3, 2.0),
        "kJ/mol",
    )

    payload, report = msm.convert(
        source,
        to_form="molsysmt.MolSysDict",
        return_report=True,
    )

    assert report.outcome == "equivalent"
    assert report.issues == ()
    restored = msm.convert(payload, to_form="molsysmt.MolSys")
    for attribute in (
        "velocities",
        "b_factor",
        "temperature",
        "potential_energy",
        "kinetic_energy",
    ):
        actual = getattr(restored.structures, attribute)
        expected = getattr(source.structures, attribute)
        np.testing.assert_array_equal(puw.get_value(actual), puw.get_value(expected))
        assert puw.get_unit(actual) == puw.get_unit(expected)
    assert restored.structures.alternate_location == [{}, {}, {}]
    assert restored.structures.bioassembly == {"1": []}
    source.structures.alternate_location = np.full((3, 4), "")
    with pytest.raises(ValueError, match="sparse atom-to-sites"):
        msm.convert(source, to_form="molsysmt.MolSysDict")


def test_nontrivial_structure_state_association_is_reported(rich_molsys):
    source = rich_molsys.copy()
    source.chemical_states.append_state()
    source.chemical_states._states[1].state_id = "alternate"
    source._set_structure_chemical_state_indices([0, 1, 1])

    payload, report = msm.convert(
        source,
        to_form="molsysmt.MolSysDict",
        return_report=True,
    )

    assert report.outcome == "equivalent"
    assert report.issues == ()
    restored = msm.convert(payload, to_form="molsysmt.MolSys")
    assert restored.chemical_states.n_chemical_states == 2
    assert restored.chemical_states.reference_chemical_state_index == 0
    assert restored.chemical_states._states[1].state_id == "alternate"
    assert msm.get(restored, structure_chemical_state_index=True) == [0, 1, 1]
