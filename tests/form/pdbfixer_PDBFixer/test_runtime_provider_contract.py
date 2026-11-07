"""Grounding the optional PDBFixer floor in public cap hydrogen completion."""

import tomllib
from pathlib import Path

import pytest
from packaging.requirements import Requirement

import molsysmt as msm


def test_optional_requirement_admits_the_cap_completion_floor():
    project = tomllib.loads(
        (Path(__file__).resolve().parents[3] / "pyproject.toml").read_text()
    )["project"]
    requirement = next(
        requirement
        for requirement in map(Requirement, project["optional-dependencies"]["soft"])
        if requirement.name.lower() == "pdbfixer"
    )
    assert requirement.specifier.contains("1.11.0")
    assert requirement.specifier.contains("1.12.0")
    assert not requirement.specifier.contains("1.10.0"), (
        "PDBFixer 1.10 leaves ACE and NME without their hydrogens; "
        "1.11 fixes cap completion in the consumed addMissingHydrogens route."
    )
    assert all(
        Requirement(raw).name.lower() != "pdbfixer" for raw in project["dependencies"]
    )


def test_public_ph_engine_completes_caps_and_keeps_the_source(monkeypatch):
    pytest.importorskip("pdbfixer")
    openmm = pytest.importorskip("openmm")
    from openmm import app

    source = msm.convert(
        msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"],
        to_form="molsysmt.MolSys",
    )
    source = msm.remove(source, selection='atom_type=="H"')
    assert source.topology.n_atoms == 10
    assert source.topology.groups["group_name"].tolist() == ["ACE", "ALA", "NME"]

    original_add = app.Modeller.addHydrogens
    reference = openmm.Platform.getPlatformByName("Reference")
    platforms = []

    def add_reference_hydrogens(self, *args, **kwargs):
        # The public pH route does not expose a platform. Constrain hardware
        # selection while retaining the actual provider's hydrogen completion.
        kwargs["platform"] = reference
        platforms.append("Reference")
        return original_add(self, *args, **kwargs)

    monkeypatch.setattr(app.Modeller, "addHydrogens", add_reference_hydrogens)

    result = msm.build.add_missing_hydrogens(source, pH=7.4, engine="PDBFixer")

    assert result.topology.n_atoms == 22
    for name, expected in {"ACE": 3, "ALA": 5, "NME": 4}.items():
        assert (
            msm.get(
                result,
                selection=f'group_name=="{name}" and atom_type=="H"',
                n_atoms=True,
            )
            == expected
        )
    assert source.topology.n_atoms == 10
    assert msm.get(source, selection='atom_type=="H"', n_atoms=True) == 0
    topology = msm.convert(result, to_form="openmm.Topology")
    system = app.ForceField("amber14/protein.ff14SB.xml").createSystem(topology)
    assert system.getNumParticles() == 22
    assert platforms == ["Reference"]
