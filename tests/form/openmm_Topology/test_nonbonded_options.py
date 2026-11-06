"""Protecting physical nonbonded options used by native force construction."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentConflictError, ArgumentError

openmm = pytest.importorskip("openmm")
from openmm import unit  # noqa: E402


@pytest.fixture
def periodic_topology(alanine_molsys):
    molsys = msm.extract(alanine_molsys, structure_indices=0)
    msm.set(molsys, box=puw.quantity(np.diag([3.0, 3.0, 3.0])[None], "nm"))
    return msm.convert(molsys, to_form="openmm.Topology")


def _force(topology, **kwargs):
    system = msm.convert(
        topology,
        to_form="openmm.System",
        forcefield="AMBER14",
        water_model="TIP3P",
        non_bonded_method="PME",
        **kwargs,
    )
    return next(
        force
        for force in system.getForces()
        if isinstance(force, openmm.NonbondedForce)
    )


@pytest.mark.parametrize("enabled", [False, True])
def test_explicit_dispersion_choices_are_applied(periodic_topology, enabled):
    assert (
        _force(
            periodic_topology, dispersion_correction=enabled
        ).getUseDispersionCorrection()
        is enabled
    )


@pytest.mark.parametrize(
    "distance, expected", [("0 nm", 0.0), ("0.4 nm", 0.4), ("400 pm", 0.4)]
)
def test_switching_distance_applies_a_physical_length(
    periodic_topology, distance, expected
):
    force = _force(periodic_topology, switch_distance=distance)
    assert force.getUseSwitchingFunction() is True
    assert force.getSwitchingDistance().value_in_unit(unit.nanometer) == pytest.approx(
        expected
    )


@pytest.mark.parametrize("distance", ["-0.1 nm", "1 nm", "1.2 nm", "[0.2,0.3] nm"])
def test_switching_requires_one_nonnegative_length_below_the_actual_cutoff(
    periodic_topology, distance
):
    with pytest.raises(ArgumentError, match="switch_distance"):
        _force(periodic_topology, switch_distance=distance)


def test_a_switch_request_without_cutoff_is_not_silently_ignored(periodic_topology):
    with pytest.raises(ArgumentConflictError, match="switch_distance"):
        msm.convert(
            periodic_topology,
            to_form="openmm.System",
            forcefield="AMBER14",
            non_bonded_method="no cutoff",
            switch_distance="0.4 nm",
        )


def test_explicit_ewald_tolerance_reaches_the_constructed_force(periodic_topology):
    assert _force(
        periodic_topology, ewald_error_tolerance=1e-4
    ).getEwaldErrorTolerance() == pytest.approx(1e-4)


@pytest.mark.parametrize("value", [0.0, -1.0, float("nan"), float("inf"), [1e-4]])
def test_invalid_ewald_tolerance_does_not_become_an_engine_default(
    periodic_topology, value
):
    with pytest.raises(ArgumentError, match="ewald_error_tolerance"):
        _force(periodic_topology, ewald_error_tolerance=value)
