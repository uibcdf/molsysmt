"""Build assemblies from the requested structures, preserving positional order."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import Structures
from tests.native.test_molsys import build_minimal_molsys


def _operation(chains):
    return {
        "chain_indices": chains,
        "rotations": [
            np.eye(3),
            np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]),
        ],
        "translations": puw.quantity([[0.0, 0.0, 0.0], [10.0, 20.0, 30.0]], "angstrom"),
    }


@pytest.fixture
def molsys():
    result = build_minimal_molsys(3)
    result.structures = Structures(
        coordinates=result.structures.coordinates,
        time=puw.quantity([5.0, 15.0, 40.0], "ps"),
        structure_id=["label-A", "label-B", "label-C"],
        bioassembly={"1": _operation([0, 1])},
    )
    return result


def _assert_selected_geometry(assembled, indices, atom_indices):
    source = np.arange(36.0).reshape(3, 4, 3)[indices][:, atom_indices]
    rotated = np.stack([-source[:, :, 1], source[:, :, 0], source[:, :, 2]], axis=-1)
    expected = np.concatenate([source, rotated + [1.0, 2.0, 3.0]], axis=1)
    np.testing.assert_allclose(
        puw.get_value(assembled.structures.get_coordinates(), to_unit="nm"),
        expected,
        rtol=0,
        atol=1e-13,
    )
    assert assembled.structures.structure_id.tolist() == [
        ["label-A", "label-B", "label-C"][index] for index in indices
    ]
    np.testing.assert_allclose(
        puw.get_value(assembled.structures.get_time(), to_unit="ps"),
        np.array([5.0, 15.0, 40.0])[indices],
    )
    assert assembled.topology.n_atoms == len(atom_indices) * 2


@pytest.mark.parametrize(
    "chains,atoms",
    [
        pytest.param([0, 1], [0, 1, 2, 3], id="common-chains"),
        pytest.param([[0, 1], [0, 1]], [0, 1, 2, 3], id="repeated-chains"),
        pytest.param([1], [2, 3], id="common-single-chain"),
        pytest.param([[1], [1]], [2, 3], id="repeated-single-chain"),
    ],
)
@pytest.mark.parametrize(
    "selection,indices",
    [(2, [2]), ([2, 0, 2], [2, 0, 2]), ("all", [0, 1, 2])],
)
def test_explicit_structure_selection_preserves_geometry_and_metadata(
    molsys, chains, atoms, selection, indices
):
    with puw.context(standard_units=["angstrom", "ns", "kcal/mol", "K"]):
        assembled = msm.build.make_bioassembly(
            molsys,
            bioassembly=_operation(chains),
            structure_indices=selection,
        )
    _assert_selected_geometry(assembled, indices, atoms)
    np.testing.assert_array_equal(
        puw.get_value(molsys.structures.get_coordinates(), to_unit="nm"),
        np.arange(36.0).reshape(3, 4, 3),
    )


@pytest.mark.parametrize("assembly", [None, "1"])
def test_stored_assembly_preserves_nonconsecutive_structure_selection(molsys, assembly):
    assembled = msm.build.make_bioassembly(
        molsys,
        bioassembly=assembly,
        structure_indices=[2, 0, 2],
    )
    _assert_selected_geometry(assembled, [2, 0, 2], [0, 1, 2, 3])


def test_default_selection_keeps_first_structure(molsys):
    assembled = msm.build.make_bioassembly(molsys)
    _assert_selected_geometry(assembled, [0], [0, 1, 2, 3])


@pytest.mark.parametrize("to_form", [None, "molsysmt.MolSys"])
def test_h5msm_input_keeps_selected_structure_order(molsys, tmp_path, to_form):
    filename = tmp_path / "source.h5msm"
    msm.h5msm.write(molsys, filename)
    original = filename.read_bytes()
    assembled = msm.build.make_bioassembly(
        filename,
        bioassembly="1",
        structure_indices=[2, 0, 2],
        to_form=to_form,
    )
    assert msm.get_form(assembled) == "molsysmt.MolSys"
    _assert_selected_geometry(assembled, [2, 0, 2], [0, 1, 2, 3])
    assert filename.read_bytes() == original


@pytest.mark.parametrize("chains", [[0, 1], [[0, 1], [0, 1]]])
@pytest.mark.parametrize("indices", [[3], [-1]])
def test_invalid_structure_indices_are_not_silently_ignored(molsys, chains, indices):
    with pytest.raises(msm.ArgumentError):
        msm.build.make_bioassembly(
            molsys,
            bioassembly=_operation(chains),
            structure_indices=indices,
        )
