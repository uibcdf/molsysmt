"""Exercise the structure generator's actual torsion statements without other scenes."""

import ast
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw

GENERATOR = (
    Path(__file__).resolve().parents[2]
    / "docs/generate_static_views/tools_structure.py"
)


def assignment(name, namespace):
    tree = ast.parse(GENERATOR.read_text())
    nodes = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == name
            for target in node.targets
        )
    ]
    assert len(nodes) == 1
    exec(
        compile(ast.Module(body=nodes, type_ignores=[]), str(GENERATOR), "exec"),
        namespace,
    )


def angles(molsys, quartet):
    a, b, c, d = puw.get_value(molsys.structures.coordinates, to_unit="nm")[0, quartet]
    axis = c - b
    axis /= np.linalg.norm(axis)
    first, last = a - b, d - c
    first -= (first @ axis) * axis
    last -= (last @ axis) * axis
    return np.arctan2(np.cross(axis, first) @ last, first @ last)


@pytest.mark.parametrize("units", [["nm", "ps", "radians"], ["pm", "fs", "degrees"]])
def test_actual_generator_quartets_drive_set_and_shift(units):
    with puw.context(standard_units=units):
        source = msm.convert(
            msm.systems["chicken villin HP35"]["chicken_villin_HP35.h5msm"],
            to_form="molsysmt.MolSys",
        )
        before = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
        namespace = {"msm": msm, "molsys_dih": source}
        assignment("phi_quartets", namespace)
        quartets = np.asarray(namespace["phi_quartets"])
        assert quartets.ndim == 2 and quartets.shape[1] == 4 and len(quartets) > 2
        names = np.asarray(msm.get(source, element="atom", atom_name=True))
        np.testing.assert_array_equal(
            names[quartets], np.tile(["C", "N", "CA", "C"], (len(quartets), 1))
        )
        quartet = quartets[1]
        for name, expected in [
            ("molsys_set", np.deg2rad(60)),
            ("molsys_shifted", angles(source, quartet) + np.deg2rad(90)),
        ]:
            assignment(name, namespace)
            result = namespace[name]
            delta = angles(result, quartet) - expected
            assert abs(np.arctan2(np.sin(delta), np.cos(delta))) < 1e-7
            assert result is not source
        np.testing.assert_array_equal(
            puw.get_value(source.structures.coordinates, to_unit="nm"), before
        )
