"""Check the legacy keyword helper against actual physical constraint policies."""

from copy import deepcopy

import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentChoiceError
from molsysmt.native import MolecularMechanics

openmm = pytest.importorskip("openmm")
from openmm import app  # noqa: E402


@pytest.mark.parametrize(
    "policy,expected",
    [
        (None, None),
        ("h_bonds", app.HBonds),
        ("hbonds", app.HBonds),
        ("all_bonds", app.AllBonds),
        ("all bonds", app.AllBonds),
        ("h_angles", app.HAngles),
        ("none", None),
    ],
)
@pytest.mark.parametrize("skip", [False, True])
def test_legacy_parameters_preserve_the_requested_constraint_policy(
    policy, expected, skip
):
    mechanics = MolecularMechanics(non_bonded_method="no_cutoff", constraints=policy)
    before = deepcopy(mechanics.to_dict())
    assert (
        mechanics.get_openmm_System_parameters(skip_digestion=skip)["constraints"]
        is expected
    )
    assert mechanics.to_dict() == before


def test_legacy_all_bonds_changes_actual_constraint_pairs_without_running_dynamics():
    source = msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"]
    topology = msm.convert(source, to_form="openmm.Topology")
    forcefield = app.ForceField("amber14-all.xml")
    mechanics = MolecularMechanics(
        non_bonded_method="no_cutoff", constraints="all_bonds"
    )
    # Only the translated constraint field is under test; this does not claim
    # that the entire legacy dictionary applies to ForceField.createSystem.
    actual = forcefield.createSystem(
        topology, constraints=mechanics.get_openmm_System_parameters()["constraints"]
    )
    expected = forcefield.createSystem(topology, constraints=app.AllBonds)
    hydrogen_only = forcefield.createSystem(topology, constraints=app.HBonds)

    def pairs(system):
        return [
            system.getConstraintParameters(i) for i in range(system.getNumConstraints())
        ]

    assert pairs(actual) == pairs(expected)
    assert pairs(actual) != pairs(hydrogen_only)


@pytest.mark.parametrize("value", ["unknown", False, 1, [], {}])
def test_legacy_unknown_constraint_policy_is_refused(value):
    mechanics = MolecularMechanics(non_bonded_method="no_cutoff", constraints=value)
    with pytest.raises(ArgumentChoiceError, match="constraints"):
        mechanics.get_openmm_System_parameters()
