"""Analytic sphere areas and an independently constructed MDTraj SASA oracle."""

import json
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import MolSys

# Explicit reference radii in nm, not values obtained from MolSysMT's radius table.
_RADIUS = 0.17
_PROBE = 0.14
_POINTS = 960
_TOLERANCE = json.loads(
    (Path(__file__).parents[1] / "evidence/tolerances.json").read_text()
)["shrake_rupley_sampling_area_atol"]["atol"]


def _native(coordinates):
    system = MolSys(n_atoms=len(coordinates))
    system.topology.atoms["atom_type"] = ["C"] * len(coordinates)
    system.structures.append(
        coordinates=msm.pyunitwizard.quantity(np.array([coordinates]), "nm")
    )
    return msm.pyunitwizard.get_value(
        msm.physchem.get_sasa(
            system,
            probe_radius="0.14 nm",
            n_sphere_points=_POINTS,
            use_cell_list=False,
            use_gpu=False,
        ),
        to_unit="nm**2",
    )


@pytest.mark.parametrize(
    "coordinates", [[[0.0, 0.0, 0.0]], [[0.0, 0.0, 0.0], [2.0, 0.0, 0.0]]]
)
def test_isolated_carbon_spheres_match_closed_form(coordinates, external_float32_atol):
    expected = np.full((1, len(coordinates)), 4 * np.pi * (_RADIUS + _PROBE) ** 2)
    np.testing.assert_allclose(
        _native(coordinates), expected, atol=external_float32_atol, rtol=0
    )


def test_overlap_matches_spherical_cap_area():
    radius = _RADIUS + _PROBE
    expected = np.full((1, 2), 2 * np.pi * radius**2 + np.pi * radius * radius)
    np.testing.assert_allclose(
        _native([[0.0, 0.0, 0.0], [radius, 0.0, 0.0]]),
        expected,
        atol=_TOLERANCE,
        rtol=0,
    )


def test_native_sasa_agrees_with_independently_constructed_mdtraj():
    md = pytest.importorskip("mdtraj")
    coordinates = [[0.0, 0.0, 0.0], [_RADIUS + _PROBE, 0.0, 0.0]]
    topology = md.Topology()
    group = topology.add_residue("LIG", topology.add_chain())
    topology.add_atom("C1", md.element.carbon, group)
    topology.add_atom("C2", md.element.carbon, group)
    trajectory = md.Trajectory(np.array([coordinates], dtype=np.float32), topology)
    expected = md.shrake_rupley(
        trajectory,
        probe_radius=_PROBE,
        n_sphere_points=_POINTS,
        mode="atom",
        change_radii={"C": _RADIUS},
    )
    np.testing.assert_allclose(_native(coordinates), expected, atol=_TOLERANCE, rtol=0)


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("cell", [False, True])
@pytest.mark.parametrize("pbc", [False, True])
def test_opposite_faces_match_independent_spherical_cap(unit, cell, pbc):
    """Check a literal two-sphere MIC construction against a closed-form area."""
    puw = msm.pyunitwizard
    molsys = MolSys(n_atoms=2)
    molsys.topology.atoms["atom_type"] = ["C", "C"]
    molsys.structures.append(
        coordinates=puw.quantity([[[0.1, 0, 0], [1.9, 0, 0]]], "nm"),
        box=puw.quantity([np.diag([2.0, 2.0, 2.0])], "nm"),
    )
    radius = _RADIUS + _PROBE
    expected = (
        2 * np.pi * radius**2 + np.pi * radius * 0.2 if pbc else 4 * np.pi * radius**2
    )
    with puw.context(standard_units=[unit, "ps", "radians"]):
        actual = msm.physchem.get_sasa(
            molsys,
            probe_radius="140 pm",
            n_sphere_points=_POINTS,
            use_cell_list=cell,
            use_gpu=False,
            pbc=pbc,
        )
        np.testing.assert_allclose(
            puw.get_value(actual, to_unit="nm**2"),
            [[expected, expected]],
            atol=_TOLERANCE,
            rtol=0,
        )
