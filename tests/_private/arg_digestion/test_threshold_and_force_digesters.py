import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.arg_digestion.argument.angle_threshold import digest_angle_threshold
from molsysmt._private.arg_digestion.argument.cutoff_distance import digest_cutoff_distance
from molsysmt._private.arg_digestion.argument.distance_threshold import digest_distance_threshold
from molsysmt._private.arg_digestion.argument.force import digest_force
from molsysmt._private.arg_digestion.argument.force_constant import digest_force_constant
from molsysmt._private.arg_digestion.argument.radius import digest_radius
from molsysmt._private.arg_digestion.argument.threshold import digest_threshold

ANGLE_CALLER = "molsysmt.hbonds.get_luzard_chandler_hbonds.get_luzard_chandler_hbonds"
DISTANCE_CALLER = "molsysmt.hbonds.get_buch_hbonds.get_buch_hbonds"
THRESHOLD_CALLER = "molsysmt.structure.show_contacts.show_contacts"
THRESHOLD_NONE_CALLER = "molsysmt.structure.get_neighbors.get_neighbors"
FORM_CONVERTER_CALLER = "molsysmt.form.file_cif.to_mmcif_PdbxContainers_DataContainer.to_mmcif_PdbxContainers_DataContainer"
FORCE_CONSTANT_CALLER = "molsysmt.molecular_mechanics.add_harmonic_bond_force.add_harmonic_bond_force"


def test_angle_distance_and_threshold_digesters_cover_supported_callers():
    angle = digest_angle_threshold("30 degrees", caller=ANGLE_CALLER)
    expected_angle = msm.pyunitwizard.standardize(msm.pyunitwizard.quantity(30.0, "degrees"))
    assert msm.pyunitwizard.get_value(angle) == pytest.approx(msm.pyunitwizard.get_value(expected_angle))

    distance_threshold = digest_distance_threshold("0.35 nm", caller=DISTANCE_CALLER)
    assert msm.pyunitwizard.get_value(distance_threshold) == pytest.approx(0.35)

    threshold = digest_threshold("0.45 nm", caller=THRESHOLD_CALLER)
    assert msm.pyunitwizard.get_value(threshold) == pytest.approx(0.45)
    assert digest_threshold(None, caller=THRESHOLD_NONE_CALLER) is None

    with pytest.raises(ArgumentError):
        digest_angle_threshold("1 nm", caller=ANGLE_CALLER)

    with pytest.raises(ArgumentError):
        digest_distance_threshold("30 degrees", caller=DISTANCE_CALLER)


def test_cutoff_distance_radius_and_force_digesters_accept_valid_quantities():
    cutoff = digest_cutoff_distance("1.2 nm", caller=FORM_CONVERTER_CALLER)
    assert msm.pyunitwizard.get_value(cutoff) == pytest.approx(1.2)
    assert digest_cutoff_distance(None, caller=FORM_CONVERTER_CALLER) is None

    radius = digest_radius("0.2 nm")
    assert msm.pyunitwizard.get_value(radius) == pytest.approx(0.2)

    force = digest_force("2.0 kilojoule/(nanometer mol)")
    assert msm.pyunitwizard.get_value(force, to_unit="kilojoule/(nanometer mol)") == pytest.approx(2.0)

    with pytest.raises(ArgumentError):
        digest_cutoff_distance("90 degrees")

    with pytest.raises(ArgumentError):
        digest_radius("90 degrees")

    with pytest.raises(ArgumentError):
        digest_force("1.0 nanometers")


def test_force_constant_supports_scalar_and_list_outputs_for_supported_callers():
    scalar = digest_force_constant("5 kilojoule/(nanometer**2 mol)", caller=FORCE_CONSTANT_CALLER)
    assert len(scalar) == 1
    assert msm.pyunitwizard.get_value(scalar[0], to_unit="kilojoule/(nanometer**2 mol)") == pytest.approx(5.0)

    values = [
        msm.pyunitwizard.quantity(5.0, "kilojoule/(nanometer**2 mol)"),
        msm.pyunitwizard.quantity(7.0, "kilojoule/(nanometer**2 mol)"),
    ]
    sequence = digest_force_constant(values, caller=FORCE_CONSTANT_CALLER)
    assert len(sequence) == 2
    assert [msm.pyunitwizard.get_value(item, to_unit="kilojoule/(nanometer**2 mol)") for item in sequence] == [pytest.approx(5.0), pytest.approx(7.0)]

    single = digest_force_constant("5 kilojoule/(nanometer**2 mol)")
    assert msm.pyunitwizard.get_value(single, to_unit="kilojoule/(nanometer**2 mol)") == pytest.approx(5.0)

    with pytest.raises(ArgumentError):
        digest_force_constant([msm.pyunitwizard.quantity(5.0, "nanometers")], caller=FORCE_CONSTANT_CALLER)
