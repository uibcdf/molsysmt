"""Distinguishing stored mechanics values from Boolean attribute requests."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt.native import MolecularMechanics, MolSys

puw = msm.pyunitwizard
SETTINGS = {
    "forcefield": "AMBER14",
    "non_bonded_method": "no_cutoff",
    "cutoff_distance": puw.quantity(1.0, "nm"),
    "switch_distance": puw.quantity(0.9, "nm"),
    "dispersion_correction": True,
    "ewald_error_tolerance": 0.0001,
    "hydrogen_mass": puw.quantity(3.0, "Da"),
    "constraints": "none",
    "flexible_constraints": False,
    "water_model": "TIP3P",
    "rigid_water": True,
    "implicit_solvent": "OBC1",
    "solute_dielectric": 1.0,
    "solvent_dielectric": 78.5,
    "salt_concentration": puw.quantity(0.1, "molar"),
    "kappa": puw.quantity(0.0, "1/nm"),
}


def _source(form, *, populated=True):
    mechanics = MolecularMechanics(**SETTINGS) if populated else MolecularMechanics()
    if form == "molsysmt.MolecularMechanics":
        return mechanics
    if form == "molsysmt.MolecularMechanicsDict":
        return msm.convert(mechanics, to_form=form)
    molsys = MolSys()
    molsys.molecular_mechanics = mechanics
    return molsys


@pytest.mark.parametrize(
    "form",
    [
        "molsysmt.MolSys",
        "molsysmt.MolecularMechanics",
        "molsysmt.MolecularMechanicsDict",
    ],
)
@pytest.mark.parametrize("attribute", SETTINGS)
def test_system_mechanical_queries_use_flags_instead_of_physical_values(
    form, attribute
):
    source = _source(form)
    expected = SETTINGS[attribute]
    result = msm.get(source, **{attribute: True})
    if puw.is_quantity(expected):
        assert puw.are_close(result, expected)
    else:
        assert result == expected
    if form == "molsysmt.MolSys":
        native = source.get(**{attribute: True})
        if puw.is_quantity(expected):
            assert puw.are_close(native, expected)
        else:
            assert native == expected
        assert source.get(**{attribute: False}) == []
    assert msm.get(source, **{attribute: False}) == []
    assert msm.get(source, output_type="dictionary", **{attribute: False}) == {}
    absent = msm.get(_source(form, populated=False), **{attribute: True})
    assert absent is None


def test_mixed_native_queries_keep_order_and_ignore_false_requests():
    molsys = _source("molsysmt.MolSys")
    kwargs = dict(
        constraints=True,
        forcefield=False,
        non_bonded_method=True,
        flexible_constraints=True,
    )
    for get in (lambda **flags: msm.get(molsys, **flags), molsys.get):
        assert get(**kwargs) == ["none", "no_cutoff", False]
        assert get(output_type="dictionary", **kwargs) == {
            "constraints": "none",
            "non_bonded_method": "no_cutoff",
            "flexible_constraints": False,
        }
        assert get(constraints=False, n_atoms=True) == 0
    assert molsys.molecular_mechanics.forcefield == "AMBER14"
    assert molsys.molecular_mechanics.constraints == "none"


@pytest.mark.parametrize("policy", ["none", "hbonds", "all_bonds", "h_angles"])
def test_setting_and_reading_a_policy_never_replaces_it_with_a_boolean(policy):
    molsys = MolSys()
    msm.set(molsys, constraints=policy)
    assert msm.get(molsys, constraints=True) == policy
    assert molsys.get(constraints=True) == policy
    assert molsys.molecular_mechanics.constraints == policy


@pytest.mark.parametrize("attribute", SETTINGS)
@pytest.mark.parametrize("flag", [None, 0, 1, "none", [], np.bool_(True)])
def test_mechanical_reader_requires_a_boolean_flag(attribute, flag):
    molsys = _source("molsysmt.MolSys")
    for get in (lambda **flags: msm.get(molsys, **flags), molsys.get):
        with pytest.raises(ArgumentError, match=attribute):
            get(**{attribute: flag})


def test_reading_stored_requests_does_not_credit_engine_execution():
    ackredit = pytest.importorskip("ackredit")
    molsys = _source("molsysmt.MolSys")
    with ackredit.session("read-mechanics"):
        with ackredit.capture("stored-requests") as run:
            result = molsys.get(constraints=True, implicit_solvent=True)
        assert result == ["none", "OBC1"]
        assert not run.attribution.to_dict()["items"]
        assert not ackredit.get_used_items()


@pytest.mark.parametrize("flag", [False, True])
def test_a_constraint_reader_flag_is_not_a_physical_policy(flag):
    molsys = _source("molsysmt.MolSys")
    with pytest.raises(ArgumentError, match="constraints"):
        msm.set(molsys, constraints=flag)
    with pytest.raises(ArgumentError, match="constraints"):
        msm.convert(molsys, to_form="openmm.System", constraints=flag)
    assert molsys.molecular_mechanics.constraints == "none"
