"""Executing the actual interface lesson against an independent sphere oracle."""

import ast
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import MolSys

ROOT = Path(__file__).resolve().parents[3]
LESSON = ROOT / "docs/content/course/Path_Alzheimer/54_Final_Project.ipynb"
TOLERANCE = json.loads(
    (ROOT / "tests/scientific_truth/evidence/tolerances.json").read_text()
)["shrake_rupley_sampling_area_atol"]["atol"]


def _code():
    cells = json.loads(LESSON.read_text())["cells"]
    return next(
        "".join(cell["source"])
        for cell in cells
        if cell["cell_type"] == "code" and "# 5." in "".join(cell["source"])
    )


def _source(distance):
    molsys = MolSys(n_atoms=3, n_groups=3)
    molsys.topology.atoms["atom_type"] = ["C", "C", "O"]
    molsys.topology.atoms["group_index"] = [0, 1, 2]
    molsys.topology.groups["group_name"] = ["ALA", "ALA", "HOH"]
    molsys.structures.append(
        coordinates=puw.quantity(
            [[[0, 0, 0], [distance, 0, 0], [distance / 2, 0, 0]]], "nm"
        ),
        box=puw.quantity([np.diag([3.0, 3.0, 3.0])], "nm"),
    )
    return molsys


@pytest.mark.parametrize("distance", [0.31, 2.9])
@pytest.mark.parametrize("length_unit", ["nm", "angstrom"])
def test_course_interface_area_tracks_geometry_not_a_group_table(
    distance, length_unit, capsys
):
    molsys = _source(distance)
    original_xyz = puw.get_value(molsys.structures.coordinates, to_unit="nm").copy()
    original_atoms = molsys.topology.atoms.copy(deep=True)
    original_groups = molsys.topology.groups.copy(deep=True)
    namespace = {
        "msm": msm,
        "final_complex": molsys,
        "target_atom_indices": [0],
        "candidate_atom_indices": [1],
    }
    with puw.context(standard_units=[length_unit, "ps", "radians"]):
        policy = {
            k: v for k, v in puw.configure.report().items() if k != "loaded_libraries"
        }
        exec(compile(_code(), str(LESSON), "exec"), namespace)
        assert {
            k: v for k, v in puw.configure.report().items() if k != "loaded_libraries"
        } == policy
    radius = (
        0.17 + 0.14
    )  # Independently specified vdW carbon radius and water-probe radius, in nm.
    expected = 2 * np.pi * radius * max(0.0, 2 * radius - distance)
    total = puw.get_value(namespace["delta_sasa"], to_unit="nm**2")
    interface = puw.get_value(namespace["interface_mean_area"], to_unit="nm**2")
    assert total.shape == interface.shape == (1,)
    np.testing.assert_allclose(total, [expected], atol=2 * TOLERANCE, rtol=0)
    np.testing.assert_allclose(interface, total / 2, atol=1e-12, rtol=0)
    for name in ("sasa_A", "sasa_B"):
        np.testing.assert_allclose(
            puw.get_value(namespace[name], to_unit="nm**2"),
            [4 * np.pi * radius**2],
            atol=1e-7,
            rtol=0,
        )
    assert namespace["molsys_AB"].topology.n_atoms == 2
    assert namespace["n_hbonds"] == 0
    pd.testing.assert_frame_equal(molsys.topology.atoms, original_atoms)
    pd.testing.assert_frame_equal(molsys.topology.groups, original_groups)
    np.testing.assert_array_equal(
        puw.get_value(molsys.structures.coordinates, to_unit="nm"), original_xyz
    )
    # Identical group names make the reference descriptor invariant to this displacement.
    np.testing.assert_array_equal(
        msm.physchem.get_area_buried(molsys, selection=[0, 1]), [86.6, 86.6]
    )
    output = capsys.readouterr().out
    assert "Total SASA loss" in output and "Mean interface area" in output
    assert "Stabilizing" not in output


@pytest.mark.parametrize(
    "target,candidate", [([], [1]), ([0], []), ([0], [0]), ([0, 0], [1])]
)
def test_course_interface_requires_two_nonempty_disjoint_unique_populations(
    target, candidate
):
    namespace = {
        "msm": msm,
        "final_complex": _source(0.31),
        "target_atom_indices": target,
        "candidate_atom_indices": candidate,
    }
    with pytest.raises(ValueError, match="nonempty|unique|disjoint"):
        exec(compile(_code(), str(LESSON), "exec"), namespace)


def test_toolbox_interface_example_uses_the_same_geometric_definition():
    tutorial = ROOT / "docs/content/user/tools/physchem/get_sasa.ipynb"
    cell = next(
        cell
        for cell in json.loads(tutorial.read_text())["cells"]
        if cell.get("id") == "sasa-interface-carbon-probes"
    )
    namespace = {"msm": msm, "puw": puw}
    exec(compile("".join(cell["source"]), str(tutorial), "exec"), namespace)
    expected = 2 * np.pi * 0.31**2
    np.testing.assert_allclose(
        puw.get_value(namespace["delta_sasa"], to_unit="nm**2"),
        [expected],
        atol=2 * TOLERANCE,
        rtol=0,
    )
    np.testing.assert_allclose(
        puw.get_value(namespace["interface_mean_area"], to_unit="nm**2"),
        [expected / 2],
        atol=TOLERANCE,
        rtol=0,
    )


def test_course_declares_partner_atom_ranges_from_actual_merge_order():
    code = next(
        "".join(cell["source"])
        for cell in json.loads(LESSON.read_text())["cells"]
        if cell["cell_type"] == "code" and "# 3." in "".join(cell["source"])
    )
    # Execute the actual map and merge statements. Solvation and full biological
    # preparation retain their independent qualification boundaries.
    statements = []
    for statement in ast.parse(code).body:
        if any(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "solvate"
            for node in ast.walk(statement)
        ):
            break
        statements.append(statement)
    target = _source(0.31)
    candidate = msm.extract(target, selection=[1])
    namespace = {
        "msm": msm,
        "fibril": target,
        "peptide": candidate,
        "candidate_pose_coordinates": msm.get(candidate, coordinates=True),
    }
    exec(
        compile(
            ast.fix_missing_locations(ast.Module(body=statements, type_ignores=[])),
            str(LESSON),
            "exec",
        ),
        namespace,
    )
    assert namespace["target_atom_indices"] == [0, 1, 2]
    assert namespace["candidate_atom_indices"] == [3]
    merged = namespace["complex"]
    np.testing.assert_array_equal(
        puw.get_value(merged.structures.coordinates, to_unit="nm"),
        np.concatenate(
            [
                puw.get_value(target.structures.coordinates, to_unit="nm"),
                puw.get_value(candidate.structures.coordinates, to_unit="nm"),
            ],
            axis=1,
        ),
    )
