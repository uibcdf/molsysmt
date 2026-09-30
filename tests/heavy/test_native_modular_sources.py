"""Checking projected native and modular-file sources without full conversion."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.execution import ChunkedExecutor, Reducer
from molsysmt.native import MolSys, Structures


class _Collector(Reducer):
    def initialize(self, metadata):
        self.chunks = []

    def consume(self, chunk):
        self.chunks.append({
            name: None if array is None else array.copy()
            for name, array in chunk.items()
        })

    def finalize(self):
        return self.chunks


def _structures():
    return Structures(
        coordinates=puw.quantity(np.arange(6 * 4 * 3).reshape(6, 4, 3), "angstrom"),
        box=puw.quantity(np.tile(np.eye(3) * 30, (6, 1, 1)), "angstrom"),
        time=puw.quantity(np.arange(6), "ns"),
        structure_id=np.array([f"source-{100 + i}" for i in range(6)]),
    )


@pytest.mark.parametrize("form", ["molsysmt.Structures", "molsysmt.MolSys", "file:h5msm"])
@pytest.mark.parametrize("mode", ["force", "off"])
def test_selected_projected_sources_preserve_axes_and_units(form, mode, tmp_path, monkeypatch):
    structures = _structures()
    selected = np.array([4, 1, 4, 0, 3], dtype=np.int64)
    atoms = np.array([3, 0], dtype=np.int64)
    if form == "file:h5msm":
        source = str(tmp_path / "structures.h5msm")
        msm.convert(structures, to_form=source)
        from molsysmt.form import _h5msm05_modular

        def forbidden(*args, **kwargs):
            raise AssertionError("Iteration must not load whole modular domains.")

        monkeypatch.setattr(_h5msm05_modular, "read_molsys_file", forbidden)
        monkeypatch.setattr(_h5msm05_modular, "read_modular_file", forbidden)
    elif form == "molsysmt.MolSys":
        source = MolSys._from_partial_domains(structures=structures)

        def forbidden(*args, **kwargs):
            raise AssertionError("Iteration must not extract or copy the full source.")

        monkeypatch.setattr(Structures, "extract", forbidden)
    else:
        source = structures
    with msm.configure.context(chunk_memory_fraction=None):
        chunks = ChunkedExecutor(
            source, form, "projected_test", reducer=_Collector(),
            atom_indices=atoms, structure_indices=selected, chunk_size=2,
            heavy_mode=mode, attributes=["coordinates", "box"],
        ).execute()
    xyz = np.concatenate([chunk["coordinates"] for chunk in chunks])
    reference = puw.get_value(structures.coordinates, to_unit="nm")[np.ix_(selected, atoms)]
    np.testing.assert_allclose(xyz, reference)
    np.testing.assert_allclose(
        np.concatenate([chunk["box"] for chunk in chunks]),
        np.tile(np.eye(3) * 3, (5, 1, 1)),
    )
    np.testing.assert_array_equal(
        np.concatenate([chunk["structure_indices"] for chunk in chunks]), selected
    )
    assert [len(chunk["structure_indices"]) for chunk in chunks] == (
        [2, 2, 1] if mode == "force" else [5]
    )


def test_native_coordinate_getter_copies_only_the_projection(monkeypatch):
    from molsysmt.form.molsysmt_Structures import get_structural_attributes as getters

    shapes = []
    original = getters.copy

    def observed(value):
        shapes.append(puw.get_value(value).shape)
        return original(value)

    monkeypatch.setattr(getters, "copy", observed)
    structures = _structures()
    selected = msm.get(structures, selection=[3, 0], structure_indices=[4, 1], coordinates=True)
    assert shapes == [(2, 2, 3)]
    selected[0, 0, 0] = puw.quantity(999, "nm")
    assert puw.get_value(structures.coordinates, to_unit="nm")[4, 3, 0] != 999


def test_modular_iterator_projects_labels_time_and_closes_on_early_exit(tmp_path):
    from molsysmt.form.file_h5msm.iterators import StructuresIterator

    source = str(tmp_path / "labels.h5msm")
    msm.convert(_structures(), to_form=source)
    iterator = StructuresIterator(
        source, atom_indices=[3, 0], structure_indices=[4, 1, 4, 0],
        chunk=2, output_type="dictionary", coordinates=True,
        structure_id=True, time=True,
    )
    with iterator:
        block = next(iterator)
        assert block["structure_id"].tolist() == ["source-104", "source-101"]
        np.testing.assert_allclose(puw.get_value(block["time"], to_unit="ps"), [4000, 1000])
        assert block["coordinates"].shape == (2, 2, 3)
        assert iterator._inner._file.id.valid
    assert not iterator._inner._file.id.valid


def test_modular_iterator_closes_owned_handle_when_consumer_fails(tmp_path):
    from molsysmt.form.file_h5msm.iterators import StructuresIterator

    source = str(tmp_path / "failed.h5msm")
    msm.convert(_structures(), to_form=source)
    iterator = StructuresIterator(source, chunk=1, coordinates=True)
    with pytest.raises(RuntimeError, match="consumer failed"):
        with iterator:
            next(iterator)
            raise RuntimeError("consumer failed")
    assert not iterator._inner._file.id.valid


@pytest.mark.parametrize("operation", ["get_center", "get_rmsd", "get_distances"])
def test_public_reducers_preserve_quantities_under_nondefault_units(operation):
    puw.configure.set_standard_units([
        "angstrom", "ns", "K", "mole", "dalton", "e", "kJ/mol",
        "kJ/(mol*nm)", "kJ/(mol*nm**2)", "radians",
    ])
    molsys = MolSys._from_partial_domains(structures=_structures())
    function = getattr(msm.structure, operation)
    options = dict(selection=[0, 3], structure_indices=[4, 1, 4])
    if operation == "get_distances":
        options["pbc"] = True
    with msm.configure.context(chunk_memory_fraction=None, chunk_size=2):
        eager = function(molsys, heavy_mode="off", **options)
        chunked = function(molsys, heavy_mode="force", **options)
    eager_values = puw.get_value(eager, to_unit="nm")
    chunked_values = puw.get_value(chunked, to_unit="nm")
    assert eager_values.shape == chunked_values.shape
    np.testing.assert_allclose(chunked_values, eager_values, atol=1e-12)


@pytest.mark.parametrize("fault", ["unit", "shape", "schema"])
def test_modular_iterator_rejects_invalid_series_metadata(tmp_path, fault):
    import h5py

    source = str(tmp_path / "invalid.h5msm")
    msm.convert(_structures(), to_form=source)
    with h5py.File(source, "r+") as file:
        if fault == "unit":
            file["structures/coordinates"].attrs["unit"] = "angstrom"
        elif fault == "shape":
            file["structures"].attrs["n_atoms"] = 5
        else:
            file["structures"].attrs["schema_version"] = 9
    with pytest.raises(ValueError):
        ChunkedExecutor(
            source, "file:h5msm", "invalid_file_test", reducer=_Collector(),
            heavy_mode="force",
        ).execute()
