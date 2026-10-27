"""Check physical SASA area against analytic spheres under independent unit policies."""

import json
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import MolSys

TOLERANCES = json.loads(
    (
        Path(__file__).parents[2] / "scientific_truth/evidence/tolerances.json"
    ).read_text()
)
EXACT = TOLERANCES["external_float32_atol"]["atol"]
SAMPLED = TOLERANCES["shrake_rupley_sampling_area_atol"]["atol"]
RADIUS = 0.17
PROBE = 0.14


def carbon_system(coordinates, coordinate_unit="nm", groups=None, box=None):
    xyz = np.asarray(coordinates, dtype=float)
    if groups is None:
        groups = [0] * xyz.shape[1]
    source = MolSys(n_atoms=xyz.shape[1], n_groups=max(groups) + 1, n_chains=1)
    source.topology.atoms["atom_type"] = ["C"] * xyz.shape[1]
    source.topology.atoms["atom_name"] = [f"C{i}" for i in range(xyz.shape[1])]
    source.topology.atoms["atom_id"] = [str(17 + i * 3) for i in range(xyz.shape[1])]
    source.topology.atoms["group_index"] = groups
    source.topology.atoms["chain_index"] = [0] * xyz.shape[1]
    source.topology.groups["group_name"] = ["LIG"] * (max(groups) + 1)
    source.topology.groups["group_id"] = [
        str(7 + i * 2) for i in range(max(groups) + 1)
    ]
    source.topology.chains["chain_id"] = ["A"]
    source.structures.coordinates = puw.quantity(xyz, coordinate_unit)
    if box is not None:
        source.structures.box = puw.quantity(
            np.asarray(box, dtype=float), coordinate_unit
        )
    return source


CASES = [
    (engine, cell)
    for engine in ("MolSysMT", "MDTraj")
    for cell in ((False, True) if engine == "MolSysMT" else (False,))
]


@pytest.mark.parametrize("standard", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize(
    "input_unit,scale", [("nm", 1), ("angstrom", 10), ("pm", 1000)]
)
@pytest.mark.parametrize("engine,cell", CASES)
@pytest.mark.parametrize("element", ["atom", "group"])
@pytest.mark.parametrize("probe", ["0.14 nm", "1.4 angstroms", "140 pm"])
def test_isolated_carbon_area_is_physical_under_unit_contexts(
    standard, input_unit, scale, engine, cell, element, probe
):
    if engine == "MDTraj":
        pytest.importorskip("mdtraj")
    source = carbon_system(
        np.array([[[0, 0, 0]], [[1, 2, 3]], [[0.2, 0.3, 0.4]]]) * scale, input_unit
    )
    original = puw.get_value(source.structures.coordinates).copy()
    with puw.context(
        standard_units=[standard, "ps", "radians", "dalton", "e", "dimensionless"]
    ):
        before = puw.configure.get_standard_units()
        area = msm.physchem.get_sasa(
            source,
            element=element,
            structure_indices=[2, 0, 2],
            engine=engine,
            probe_radius=probe,
            n_sphere_points=960,
            use_gpu=False,
            use_cell_list=cell,
        )
        assert puw.check(area, dimensionality={"[L]": 2})
        assert area.shape == (3, 1)
        np.testing.assert_allclose(
            puw.get_value(area, to_unit="nm**2"),
            4 * np.pi * (RADIUS + PROBE) ** 2,
            rtol=0,
            atol=EXACT,
        )
        assert puw.configure.get_standard_units() == before
    np.testing.assert_array_equal(
        puw.get_value(source.structures.coordinates), original
    )
    assert source.structures.box is None


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("cell", [False, True])
@pytest.mark.parametrize("element", ["atom", "group"])
def test_grouped_overlap_and_isolated_area_keep_units_and_all_occluders(
    unit, cell, element
):
    source = carbon_system([[[0, 0, 0], [0.31, 0, 0], [2, 0, 0]]], groups=[0, 0, 1])
    inflated = RADIUS + PROBE
    cap = 2 * np.pi * inflated**2 + np.pi * inflated * 0.31
    sphere = 4 * np.pi * inflated**2
    expected = [[cap, cap, sphere]] if element == "atom" else [[2 * cap, sphere]]
    with puw.context(standard_units=[unit, "ps", "radians"]):
        area = msm.physchem.get_sasa(
            source,
            element=element,
            use_cell_list=cell,
            use_gpu=False,
            n_sphere_points=960,
        )
        np.testing.assert_allclose(
            puw.get_value(area, to_unit="nm**2"),
            expected,
            rtol=0,
            atol=SAMPLED * (2 if element == "group" else 1),
        )
        selected = msm.physchem.get_sasa(
            source,
            element="atom",
            selection=[0],
            use_cell_list=cell,
            use_gpu=False,
            n_sphere_points=960,
        )
        np.testing.assert_allclose(
            puw.get_value(selected, to_unit="nm**2"), [[cap]], rtol=0, atol=SAMPLED
        )


@pytest.mark.parametrize("form", ["native", "composite", "mdtraj.Trajectory"])
@pytest.mark.parametrize("engine", ["MolSysMT", "MDTraj"])
def test_unit_safe_sasa_uses_supported_form_attributes(form, engine):
    if form == "mdtraj.Trajectory" or engine == "MDTraj":
        pytest.importorskip("mdtraj")
    source = carbon_system([[[0, 0, 0]]])
    item = (
        source
        if form == "native"
        else [source.topology, source.structures]
        if form == "composite"
        else msm.convert(source, to_form=form)
    )
    with puw.context(standard_units=["pm", "ps", "radians"]):
        area = msm.physchem.get_sasa(
            item, engine=engine, pbc=False, use_gpu=False, n_sphere_points=960
        )
        np.testing.assert_allclose(
            puw.get_value(area, to_unit="nm**2"),
            [[4 * np.pi * (RADIUS + PROBE) ** 2]],
            rtol=0,
            atol=EXACT,
        )
