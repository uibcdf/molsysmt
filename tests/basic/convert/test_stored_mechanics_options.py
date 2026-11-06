"""Resolve stored physical settings before defaults, preserving explicit choices."""

import pytest

import molsysmt as msm


@pytest.mark.parametrize("model", ["OBC1", "OBC2"])
def test_stored_model_and_solute_forcefield_reach_conversion_without_mutation(model):
    openmm = pytest.importorskip("openmm")
    molsys = msm.convert(msm.systems["Trp-Cage"]["1l2y.h5msm"], structure_indices=0)
    msm.set(molsys, forcefield="AMBER96", implicit_solvent=model)
    result = msm.convert(molsys, to_form="openmm.System")
    expected = msm.convert(
        molsys, to_form="openmm.System", forcefield="AMBER96", implicit_solvent=model
    )
    assert sorted(
        openmm.XmlSerializer.serialize(f) for f in result.getForces()
    ) == sorted(openmm.XmlSerializer.serialize(f) for f in expected.getForces())
    vacuum = msm.convert(molsys, to_form="openmm.System", implicit_solvent=None)
    assert not any(isinstance(f, openmm.CustomGBForce) for f in vacuum.getForces())
    assert msm.get(molsys, forcefield=True, implicit_solvent=True) == ["AMBER96", model]


def test_invalid_stored_setting_is_validated_before_engine_construction():
    pytest.importorskip("openmm")
    from molsysmt._private.smonitor import ArgumentError

    molsys = msm.convert(msm.systems["Trp-Cage"]["1l2y.h5msm"], structure_indices=0)
    molsys.molecular_mechanics.implicit_solvent = "unknown-model"
    with pytest.raises(ArgumentError, match="implicit_solvent"):
        msm.convert(molsys, to_form="openmm.System")
