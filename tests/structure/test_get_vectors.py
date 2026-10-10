"""Qualify directed geometry against independent indexed-coordinate controls."""

from importlib.util import find_spec
from itertools import product

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import (
    ArgumentError,
    MemoryBudgetExceededError,
    MemoryPressureWarning,
    NotImplementedMethodError,
    StructuralInconsistencyError,
)
from molsysmt.native import Structures


def system(box=None):
    xyz = np.array(
        [
            [[0, 0, 0], [3, 4, 0], [0, 0, 2]],
            [[1, 2, 0], [4, 6, 0], [1, 2, 3]],
            [[2, 4, 0], [5, 8, 0], [2, 4, 4]],
        ],
        dtype=float,
    )
    return Structures(
        coordinates=puw.quantity(xyz, "nm"), box=box, structure_id=["91", "4", "27"]
    )


def values(result):
    return puw.get_value(result, to_unit="nm")


@pytest.mark.parametrize("heavy_mode", ["off", "force"])
def test_ordered_repeated_pairs_reversed_vectors_and_parallel_outputs(heavy_mode):
    source = system()
    before = source._coordinates.copy()
    result = msm.structure.get_vectors(
        source,
        selection=[[1, 0], [0, 1], [1, 0]],
        pairs=True,
        structure_indices=[2, 0, 2],
        pbc=False,
        output_type="dictionary",
        heavy_mode=heavy_mode,
        num_threads=2,
        parallel=True,
    )
    expected = np.array([[-3, -4, 0], [3, 4, 0], [-3, -4, 0]], dtype=float)
    np.testing.assert_array_equal(
        values(result["vectors"]), np.repeat(expected[None], 3, axis=0)
    )
    np.testing.assert_allclose(values(result["distances"]), 5)
    np.testing.assert_allclose(
        result["directions"], np.repeat((expected / 5)[None], 3, axis=0)
    )
    assert result["atom_indices"].tolist() == [1, 0, 1]
    assert result["atom_indices_2"].tolist() == [0, 1, 0]
    assert result["structure_indices"].tolist() == [2, 0, 2]
    assert result["image_vectors"].dtype == np.int32
    np.testing.assert_array_equal(source._coordinates, before)


@pytest.mark.parametrize("heavy_mode", ["off", "force"])
def test_aligned_structure_lists_between_sources_and_endpoint_centers(heavy_mode):
    first = system()
    second = Structures(coordinates=puw.quantity(first._coordinates + 10, "nm"))
    result = msm.structure.get_vectors(
        first,
        selection=[[0, 1], [2]],
        molecular_system_2=second,
        selection_2=[[1], [0, 2]],
        weights=[[1, 3], [1]],
        structure_indices=[2, 0, 2],
        structure_indices_2=[0, 1, 2],
        pairs=True,
        pbc=False,
        output_type="dictionary",
        heavy_mode=heavy_mode,
    )
    a = first._coordinates[[2, 0, 2]]
    b = second._coordinates[[0, 1, 2]]
    expected = np.stack(
        (b[:, 1] - (a[:, 0] + 3 * a[:, 1]) / 4, (b[:, 0] + b[:, 2]) / 2 - a[:, 2]),
        axis=1,
    )
    np.testing.assert_allclose(values(result["vectors"]), expected)
    assert result["atom_offsets"].tolist() == [0, 2, 3]
    assert result["structure_indices_2"].tolist() == [0, 1, 2]
    assert result["parameters"]["center_of_atoms"] is True
    assert result["parameters"]["sense"] == "first_to_second"
    np.testing.assert_array_equal(result["parameters"]["relative_weights"], [1, 3, 1])


def test_cartesian_product_and_distance_contract():
    source = system()
    observed = msm.structure.get_vectors(
        source, selection=[2, 0], selection_2=[1, 2], pbc=False
    )
    expected = (
        source._coordinates[:, None, [1, 2]] - source._coordinates[:, [2, 0], None]
    )
    assert observed.shape == (3, 2, 2, 3)
    np.testing.assert_array_equal(values(observed), expected)
    scalar = msm.structure.get_distances(
        source, selection=[2, 0], selection_2=[1, 2], pbc=False
    )
    np.testing.assert_allclose(
        np.linalg.norm(values(observed), axis=-1), values(scalar)
    )


def test_implicit_centers_retain_weights_between_structures():
    source = system()
    result = msm.structure.get_vectors(
        source,
        selection=[0, 1],
        center_of_atoms=True,
        weights=[1, 3],
        structure_indices=[0, 0],
        structure_indices_2=[1, 2],
        pairs=True,
        pbc=False,
    )
    np.testing.assert_allclose(values(result)[:, 0], [[1, 2, 0], [2, 4, 0]])


def test_array_indices_and_zero_vector_dictionary():
    source = system()
    a, b, s, t, result = msm.structure.get_vectors(
        source,
        selection=[2, 0],
        selection_2=[2, 0],
        pairs=True,
        structure_indices=[2, 0],
        pbc=False,
        output_indices="atom",
        output_structure_indices="structure",
    )
    np.testing.assert_array_equal(a, [2, 0])
    np.testing.assert_array_equal(b, a)
    np.testing.assert_array_equal(s, [2, 0])
    np.testing.assert_array_equal(t, s)
    assert result.shape == (2, 2, 3)
    result = msm.structure.get_vectors(
        source, selection=[0], pbc=False, output_type="dictionary"
    )
    np.testing.assert_array_equal(values(result["vectors"]), 0)
    np.testing.assert_array_equal(values(result["distances"]), 0)
    assert np.isnan(result["directions"]).all()


@pytest.mark.parametrize("heavy_mode", ["off", "force"])
def test_units_and_coordinates_only_h5msm_selection(tmp_path, heavy_mode):
    source = system()
    path = str(tmp_path / "coordinates.h5msm")
    msm.convert(source, to_form=path)
    with puw.context(standard_units=["angstrom", "ps"]):
        result = msm.structure.get_vectors(
            path,
            selection=[0],
            selection_2=[1],
            structure_indices=[2, 0],
            pbc=False,
            heavy_mode=heavy_mode,
        )
        assert puw.has_unit(result, "angstrom")
        np.testing.assert_allclose(
            puw.get_value(result)[:, 0, 0], [[30, 40, 0], [30, 40, 0]]
        )


def test_raw_quantity_form_and_input_length_unit():
    xyz = puw.quantity(system()._coordinates * 10, "angstrom")
    observed = msm.structure.get_vectors(xyz, selection=[0], selection_2=[1], pbc=False)
    np.testing.assert_allclose(values(observed)[:, 0, 0], [[3, 4, 0]] * 3)


@pytest.mark.parametrize(
    "box",
    [
        np.diag([10.0, 10.0, 10.0]),
        np.array([[4.0, 0.0, 0.0], [3.8, 1.0, 0.0], [0.3, 0.2, 3.0]]),
    ],
)
def test_periodic_vectors_images_against_exhaustive_lattice_oracle(box):
    xyz = np.array([[[0.1, 0.1, 0.1], [3.3, 2.2, 0.2]]])
    source = Structures(
        coordinates=puw.quantity(xyz, "nm"), box=puw.quantity(box[None], "nm")
    )
    result = msm.structure.get_vectors(
        source, selection=[[0, 1]], pairs=True, output_type="dictionary"
    )
    raw = xyz[0, 1] - xyz[0, 0]
    lattice = np.array(list(product(range(-8, 9), repeat=3)))
    candidates = raw + lattice @ box
    expected = candidates[np.argmin(np.linalg.norm(candidates, axis=1))]
    np.testing.assert_allclose(values(result["vectors"])[0, 0], expected, atol=1e-12)
    np.testing.assert_allclose(
        raw + result["image_vectors"][0, 0] @ box, expected, atol=1e-12
    )


def test_first_structure_box_and_half_box_tie_are_explicit():
    source = Structures(
        coordinates=puw.quantity([[[0.0, 0.0, 0.0]], [[6.0, 0.0, 0.0]]], "nm"),
        box=puw.quantity(
            [np.diag([10.0, 10.0, 10.0]), np.diag([20.0, 20.0, 20.0])], "nm"
        ),
    )
    result = msm.structure.get_vectors(
        source,
        selection=[0],
        structure_indices=[0],
        structure_indices_2=[1],
        pairs=True,
        output_type="dictionary",
    )
    np.testing.assert_allclose(values(result["vectors"]), [[[-4, 0, 0]]])
    np.testing.assert_array_equal(result["image_vectors"], [[[-1, 0, 0]]])
    source = Structures(
        coordinates=puw.quantity([[[0.0, 0.0, 0.0]], [[5.0, 0.0, 0.0]]], "nm"),
        box=puw.quantity(
            [np.diag([10.0, 10.0, 10.0]), np.diag([20.0, 20.0, 20.0])], "nm"
        ),
    )
    np.testing.assert_allclose(
        values(
            msm.structure.get_vectors(
                source,
                selection=[0],
                structure_indices=[0],
                structure_indices_2=[1],
                pairs=True,
            )
        ),
        [[[-5, 0, 0]]],
    )


def test_split_periodic_centers_are_rejected_without_mutation():
    source = Structures(
        coordinates=puw.quantity([[[0.1, 0, 0], [9.9, 0, 0]]], "nm"),
        box=puw.quantity([np.diag([10.0, 10.0, 10.0])], "nm"),
    )
    before = source._coordinates.copy()
    with pytest.raises(NotImplementedMethodError):
        msm.structure.get_vectors(source, selection=[0, 1], center_of_atoms=True)
    np.testing.assert_array_equal(source._coordinates, before)


@pytest.mark.parametrize(
    "selection,structures,shape", [([], [0], (1, 0, 3, 3)), ([0], [], (0, 1, 3, 3))]
)
def test_typed_empty_axes(selection, structures, shape):
    result = msm.structure.get_vectors(
        system(),
        selection=selection,
        selection_2="all",
        structure_indices=structures,
        pbc=False,
        output_type="dictionary",
    )
    assert result["vectors"].shape == shape
    assert result["image_vectors"].shape == shape
    assert result["distances"].shape == shape[:-1]
    assert result["atom_indices"].dtype == np.int64


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(selection=[-1]),
        dict(structure_indices=[99]),
        dict(structure_indices=[0], structure_indices_2=[0, 1]),
        dict(selection=[0], selection_2=[0, 1], pairs=True),
        dict(selection=[0, 1], center_of_atoms=True, weights=[0, 0]),
        dict(output_type="typo"),
        dict(selection=[0], weights=[1]),
    ],
)
def test_invalid_contracts_fail(kwargs):
    with pytest.raises(ArgumentError):
        msm.structure.get_vectors(system(), pbc=False, **kwargs)


def test_nonfinite_coordinates_and_singular_box_fail():
    xyz = system()._coordinates.copy()
    xyz[0, 0, 0] = np.nan
    source = Structures(coordinates=puw.quantity(xyz, "nm"))
    with pytest.raises(StructuralInconsistencyError):
        msm.structure.get_vectors(source, pbc=False)
    source = system(box=puw.quantity(np.zeros((3, 3, 3)), "nm"))
    with pytest.raises(StructuralInconsistencyError):
        msm.structure.get_vectors(source)


def test_budget_preflight_rejects_cartesian_product_but_accepts_sparse_pairs(
    monkeypatch,
):
    source = Structures(coordinates=puw.quantity(np.zeros((1, 1000, 3)), "nm"))
    monkeypatch.setattr(msm.configure, "max_ram_usage", 2_000_000)
    with pytest.raises(MemoryBudgetExceededError):
        msm.structure.get_vectors(source, pbc=False)
    result = msm.structure.get_vectors(
        source, selection=[1, 2], selection_2=[3, 4], pairs=True, pbc=False
    )
    assert result.shape == (1, 2, 3)


def test_second_center_and_mass_weighted_center():
    source = system()
    observed = msm.structure.get_vectors(
        source, selection=[0, 1], center_of_atoms_2=True, pbc=False
    )
    expected = (
        source._coordinates[:, [0, 1]].mean(axis=1)[:, None, None]
        - source._coordinates[:, [0, 1], None]
    )
    np.testing.assert_allclose(values(observed), expected)
    source = msm.convert(
        msm.systems["alanine dipeptide"]["alanine_dipeptide.h5msm"],
        to_form="molsysmt.MolSys",
    )
    observed = msm.structure.get_vectors(
        source,
        selection=[0, 1, 2],
        center_of_atoms=True,
        weights="masses",
        selection_2=[3],
        pbc=False,
    )
    masses = puw.get_value(
        msm.physchem.get_mass(source, element="atom", selection=[0, 1, 2])
    )
    center = np.average(source.structures._coordinates[:, :3], axis=1, weights=masses)
    np.testing.assert_allclose(
        values(observed)[:, 0, 0], source.structures._coordinates[:, 3] - center
    )


def test_forced_blocks_for_independent_structure_axes_are_bounded(monkeypatch):
    from molsysmt.structure._vectors import VectorsReducer

    seen = []
    consume = VectorsReducer.consume

    def recorded(self, chunk):
        seen.append(len(chunk["coordinates"]))
        return consume(self, chunk)

    monkeypatch.setattr(VectorsReducer, "consume", recorded)
    monkeypatch.setattr(msm.configure, "max_ram_usage", 8000)
    with pytest.warns(MemoryPressureWarning):
        result = msm.structure.get_vectors(
            system(),
            selection=[0],
            selection_2=[1],
            structure_indices=[0, 2, 0],
            structure_indices_2=[2, 0, 2],
            pairs=True,
            pbc=False,
            heavy_mode="force",
        )
    np.testing.assert_allclose(values(result)[:, 0], [[5, 8, 0], [1, 0, 0], [5, 8, 0]])
    assert seen == [1, 1, 1]


def test_declared_donor_pairs_compose_without_chemical_reinterpretation():
    import pandas as pd

    from molsysmt.native import MolSys, Topology

    topology = Topology(n_atoms=3)
    topology.atoms["atom_type"] = ["O", "H", "H"]
    topology.bonds = pd.DataFrame(
        dict(atom1_index=[0, 0], atom2_index=[1, 2], bond_type=["covalent", "covalent"])
    )
    topology._chemical_states_domain._states[0].connectivity_completeness = "complete"
    source = MolSys()
    source.topology = topology
    source.structures = Structures(
        coordinates=puw.quantity(
            [[[0.0, 0.0, 0.0], [0.1, 0.0, 0.0], [0.0, 0.1, 0.0]]], "nm"
        )
    )
    sites = msm.interactions.hbonds.get_hbond_sites(source)
    pairs = sites["donor_hydrogen_pairs"]
    assert len(pairs) > 0
    result = msm.structure.get_vectors(
        source, selection=pairs, pairs=True, pbc=False, output_type="dictionary"
    )
    expected = (
        source.structures._coordinates[:, pairs[:, 1]]
        - source.structures._coordinates[:, pairs[:, 0]]
    )
    np.testing.assert_allclose(values(result["vectors"]), expected)
    np.testing.assert_allclose(
        result["directions"], expected / np.linalg.norm(expected, axis=-1)[..., None]
    )


@pytest.mark.parametrize(
    "backend,module",
    [
        ("pint", "pint"),
        ("openmm.unit", "openmm"),
        ("unyt", "unyt"),
        ("astropy.units", "astropy"),
    ],
)
def test_output_backend_and_unit_policy_are_preserved(backend, module):
    if find_spec(module) is None:
        pytest.skip(f"Optional quantity backend: {module}")
    source = system()
    with puw.context(default_form=backend, standard_units=["angstrom", "ps"]):
        result = msm.structure.get_vectors(
            source,
            selection=[0],
            selection_2=[1],
            pairs=True,
            pbc=False,
            output_type="dictionary",
        )
        for name in ("vectors", "distances"):
            assert puw.get_form(result[name]) == backend
            assert puw.has_unit(result[name], "angstrom")
        np.testing.assert_allclose(
            values(result["vectors"])[:, 0], [[3.0, 4.0, 0.0]] * 3
        )
        np.testing.assert_allclose(result["directions"][:, 0], [[0.6, 0.8, 0.0]] * 3)


def test_native_strided_inputs_and_shape_rejection():
    from molsysmt import _rust

    first = system()._coordinates[:, ::-1]
    second = system()._coordinates
    result = _rust.get_vectors(first, second, None, True, False, 1)
    np.testing.assert_array_equal(result[0], second - first)
    with pytest.raises(ValueError, match="axes"):
        _rust.get_vectors(first, second[:1], None, True, False, 1)


def test_flat_pair_shorthand_and_explicit_center_disambiguation():
    source = system()
    observed = msm.structure.get_vectors(
        source, selection=[0, 1], pairs=True, pbc=False
    )
    assert observed.shape == (3, 1, 3)
    np.testing.assert_allclose(values(observed)[:, 0], [[3.0, 4.0, 0.0]] * 3)
    centers = msm.structure.get_vectors(
        source,
        selection=[[0, 1], [2]],
        center_of_atoms=True,
        pairs=True,
        structure_indices=[0],
        structure_indices_2=[1],
        pbc=False,
    )
    np.testing.assert_allclose(values(centers)[0], [[1.0, 2.0, 0.0], [1.0, 2.0, 1.0]])
