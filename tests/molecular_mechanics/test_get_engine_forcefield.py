"""Protect resource-name lookup ownership and independent engine construction."""

import builtins

import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentChoiceError, ArgumentError
from molsysmt.molecular_mechanics.forcefields import switcher

_ENTRIES = [
    (engine, forcefield, model)
    for engine, fields in switcher.items()
    for forcefield, models in fields.items()
    for model in models
]


def _model_kwargs(model):
    if model == "vacuum":
        return {}
    if model in {"OBC1", "OBC2"}:
        return {"implicit_solvent": model}
    return {"water_model": model}


def test_get_engine_forcefield_1():

    output = msm.molecular_mechanics.get_engine_forcefield("AMBER14", engine="OpenMM")
    assert output == ["amber14-all.xml"]


def test_get_engine_forcefield_2():

    output = msm.molecular_mechanics.get_engine_forcefield(
        "AMBER14", water_model="TIP3P", engine="OpenMM"
    )
    assert output == ["amber14-all.xml", "amber14/tip3p.xml"]


@pytest.mark.parametrize("engine,forcefield,model", _ENTRIES)
@pytest.mark.parametrize("trusted", [False, True])
def test_caller_edits_do_not_change_registry_or_later_results(
    engine, forcefield, model, trusted
):
    registered = switcher[engine][forcefield][model]
    expected = tuple(registered)
    kwargs = dict(engine=engine, skip_digestion=trusted, **_model_kwargs(model))
    first = msm.molecular_mechanics.get_engine_forcefield(forcefield, **kwargs)
    second = msm.molecular_mechanics.get_engine_forcefield(forcefield, **kwargs)
    assert isinstance(first, list)
    assert tuple(first) == expected
    assert first is not registered
    assert first is not second
    first.append("task-owned-missing-forcefield.xml")
    first[0] = "task-owned-replacement.xml"
    second.clear()
    assert tuple(registered) == expected
    assert msm.molecular_mechanics.get_engine_forcefield(forcefield, **kwargs) == list(
        expected
    )


@pytest.mark.parametrize("trusted", [False, True])
def test_parameterization_is_unchanged_after_caller_local_resource_edits(trusted):
    openmm = pytest.importorskip("openmm")
    molsys = msm.convert(msm.systems["Trp-Cage"]["1l2y.h5msm"], structure_indices=0)
    reference = msm.convert(
        molsys, to_form="openmm.System", forcefield="AMBER14", water_model="TIP3P"
    )
    resources = msm.molecular_mechanics.get_engine_forcefield(
        "AMBER14", water_model="TIP3P", skip_digestion=trusted
    )
    resources.append("task-owned-missing-forcefield.xml")
    system = msm.convert(
        molsys, to_form="openmm.System", forcefield="AMBER14", water_model="TIP3P"
    )
    assert system.getNumParticles() == 304
    assert [system.getParticleMass(i) for i in range(304)] == [
        reference.getParticleMass(i) for i in range(304)
    ]
    assert [
        system.getConstraintParameters(i) for i in range(system.getNumConstraints())
    ] == [
        reference.getConstraintParameters(i)
        for i in range(reference.getNumConstraints())
    ]
    # Force enumeration may differ between OpenMM builders; compare all payloads.
    assert sorted(
        openmm.XmlSerializer.serialize(force) for force in system.getForces()
    ) == sorted(
        openmm.XmlSerializer.serialize(force) for force in reference.getForces()
    )
    assert msm.molecular_mechanics.get_engine_forcefield(
        "AMBER14", water_model="TIP3P"
    ) == ["amber14-all.xml", "amber14/tip3p.xml"]


@pytest.mark.parametrize(
    "engine,forcefield,expected",
    [
        ("OpenMM", "AMBER10", ["amber10.xml", "implicit/obc1.xml"]),
        ("OpenMM", "AMBER14", ["amber14-all.xml", "implicit/obc1.xml"]),
        ("LEaP", "AMBER14", ["leaprc.protein.ff14SB"]),
        ("LEaP", "AMBER99SBILDN", ["oldff/leaprc.ff99SBildn"]),
    ],
)
def test_implicit_solvent_precedes_water_model_without_rewriting_resources(
    engine, forcefield, expected
):
    assert msm.molecular_mechanics.get_engine_forcefield(
        forcefield, engine=engine, implicit_solvent="OBC1", water_model="TIP4P-FB"
    ) == expected


@pytest.mark.parametrize(
    "argument,value",
    [
        ("forcefield", None),
        ("forcefield", ["AMBER14"]),
        ("forcefield", "unknown"),
        ("engine", None),
        ("engine", ["OpenMM"]),
        ("engine", "unknown"),
        ("water_model", True),
        ("water_model", "unknown"),
        ("implicit_solvent", True),
        ("implicit_solvent", "unknown"),
        ("skip_digestion", 1),
        ("skip_digestion", "True"),
        ("skip_digestion", "False"),
    ],
)
def test_invalid_arguments_have_native_diagnostics(argument, value):
    kwargs = {"forcefield": "AMBER14", argument: value}
    with pytest.raises(ArgumentError, match=argument):
        msm.molecular_mechanics.get_engine_forcefield(**kwargs)


@pytest.mark.parametrize(
    "kwargs,argument",
    [
        ({"engine": "Amber"}, "engine"),
        ({"forcefield": "GAFF"}, "forcefield"),
        ({"water_model": "SPC"}, "water_model"),
        ({"forcefield": "CHARMM36", "implicit_solvent": "OBC1"}, "implicit_solvent"),
    ],
)
def test_unregistered_combinations_have_native_choice_diagnostics(kwargs, argument):
    with pytest.raises(ArgumentChoiceError, match=argument):
        msm.molecular_mechanics.get_engine_forcefield(**{"forcefield": "AMBER14", **kwargs})


@pytest.mark.parametrize("engine", ["OpenMM", "LEaP"])
def test_metadata_lookup_does_not_import_or_require_an_engine(engine, monkeypatch):
    from depdigest.core import checker

    original_import = builtins.__import__
    original_find_spec = checker.find_spec

    def guarded_import(name, *args, **kwargs):
        if name.split(".")[0] in {"openmm", "pytraj", "parmed", "pdbfixer"}:
            raise AssertionError(f"Metadata lookup imported engine {name}")
        return original_import(name, *args, **kwargs)

    def missing(name, *args, **kwargs):
        if name in {"openmm", "pytraj", "parmed", "pdbfixer"}:
            return None
        return original_find_spec(name, *args, **kwargs)

    try:
        monkeypatch.setattr(builtins, "__import__", guarded_import)
        monkeypatch.setattr(checker, "find_spec", missing)
        checker.is_installed.cache_clear()
        for candidate_engine, forcefield, model in _ENTRIES:
            if candidate_engine != engine:
                continue
            result = msm.molecular_mechanics.get_engine_forcefield(
                forcefield, engine=engine, **_model_kwargs(model)
            )
            assert result == switcher[engine][forcefield][model]
    finally:
        monkeypatch.setattr(builtins, "__import__", original_import)
        monkeypatch.setattr(checker, "find_spec", original_find_spec)
        checker.is_installed.cache_clear()
