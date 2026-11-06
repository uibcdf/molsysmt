"""Check native minimization ownership and actual course-call continuation."""

import ast
import inspect
import json
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw

pytest.importorskip("openmm")

ROOT = Path(__file__).resolve().parents[3]
COURSE = ROOT / "docs/content/course"
LESSONS = [
    f"Path_{name}/43_Energy_Minimization.ipynb"
    for name in ["Alzheimer", "Enzyme", "Antiviral", "Biophysics"]
] + ["Path_Alzheimer/54_Final_Project.ipynb"]


@pytest.mark.parametrize("platform", ["CPU", "Reference"])
@pytest.mark.parametrize("in_place", [False, True])
def test_native_minimization_ownership_coordinates_energy_and_units(
    alanine_molsys, platform, in_place
):
    molsys = msm.extract(alanine_molsys, structure_indices=0)
    original = puw.get_value(molsys.get(coordinates=True), to_unit="nm").copy()
    with puw.context(
        standard_units=["angstrom", "ps", "kcal/mol", "e", "K", "radians"]
    ):
        policy = {
            k: v for k, v in puw.configure.report().items() if k != "loaded_libraries"
        }
        before = msm.molecular_mechanics.get_potential_energy(molsys, platform=platform)
        result = msm.molecular_mechanics.potential_energy_minimization(
            molsys, platform=platform, in_place=in_place
        )
        if in_place:
            assert result is None
            minimized = molsys
        else:
            assert isinstance(result, type(molsys))
            assert result is not molsys
            minimized = result
            np.testing.assert_array_equal(
                puw.get_value(molsys.structures.coordinates, to_unit="nm"), original
            )
        coordinates = puw.get_value(minimized.get(coordinates=True), to_unit="nm")
        assert coordinates.shape == original.shape
        assert np.isfinite(coordinates).all()
        assert np.max(np.abs(coordinates - original)) > 1e-5
        after = msm.molecular_mechanics.get_potential_energy(
            minimized, platform=platform
        )
        assert puw.get_unit(before) == puw.unit("kcal/mol")
        assert puw.get_unit(after) == puw.unit("kcal/mol")
        before_value = puw.get_value(before, to_unit="kJ/mol")
        after_value = puw.get_value(after, to_unit="kJ/mol")
        assert np.isfinite([before_value, after_value]).all()
        assert after_value < before_value - 1e-4
        assert {
            k: v for k, v in puw.configure.report().items() if k != "loaded_libraries"
        } == policy


@pytest.mark.parametrize("lesson", LESSONS)
def test_course_minimization_keeps_the_minimized_system_for_later_steps(
    alanine_molsys, lesson
):
    notebook = json.loads((COURSE / lesson).read_text())
    code = "\n\n".join(
        "".join(c["source"]) for c in notebook["cells"] if c["cell_type"] == "code"
    )
    tree = ast.parse(code)
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "potential_energy_minimization"
    ]
    assert len(calls) == 1
    call = calls[0]
    # Check the actual public keyword contract; no invented compatibility alias.
    assert all(keyword.arg is not None for keyword in call.keywords)
    inspect.signature(msm.molecular_mechanics.potential_energy_minimization).bind(
        *[object() for _ in call.args],
        **{keyword.arg: object() for keyword in call.keywords},
    )
    assert isinstance(call.args[0], ast.Name)
    system_name = call.args[0].id
    parents = {
        child: parent
        for parent in ast.walk(tree)
        for child in ast.iter_child_nodes(parent)
    }
    statement = parents[call]
    assert isinstance(statement, (ast.Expr, ast.Assign))
    assert statement.value is call
    molsys = msm.extract(alanine_molsys, structure_indices=0)
    original = puw.get_value(molsys.get(coordinates=True), to_unit="nm").copy()
    before = msm.molecular_mechanics.get_potential_energy(molsys, platform="CPU")
    namespace = {"msm": msm, system_name: molsys}
    # Execute the actual lesson call on a bounded bundled model, not its
    # network/download/ligand/membrane preparation or graphical scene.
    executable = ast.fix_missing_locations(
        ast.Module(body=[statement], type_ignores=[])
    )
    exec(compile(executable, str(COURSE / lesson), "exec"), namespace)
    minimized = namespace[system_name]
    coordinates = puw.get_value(minimized.get(coordinates=True), to_unit="nm")
    assert np.max(np.abs(coordinates - original)) > 1e-5, (
        "The lesson continues with unminimized coordinates"
    )
    explicit_in_place = any(
        k.arg == "in_place" and ast.literal_eval(k.value) is True for k in call.keywords
    )
    if not explicit_in_place:
        assert minimized is not molsys
        np.testing.assert_array_equal(
            puw.get_value(molsys.get(coordinates=True), to_unit="nm"), original
        )
    after = msm.molecular_mechanics.get_potential_energy(minimized, platform="CPU")
    assert (
        puw.get_value(after, to_unit="kJ/mol")
        < puw.get_value(before, to_unit="kJ/mol") - 1e-4
    )
    # Later energy/view calls must receive the system that was actually relaxed.
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in {"get_potential_energy", "view"}
            and node.lineno > call.lineno
        ):
            assert isinstance(node.args[0], ast.Name)
            assert namespace[node.args[0].id] is minimized
