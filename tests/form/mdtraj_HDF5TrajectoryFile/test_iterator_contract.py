"""Keep bounded HDF5 iteration ordered, nullable, unit-aware and cursor-safe."""

import numpy as np
import pytest

from molsysmt import pyunitwizard as puw
from molsysmt.form.mdtraj_HDF5TrajectoryFile.iterators import StructuresIterator


@pytest.mark.parametrize("mode", ["minimal", "complete"])
@pytest.mark.parametrize("length,time", [("nm", "ps"), ("pm", "fs")])
def test_optional_fields_and_nonconsecutive_chunks_are_coherent(
    mdtraj_hdf5_small_files, mdtraj_selection_ensemble, mode, length, time
):
    import mdtraj as md

    with md.formats.HDF5TrajectoryFile(
        str(mdtraj_hdf5_small_files[mode]), "r"
    ) as reader:
        reader.seek(1)
        units = [
            length if u == "nm" else time if u == "ps" else u
            for u in puw.configure.get_standard_units()
        ]
        with puw.context(standard_units=units):
            # Retain copies of the reusable outer attribute dictionary.
            blocks = [
                dict(block)
                for block in StructuresIterator(
                    reader,
                    atom_indices=[3, 1, 1],
                    structure_indices=[2, 0, 2],
                    chunk=2,
                    output_type="dictionary",
                    coordinates=True,
                    box=True,
                    time=True,
                    velocities=True,
                    temperature=True,
                    kinetic_energy=True,
                    potential_energy=True,
                    total_energy=True,
                    structure_index=True,
                )
            ]
            assert reader.tell() == 1
            assert [block["coordinates"].shape for block in blocks] == [
                (2, 3, 3),
                (1, 3, 3),
            ]
            xyz = np.concatenate(
                [puw.get_value(b["coordinates"], to_unit="nm") for b in blocks]
            )
            np.testing.assert_allclose(
                xyz,
                mdtraj_selection_ensemble.xyz[[2, 0, 2]][:, [3, 1, 1]],
                rtol=0,
                atol=1e-6,
            )
            np.testing.assert_array_equal(
                np.concatenate([b["structure_index"] for b in blocks]), [2, 0, 2]
            )
            if mode == "minimal":
                for block in blocks:
                    assert all(
                        block[name] is None
                        for name in [
                            "box",
                            "time",
                            "velocities",
                            "temperature",
                            "kinetic_energy",
                            "potential_energy",
                            "total_energy",
                        ]
                    )
            else:
                for name, unit, expected in [
                    ("time", "ps", [9, 1, 9]),
                    ("temperature", "K", [290, 270, 290]),
                    ("kinetic_energy", "kJ/mol", [3, 1, 3]),
                    ("potential_energy", "kJ/mol", [-30, -10, -30]),
                    ("total_energy", "kJ/mol", [-27, -9, -27]),
                ]:
                    values = np.concatenate(
                        [puw.get_value(b[name], to_unit=unit) for b in blocks]
                    )
                    np.testing.assert_allclose(values, expected, rtol=0, atol=1e-12)
                box = np.concatenate(
                    [puw.get_value(b["box"], to_unit="nm") for b in blocks]
                )
                np.testing.assert_allclose(
                    box,
                    mdtraj_selection_ensemble.unitcell_vectors[[2, 0, 2]],
                    atol=1e-6,
                )
                velocities = np.concatenate(
                    [puw.get_value(b["velocities"], to_unit="nm/ps") for b in blocks]
                )
                np.testing.assert_allclose(
                    velocities,
                    mdtraj_selection_ensemble.xyz[[2, 0, 2]][:, [3, 1, 1]] / 2,
                    rtol=0,
                    atol=1e-6,
                )
                assert str(puw.get_unit(blocks[0]["coordinates"])) == str(
                    puw.unit(length)
                )
                assert str(puw.get_unit(blocks[0]["time"])) == str(puw.unit(time))


@pytest.mark.parametrize("indices,expected", [("all", [0, 1, 2, 3, 4]), ([], [])])
def test_all_and_empty_axes_preserve_the_reader(
    mdtraj_hdf5_small_files, indices, expected
):
    import mdtraj as md

    with md.formats.HDF5TrajectoryFile(
        str(mdtraj_hdf5_small_files["minimal"]), "r"
    ) as reader:
        reader.seek(1)
        blocks = [
            dict(block)
            for block in StructuresIterator(
                reader,
                structure_indices=indices,
                chunk=2,
                output_type="dictionary",
                coordinates=True,
                structure_index=True,
            )
        ]
        actual = [int(i) for b in blocks for i in b["structure_index"]]
        assert actual == expected
        assert reader.tell() == 1


def test_public_iterator_honors_traversal_over_the_explicit_axis(
    mdtraj_hdf5_small_files,
):
    import mdtraj as md

    import molsysmt as msm

    with md.formats.HDF5TrajectoryFile(
        str(mdtraj_hdf5_small_files["complete"]), "r"
    ) as reader:
        reader.seek(1)
        blocks = [
            dict(block)
            for block in msm.Iterator(
                reader,
                selection=[3, 1],
                structure_indices=[4, 1, 3, 0],
                start=1,
                step=2,
                chunk=2,
                output_type="dictionary",
                coordinates=True,
                time=True,
                structure_index=True,
            )
        ]
        assert len(blocks) == 1
        np.testing.assert_array_equal(blocks[0]["structure_index"], [1, 0])
        np.testing.assert_array_equal(
            puw.get_value(blocks[0]["time"], to_unit="ps"), [4, 1]
        )
        assert blocks[0]["coordinates"].shape == (2, 2, 3)
        assert reader.tell() == 1


def test_storage_units_are_decoded_before_application_standardization(
    mdtraj_hdf5_small_files, mdtraj_selection_ensemble
):
    import h5py
    import mdtraj as md

    path = mdtraj_hdf5_small_files["complete"]
    with h5py.File(path, "r+") as handle:
        for name, scale, unit in [
            ("coordinates", 10, "angstroms"),
            ("cell_lengths", 10, "angstroms"),
            ("time", 1000, "femtoseconds"),
        ]:
            handle[name][...] = handle[name][...] * scale
            handle[name].attrs["units"] = unit
    with md.formats.HDF5TrajectoryFile(str(path), "r") as reader:
        # First verify the file is meaningful to the public provider reader.
        provider = reader.read(1)
        np.testing.assert_allclose(
            provider.coordinates, mdtraj_selection_ensemble.xyz[:1], atol=1e-6
        )
        np.testing.assert_array_equal(provider.time, [1])
        reader.seek(2)
        coordinates, time = next(
            StructuresIterator(reader, coordinates=True, time=True)
        )
        np.testing.assert_allclose(
            puw.get_value(coordinates, to_unit="nm"),
            mdtraj_selection_ensemble.xyz[:1],
            atol=1e-6,
        )
        np.testing.assert_array_equal(puw.get_value(time, to_unit="ps"), [1])
        assert reader.tell() == 2


def test_selected_reads_are_bounded_and_cursor_is_restored_on_failure(
    mdtraj_hdf5_small_files, monkeypatch
):
    import mdtraj as md

    with md.formats.HDF5TrajectoryFile(
        str(mdtraj_hdf5_small_files["complete"]), "r"
    ) as reader:
        read = reader.read
        calls = []

        def checked_read(n_frames=None, **kwargs):
            assert n_frames == 1
            calls.append(reader.tell())
            if len(calls) == 3:
                reader.seek(4)
                raise RuntimeError("controlled read failure")
            return read(n_frames=n_frames, **kwargs)

        monkeypatch.setattr(reader, "read", checked_read)
        reader.seek(1)
        iterator = StructuresIterator(
            reader, structure_indices=[4, 0, 3], chunk=2, coordinates=True
        )
        assert next(iterator).shape == (2, 4, 3)
        assert reader.tell() == 1
        with pytest.raises(RuntimeError, match="controlled read failure"):
            next(iterator)
        assert reader.tell() == 1
        assert calls == [4, 0, 3]


def test_inventory_iteration_is_an_explicit_unavailable_route(mdtraj_hdf5_small_files):
    import mdtraj as md

    import molsysmt as msm
    from molsysmt._private.smonitor import NotImplementedIteratorError

    with md.formats.HDF5TrajectoryFile(
        str(mdtraj_hdf5_small_files["complete"]), "r"
    ) as reader:
        reader.seek(1)
        with pytest.raises(
            NotImplementedIteratorError, match="mdtraj.HDF5TrajectoryFile"
        ):
            msm.Iterator(reader, atom_name=True)
        assert reader.tell() == 1
