"""Verify actual engine platform selection, numeric parity and failure ownership."""

import numpy as np
import pytest

import molsysmt as msm

openmm = pytest.importorskip("openmm")


@pytest.mark.parametrize("target", ["openmm.Context", "openmm.Simulation"])
def test_reference_construction_selects_the_requested_platform(alanine_molsys, target):
    molsys = msm.extract(alanine_molsys, structure_indices=0)
    result = msm.convert(molsys, to_form=target, platform="Reference")
    try:
        context = result.context if target == "openmm.Simulation" else result
        assert context.getPlatform().getName() == "Reference"
        assert np.isfinite(
            msm.pyunitwizard.get_value(
                context.getState(getEnergy=True).getPotentialEnergy(), to_unit="kJ/mol"
            )
        )
    finally:
        del result


def test_reference_energy_works_through_the_normal_public_boundary(alanine_molsys):
    molsys = msm.extract(alanine_molsys, structure_indices=0)
    energy = msm.molecular_mechanics.get_potential_energy(molsys, platform="Reference")
    assert np.isfinite(msm.pyunitwizard.get_value(energy, to_unit="kJ/mol"))


@pytest.mark.parametrize("model", [None, "OBC1", "OBC2"])
def test_cpu_reference_energy_parity_preserves_units_and_source(alanine_molsys, model):
    puw = msm.pyunitwizard
    molsys = msm.extract(alanine_molsys, structure_indices=0)
    if model is not None:
        msm.set(molsys, implicit_solvent=model)
    coordinates = puw.get_value(msm.get(molsys, coordinates=True), to_unit="nm").copy()
    with puw.context(
        standard_units=["angstrom", "ps", "kcal/mol", "e", "K", "radians"]
    ):
        # Lazy unit backends may load during execution without changing policy.
        policy = {
            k: v for k, v in puw.configure.report().items() if k != "loaded_libraries"
        }
        cpu = msm.molecular_mechanics.get_potential_energy(molsys, platform="CPU")
        reference = msm.molecular_mechanics.get_potential_energy(
            molsys, platform="Reference"
        )
        assert puw.get_unit(cpu) == puw.unit("kcal/mol")
        assert puw.get_unit(reference) == puw.unit("kcal/mol")
        # CPU vector kernels use lower precision than Reference; small molecular
        # energies allow 1e-3 kJ/mol absolute plus 1e-6 relative rounding.
        np.testing.assert_allclose(
            puw.get_value(cpu, to_unit="kJ/mol"),
            puw.get_value(reference, to_unit="kJ/mol"),
            atol=1e-3,
            rtol=1e-6,
        )
        assert {
            k: v for k, v in puw.configure.report().items() if k != "loaded_libraries"
        } == policy
    np.testing.assert_array_equal(
        puw.get_value(msm.get(molsys, coordinates=True), to_unit="nm"), coordinates
    )


@pytest.mark.parametrize("target", ["openmm.Context", "openmm.Simulation"])
def test_unknown_and_unregistered_names_have_different_diagnostics(
    alanine_molsys, target
):
    from molsysmt._private.smonitor import (
        ArgumentChoiceError,
        ExecutionPlatformUnavailableError,
    )
    from molsysmt.third_party.openmm.platforms._resolve import KNOWN_PLATFORMS

    available = msm.third_party.openmm.platforms.available_platforms(verbose=False)
    absent = next(
        (
            name
            for name in ["OpenCL", *sorted(KNOWN_PLATFORMS)]
            if name not in available
        ),
        None,
    )
    if absent is None:
        pytest.skip("All known engine platforms are registered on this installation")
    molsys = msm.extract(alanine_molsys, structure_indices=0)
    with pytest.raises(ArgumentChoiceError, match="platform"):
        msm.convert(molsys, to_form=target, platform="not-a-registered-platform")
    with pytest.raises(ExecutionPlatformUnavailableError, match=absent) as raised:
        msm.convert(molsys, to_form=target, platform=absent)
    assert raised.value.extra["engine"] == "OpenMM"
    assert raised.value.extra["platform"] == absent
    assert raised.value.extra["available_platforms"] == available


@pytest.mark.parametrize("value", [None, True, 1, [], "", "   "])
def test_invalid_formats_fail_before_engine_lookup(alanine_molsys, value):
    from molsysmt._private.smonitor import ArgumentError

    with pytest.raises(ArgumentError, match="platform"):
        msm.convert(alanine_molsys, to_form="openmm.Context", platform=value)


def test_installed_plugin_name_is_not_restricted_to_builtin_vocabulary(monkeypatch):
    from molsysmt.third_party.openmm.platforms import platforms
    from molsysmt.third_party.openmm.platforms._resolve import resolve_platform

    # Registry-only simulation: no custom device or numerical execution is claimed.
    marker = object()
    monkeypatch.setattr(
        platforms, "available_platforms", lambda verbose: ["FuturePlugin"]
    )
    monkeypatch.setattr(
        openmm.Platform,
        "getPlatformByName",
        lambda name: marker if name == "FuturePlugin" else None,
    )
    assert resolve_platform("FuturePlugin", "platform-contract") is marker


def test_registered_device_initialization_failure_is_not_reclassified(
    alanine_molsys, monkeypatch
):
    failure = RuntimeError("controlled CPU device initialization failure")

    def fail(*args, **kwargs):
        raise failure

    from molsysmt.form.openmm_System.to_openmm_Context import to_openmm_Context

    system = msm.convert(alanine_molsys, to_form="openmm.System")
    monkeypatch.setattr(openmm, "Context", fail)
    with pytest.raises(RuntimeError) as raised:
        to_openmm_Context(system, platform="CPU")
    assert raised.value is failure


def test_absent_engine_remains_a_dependency_diagnostic(monkeypatch):
    from depdigest.core import checker

    from molsysmt._private.smonitor import LibraryNotFoundError
    from molsysmt.third_party.openmm.platforms._resolve import resolve_platform

    original = checker.find_spec

    def missing(name, *args, **kwargs):
        return None if name == "openmm" else original(name, *args, **kwargs)

    try:
        monkeypatch.setattr(checker, "find_spec", missing)
        checker.is_installed.cache_clear()
        with pytest.raises(LibraryNotFoundError, match="openmm"):
            resolve_platform("Reference", "platform-contract")
    finally:
        monkeypatch.setattr(checker, "find_spec", original)
        checker.is_installed.cache_clear()


def test_existing_context_keeps_its_actual_platform(alanine_molsys):
    context = msm.convert(
        msm.extract(alanine_molsys, structure_indices=0),
        to_form="openmm.Context",
        platform="Reference",
    )
    try:
        result = msm.molecular_mechanics.get_potential_energy(context)
        assert context.getPlatform().getName() == "Reference"
        assert np.isfinite(msm.pyunitwizard.get_value(result, to_unit="kJ/mol"))
    finally:
        del context


def test_flat_nonbonded_energy_uses_reference_platform(alanine_molsys):
    molsys = msm.extract(alanine_molsys, structure_indices=0)
    values = [
        msm.molecular_mechanics.get_non_bonded_potential_energy(
            molsys,
            selection="group_index == 0",
            selection_2="group_index == 2",
            platform=name,
        )
        for name in ["CPU", "Reference"]
    ]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(values[0], to_unit="kJ/mol"),
        msm.pyunitwizard.get_value(values[1], to_unit="kJ/mol"),
        atol=1e-3,
        rtol=1e-6,
    )


def test_reference_minimization_returns_an_independent_system(alanine_molsys):
    puw = msm.pyunitwizard
    molsys = msm.extract(alanine_molsys, structure_indices=0)
    coordinates = puw.get_value(msm.get(molsys, coordinates=True), to_unit="nm").copy()
    initial = msm.molecular_mechanics.get_potential_energy(molsys, platform="Reference")
    result = msm.molecular_mechanics.potential_energy_minimization(
        molsys, platform="Reference"
    )
    final = msm.molecular_mechanics.get_potential_energy(result, platform="Reference")
    assert result is not molsys
    assert (
        puw.get_value(final, to_unit="kJ/mol")
        <= puw.get_value(initial, to_unit="kJ/mol") + 1e-3
    )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(molsys, coordinates=True), to_unit="nm"), coordinates
    )
