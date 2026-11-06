"""Executing capstone preparation statements on explicitly local model controls."""

import ast
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw

LESSON = (
    Path(__file__).resolve().parents[2]
    / "docs/content/course/Path_Alzheimer/54_Final_Project.ipynb"
)


def _code(step):
    return next(
        "".join(cell["source"])
        for cell in json.loads(LESSON.read_text())["cells"]
        if cell["cell_type"] == "code" and f"# {step}." in "".join(cell["source"])
    )


def _run(step, namespace):
    exec(compile(_code(step), str(LESSON), "exec"), namespace)


def _coordinates(molsys):
    return puw.get_value(msm.get(molsys, coordinates=True), to_unit="nm").copy()


def _local_target():
    return msm.convert(
        msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"],
        structure_indices=0,
    )


@pytest.mark.parametrize("missing_name", ["H", "O"])
@pytest.mark.parametrize("length_unit", ["nm", "pm"])
def test_target_cell_consumes_both_independent_repairs(
    missing_name, length_unit, monkeypatch
):
    pytest.importorskip("openmm")
    complete = _local_target()
    source = msm.extract(
        complete,
        selection=f'not (group_index==1 and atom_name=="{missing_name}")',
    )
    assert msm.get(source, n_atoms=True) == 21
    before_xyz = _coordinates(source)
    before_atoms = source.topology.atoms.copy(deep=True)
    original_convert = msm.convert
    original_heavy = msm.build.add_missing_heavy_atoms
    original_hydrogen = msm.build.add_missing_hydrogens
    calls = {}

    def local_convert(item, *args, **kwargs):
        if isinstance(item, str) and item == "pdb:2BEG":
            return source.copy()
        return original_convert(item, *args, **kwargs)

    def heavy(item, *args, **kwargs):
        result = original_heavy(item, *args, **kwargs)
        calls["heavy_input"] = item
        calls["heavy_output"] = result
        return result

    def hydrogen(item, *args, **kwargs):
        result = original_hydrogen(item, *args, **kwargs)
        calls["hydrogen_input"] = item
        calls["hydrogen_output"] = result
        return result

    monkeypatch.setattr(msm, "convert", local_convert)
    monkeypatch.setattr(msm.build, "add_missing_heavy_atoms", heavy)
    monkeypatch.setattr(msm.build, "add_missing_hydrogens", hydrogen)
    namespace = {}
    with puw.context(standard_units=[length_unit, "fs", "radians"]):
        _run(1, namespace)
    assert calls["hydrogen_input"] is calls["heavy_output"]
    assert namespace["fibril"] is calls["hydrogen_output"]
    assert namespace["fibril"] is not calls["heavy_input"]
    assert msm.get(namespace["fibril"], n_atoms=True) == 22
    assert msm.build.get_missing_heavy_atoms(namespace["fibril"]) == {}
    assert np.isfinite(_coordinates(namespace["fibril"])).all()
    # These controlled groups have unique names on unchanged group axes. The
    # correspondence is an independent test oracle, not a general identity rule.
    final_atoms = namespace["fibril"].topology.atoms
    final_keys = list(zip(final_atoms["group_index"], final_atoms["atom_name"]))
    assert len(set(final_keys)) == len(final_keys)
    mapping = np.asarray(
        [
            final_keys.index(key)
            for key in zip(before_atoms["group_index"], before_atoms["atom_name"])
        ],
        dtype=np.int64,
    )
    assert mapping.shape == (21,)
    np.testing.assert_allclose(
        _coordinates(namespace["fibril"])[:, mapping],
        before_xyz,
        atol=1e-12,
        rtol=0,
    )
    assert (
        final_atoms.iloc[mapping]["atom_type"].tolist()
        == before_atoms["atom_type"].tolist()
    )
    pd.testing.assert_frame_equal(source.topology.atoms, before_atoms)
    np.testing.assert_array_equal(_coordinates(source), before_xyz)


@pytest.mark.parametrize("length_unit", ["nm", "pm"])
def test_candidate_cell_builds_caps_and_measured_extended_torsions(length_unit):
    pytest.importorskip("openmm")
    namespace = {"msm": msm}
    with puw.context(standard_units=[length_unit, "fs", "radians"]):
        _run(2, namespace)
    peptide = namespace["peptide"]
    assert msm.get(peptide, element="group", group_name=True) == [
        "ACE",
        "LYS",
        "LEU",
        "VAL",
        "PHE",
        "PHE",
        "NME",
    ]
    assert msm.get(peptide, n_atoms=True) == 109
    for name, expected in (("phi", -135.0), ("psi", 135.0)):
        quartets = msm.chemical_states.get_dihedral_quartets(peptide, **{name: True})
        assert np.shape(quartets) == (5, 4)
        angles = msm.structure.get_dihedral_angles(
            peptide, dihedral_quartets=quartets, pbc=False
        )
        np.testing.assert_allclose(
            puw.get_value(angles, to_unit="degrees"), expected, atol=2e-5, rtol=0
        )
    assert np.isfinite(_coordinates(peptide)).all()


def test_assembly_requires_a_declared_pose_before_entering_solvation(monkeypatch):
    def unexpected_solvation(*args, **kwargs):
        pytest.fail("A missing candidate pose reached solvation")

    source = _local_target()
    before = _coordinates(source)
    monkeypatch.setattr(msm.build, "solvate", unexpected_solvation)
    namespace = {
        "msm": msm,
        "fibril": source,
        "peptide": source.copy(),
        "candidate_pose_coordinates": None,
    }
    with pytest.raises(ValueError, match="candidate_pose_coordinates"):
        _run(3, namespace)
    np.testing.assert_array_equal(_coordinates(source), before)


def _assembly_before_solvation():
    statements = []
    for statement in ast.parse(_code(3)).body:
        if any(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "solvate"
            for node in ast.walk(statement)
        ):
            break
        statements.append(statement)
    return compile(
        ast.fix_missing_locations(ast.Module(body=statements, type_ignores=[])),
        str(LESSON),
        "exec",
    )


@pytest.mark.parametrize("length_unit", ["nm", "pm"])
@pytest.mark.parametrize("rank", [2, 3])
def test_merge_uses_the_supplied_prepared_pose_and_declared_model(length_unit, rank):
    target = _local_target()
    candidate = target.copy()
    before_target, before_candidate = _coordinates(target), _coordinates(candidate)
    pose = before_candidate + np.array([2.0, 0.0, 0.0])
    namespace = {
        "msm": msm,
        "fibril": target,
        "peptide": candidate,
        "candidate_pose_coordinates": puw.quantity(
            pose[0] if rank == 2 else pose, "nm"
        ),
    }
    with puw.context(standard_units=[length_unit, "fs", "radians"]):
        exec(_assembly_before_solvation(), namespace)
    merged = namespace["complex"]
    np.testing.assert_allclose(
        _coordinates(merged),
        np.concatenate([before_target, pose], axis=1),
        atol=1e-12,
        rtol=0,
    )
    assert namespace["target_atom_indices"] == list(range(22))
    assert namespace["candidate_atom_indices"] == list(range(22, 44))
    assert msm.get(merged, forcefield=True, water_model=True) == ["AMBER14", "TIP3P"]
    np.testing.assert_array_equal(_coordinates(target), before_target)
    np.testing.assert_array_equal(_coordinates(candidate), before_candidate)


def test_bounded_candidate_admits_the_declared_forcefield_without_minimizing():
    pytest.importorskip("openmm")
    namespace = {"msm": msm}
    _run(2, namespace)
    peptide = namespace["peptide"]
    before = _coordinates(peptide)
    requested = msm.convert(
        [peptide, {"forcefield": "AMBER14", "water_model": "TIP3P"}],
        to_form="molsysmt.MolSys",
    )
    energy = msm.molecular_mechanics.get_potential_energy(requested)
    assert np.isfinite(puw.get_value(energy, to_unit="kilojoule/mole")).all()
    np.testing.assert_array_equal(_coordinates(peptide), before)
    np.testing.assert_array_equal(_coordinates(requested), before)
