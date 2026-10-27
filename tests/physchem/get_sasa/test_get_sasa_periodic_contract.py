"""Check explicit Cartesian/MIC SASA semantics against analytic carbon spheres."""

import inspect

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError, NotImplementedMethodError
from tests.physchem.get_sasa.test_get_sasa_units import EXACT, SAMPLED, carbon_system

R = 0.31
SPHERE = 4 * np.pi * R**2


def periodic_pair(box_kind="orthogonal"):
    box = np.diag([2.0, 2.0, 2.0])
    if box_kind == "triclinic":
        box[1, 0] = 0.2
        box[2, :2] = [0.1, 0.2]
    coordinates = [
        [[0.1, 0, 0], [1.9, 0, 0]],
        [[0.1, 0, 0], [1.1, 0, 0]],
        [[0.1, 0, 0], [0.3, 0, 0]],
    ]
    return carbon_system(coordinates, box=np.repeat(box[None], 3, axis=0))


@pytest.mark.parametrize("engine", ["MolSysMT", "MDTraj"])
@pytest.mark.parametrize("pbc", [True, False])
@pytest.mark.parametrize("box_kind", ["orthogonal", "triclinic"])
@pytest.mark.parametrize("unit", ["nm", "angstrom", "pm"])
@pytest.mark.parametrize("element", ["atom", "group"])
def test_selected_structures_observe_explicit_periodic_contract(
    engine, pbc, box_kind, unit, element
):
    if engine == "MDTraj":
        pytest.importorskip("mdtraj")
    source = periodic_pair(box_kind)
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    box = puw.get_value(source.structures.box, to_unit="nm").copy()
    kwargs = dict(
        engine=engine,
        pbc=pbc,
        element=element,
        structure_indices=[2, 0, 1, 2],
        use_gpu=False,
        use_cell_list=False,
        n_sphere_points=960,
    )
    with puw.context(standard_units=[unit, "ps", "radians"]):
        if engine == "MDTraj" and pbc:
            with pytest.raises(NotImplementedMethodError, match="periodic"):
                msm.physchem.get_sasa(source, **kwargs)
        else:
            # In selected structures 2 and 0, MIC separation is .2 nm. Direct
            # Cartesian separation in structure 0 is 1.8 nm (no overlap).
            cap = 2 * np.pi * R**2 + np.pi * R * 0.2
            per_atom = np.array(
                [[cap] * 2, [(cap if pbc else SPHERE)] * 2, [SPHERE] * 2, [cap] * 2]
            )
            expected = (
                per_atom if element == "atom" else per_atom.sum(axis=1, keepdims=True)
            )
            area = msm.physchem.get_sasa(source, **kwargs)
            assert area.shape == expected.shape
            np.testing.assert_allclose(
                puw.get_value(area, to_unit="nm**2"),
                expected,
                rtol=0,
                atol=SAMPLED * (2 if element == "group" else 1),
            )
    np.testing.assert_array_equal(
        puw.get_value(source.structures.coordinates, to_unit="nm"), xyz
    )
    np.testing.assert_array_equal(
        puw.get_value(source.structures.box, to_unit="nm"), box
    )


def test_boxed_mdtraj_default_rejects_implicit_cartesian_fallback():
    pytest.importorskip("mdtraj")
    with pytest.raises(NotImplementedMethodError, match="periodic"):
        msm.physchem.get_sasa(periodic_pair(), engine="MDTraj", use_gpu=False)


@pytest.mark.parametrize("engine", ["MolSysMT", "MDTraj"])
@pytest.mark.parametrize("pbc", [True, False])
def test_missing_box_is_cartesian_for_both_engines(engine, pbc):
    if engine == "MDTraj":
        pytest.importorskip("mdtraj")
    source = carbon_system([[[0, 0, 0], [2, 0, 0]]])
    area = msm.physchem.get_sasa(
        source, engine=engine, pbc=pbc, use_gpu=False, n_sphere_points=960
    )
    np.testing.assert_allclose(
        puw.get_value(area, to_unit="nm**2"), [[SPHERE] * 2], rtol=0, atol=EXACT
    )


@pytest.mark.parametrize("box_kind", ["orthogonal", "triclinic"])
@pytest.mark.parametrize("pbc", [True, False])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_periodic_cell_candidates_and_lattice_images_match(box_kind, pbc, unit):
    source = periodic_pair(box_kind)
    kwargs = dict(
        pbc=pbc, structure_indices=[2, 0, 2], use_gpu=False, n_sphere_points=960
    )
    with puw.context(standard_units=[unit, "ps", "radians"]):
        brute = msm.physchem.get_sasa(source, use_cell_list=False, **kwargs)
        cell = msm.physchem.get_sasa(source, use_cell_list=True, **kwargs)
        np.testing.assert_allclose(
            puw.get_value(cell, to_unit="nm**2"),
            puw.get_value(brute, to_unit="nm**2"),
            rtol=0,
            atol=1e-12,
        )
        if pbc:
            shifted = msm.copy(source)
            xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
            boxes = puw.get_value(source.structures.box, to_unit="nm")
            xyz[:, 1, :] += boxes[:, 0, :]
            msm.set(shifted, coordinates=puw.quantity(xyz, "nm"))
            translated = msm.physchem.get_sasa(shifted, use_cell_list=True, **kwargs)
            np.testing.assert_allclose(
                puw.get_value(translated, to_unit="nm**2"),
                puw.get_value(brute, to_unit="nm**2"),
                rtol=0,
                atol=1e-12,
            )


def test_new_control_preserves_original_positional_arguments():
    source = carbon_system([[[0, 0, 0]]])
    signature = inspect.signature(msm.physchem.get_sasa)
    assert signature.parameters["pbc"].kind == inspect.Parameter.KEYWORD_ONLY
    assert signature.parameters["pbc"].default is True
    positional = (
        source,
        "atom",
        "all",
        "all",
        "MolSysMT",
        "MolSysMT",
        "1.4 angstroms",
        960,
        False,
        False,
        None,
        None,
        None,
        False,
    )
    area = msm.physchem.get_sasa(*positional, pbc=False)
    np.testing.assert_allclose(
        puw.get_value(area, to_unit="nm**2"), [[SPHERE]], rtol=0, atol=EXACT
    )


@pytest.mark.parametrize("invalid", [None, "auto", 0, 1])
def test_periodic_control_is_validated(invalid):
    with pytest.raises(ArgumentError):
        msm.physchem.get_sasa(carbon_system([[[0, 0, 0]]]), pbc=invalid)
