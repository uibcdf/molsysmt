"""Execute biological torsion lessons with independent geometry and motion checks."""

import json
import socket
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from molsysmt import pyunitwizard as puw

COURSE = Path(__file__).parents[2] / "docs/content/course"


def coordinates(molsys):
    return puw.get_value(molsys.structures.coordinates, to_unit="nm")


def torsions(molsys, quartets):
    # Independent signed projection formula, without MolSysMT geometry kernels.
    xyz = coordinates(molsys)[0]
    result = []
    for quartet in np.asarray(quartets).reshape(-1, 4):
        a, b, c, d = xyz[quartet]
        axis = c - b
        axis /= np.linalg.norm(axis)
        first = a - b
        last = d - c
        first -= (first @ axis) * axis
        last -= (last @ axis) * axis
        result.append(np.arctan2(np.cross(axis, first) @ last, first @ last))
    return np.asarray(result)


def assert_angles(actual, expected):
    delta = actual - expected
    np.testing.assert_allclose(np.arctan2(np.sin(delta), np.cos(delta)), 0, atol=1e-7)


def assert_rotation(source, result, quartet, moving, increment):
    before, after = coordinates(source)[0], coordinates(result)[0]
    # Rodrigues reference; validate the entire output, not just one achieved angle.
    axis = before[quartet[2]] - before[quartet[1]]
    axis /= np.linalg.norm(axis)
    x, y, z = axis
    skew = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]])
    rotation = (
        np.eye(3) * np.cos(increment)
        + (1 - np.cos(increment)) * np.outer(axis, axis)
        + np.sin(increment) * skew
    )
    expected = before.copy()
    expected[moving] = (before[moving] - before[quartet[2]]) @ rotation.T + before[
        quartet[2]
    ]
    np.testing.assert_allclose(after, expected, atol=1e-10)
    fixed = np.setdiff1d(np.arange(len(before)), moving)
    assert len(fixed) > 0
    np.testing.assert_allclose(after[fixed], before[fixed], rtol=0, atol=2e-13)
    assert np.max(np.abs(after[moving] - before[moving])) > 1e-4
    assert_angles(torsions(result, quartet), torsions(source, quartet) + increment)
    for table in ("atoms", "groups", "chains", "bonds"):
        pd.testing.assert_frame_equal(
            getattr(source.topology, table), getattr(result.topology, table)
        )
    if source.structures.box is not None:
        np.testing.assert_array_equal(
            puw.get_value(source.structures.box, to_unit="nm"),
            puw.get_value(result.structures.box, to_unit="nm"),
        )


@pytest.mark.parametrize("path", ["Alzheimer", "Enzyme", "Antiviral", "Biophysics"])
@pytest.mark.parametrize("length,angle", [("nm", "radians"), ("pm", "degrees")])
def test_course_torsions_preserve_biology_geometry_and_ownership(
    path, length, angle, monkeypatch
):
    def forbidden(*args, **kwargs):
        raise AssertionError("Course examples must execute without remote lookup")

    monkeypatch.setattr(socket, "getaddrinfo", forbidden)
    notebook = COURSE / f"Path_{path}/27_Conformational_Engineering.ipynb"
    cells = json.loads(notebook.read_text())["cells"]
    scope = {}
    native_snapshot = None
    with puw.context(standard_units=[length, "ps", angle]):
        for cell in cells:
            if cell["cell_type"] == "code":
                exec(compile("".join(cell["source"]), str(notebook), "exec"), scope)
                if native_snapshot is None and "molsys" in scope:
                    native_snapshot = puw.get_value(
                        scope["molsys"].structures.coordinates
                    ).copy()
        source = scope["molsys"]
        np.testing.assert_array_equal(
            puw.get_value(source.structures.coordinates), native_snapshot
        )
        # Unit conversion can round while preserving the exact native buffer.
        np.testing.assert_allclose(
            coordinates(source), scope["original_coordinates"], rtol=0, atol=2e-13
        )
        if path == "Alzheimer":
            assert source.topology.groups.group_name.tolist() == [
                "LYS",
                "LEU",
                "VAL",
                "PHE",
                "PHE",
            ]
            assert_angles(
                torsions(scope["edited"], scope["phi_quartets"]), np.deg2rad(-135)
            )
            assert_angles(
                torsions(scope["edited"], scope["psi_quartets"]), np.deg2rad(135)
            )
            np.testing.assert_allclose(
                coordinates(scope["edited"]), scope["before_shift"], rtol=0, atol=2e-13
            )
            assert_rotation(
                scope["edited"],
                scope["shifted"],
                scope["quartet"],
                scope["moving"],
                np.deg2rad(45),
            )
        elif path in ("Enzyme", "Biophysics"):
            quartet = scope["quartet"]
            # Independently assert biological source labels on the central atom.
            atom = source.topology.atoms.iloc[quartet[1]]
            group = source.topology.groups.iloc[atom.group_index]
            chain = source.topology.chains.iloc[atom.chain_index]
            if path == "Enzyme":
                assert (chain.chain_id, group.group_id, group.group_name) == (
                    "A",
                    "159",
                    "TRP",
                )
                assert atom.atom_name == "CA"
                assert np.isfinite(torsions(source, scope["chi2_quartet"])).all()
                shift = 180
            else:
                assert (chain.chain_id, group.group_id, group.group_name) == (
                    "C",
                    "90",
                    "CYS",
                )
                assert atom.atom_name == "N"
                shift = 10
            assert_rotation(
                source, scope["edited"], quartet, scope["moving"], np.deg2rad(shift)
            )
        else:
            assert source.topology.groups.group_name.tolist() == [
                "02J",
                "ALA",
                "VAL",
                "LEU",
                "PJE",
                "010",
            ]
            assert len(source.topology.atoms) == 49
            assert source.topology.chains.chain_id.tolist() == ["C"]
            quartets = scope["quartets"]
            assert quartets.shape == (47, 4)
            assert all(len(set(q)) == 4 and q[0] < q[-1] for q in quartets)
            measured = puw.get_value(scope["angles"], to_unit="radians")[0]
            assert np.isfinite(measured).all()
            assert_angles(measured, torsions(source, quartets))
