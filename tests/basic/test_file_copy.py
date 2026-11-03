"""Protect explicit file-copy destinations and resident-copy independence."""

import hashlib
import os
from pathlib import Path

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt.native import MolSys, Structures


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).digest()


@pytest.fixture
def h5msm(tmp_path):
    molsys = MolSys(n_atoms=3)
    molsys.chemical_states.add_bonds([[0, 1]])
    molsys.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.arange(18.0).reshape(2, 3, 3), "nm")
    )
    analysis = msm.Interactions.from_records(
        [
            {
                "structure_index": 0,
                "interaction_type": "hbond",
                "participants": [
                    {"role": "donor", "atom_indices": [0]},
                    {"role": "hydrogen", "atom_indices": [1]},
                    {"role": "acceptor", "atom_indices": [2]},
                ],
                "measurements": {"distance": 0.2},
                "evidence": "synthetic",
            }
        ],
        n_atoms=3,
        n_structures=2,
        evaluated_structure_indices=[0, 1],
        method="synthetic_copy_guard",
        measure_units={"distance": "nm"},
    )
    molsys.interactions = {"test": analysis}
    path = tmp_path / "source.h5msm"
    msm.convert(molsys, to_form=path)
    return path


@pytest.mark.parametrize("direct", [False, True])
def test_missing_destination_creates_a_session_copy_without_touching_source(
    h5msm, direct
):
    from molsysmt.form.file_h5msm.copy import copy as direct_copy

    before = digest(h5msm)
    output = (direct_copy if direct else msm.copy)(str(h5msm))
    assert isinstance(output, str)
    assert msm.get_form(output) == "file:h5msm"
    assert not os.path.samefile(h5msm, output)
    assert Path(output).suffix == h5msm.suffix
    assert digest(output) == before
    import gc

    gc.collect()
    assert Path(str(output)).is_file()
    assert digest(h5msm) == before
    assert list(h5msm.parent.iterdir()) == [h5msm]


@pytest.mark.parametrize("alias", ["literal", "relative", "symlink", "hardlink"])
@pytest.mark.parametrize("direct", [False, True])
def test_source_aliases_reject_before_writing(
    h5msm, tmp_path, alias, direct, monkeypatch
):
    from molsysmt.form.file_h5msm.copy import copy as direct_copy

    target = h5msm
    if alias == "relative":
        monkeypatch.chdir(tmp_path)
        target = Path(".") / h5msm.name
    elif alias in {"symlink", "hardlink"}:
        target = tmp_path / f"{alias}.h5msm"
        try:
            (os.symlink if alias == "symlink" else os.link)(h5msm, target)
        except (OSError, NotImplementedError) as error:
            pytest.skip(f"Filesystem does not support {alias}: {error}")
    before = digest(h5msm)
    with pytest.raises(ArgumentError, match="output_filename"):
        (direct_copy if direct else msm.copy)(str(h5msm), output_filename=str(target))
    assert digest(h5msm) == before
    assert digest(target) == before


@pytest.mark.parametrize("direct", [False, True])
def test_directory_is_not_an_output_filename(h5msm, tmp_path, direct):
    from molsysmt.form.file_h5msm.copy import copy as direct_copy

    directory = tmp_path / "copies"
    directory.mkdir()
    before = digest(h5msm)
    with pytest.raises(ArgumentError, match="output_filename"):
        (direct_copy if direct else msm.copy)(
            str(h5msm), output_filename=str(directory)
        )
    assert list(directory.iterdir()) == []
    assert digest(h5msm) == before


@pytest.mark.parametrize("direct", [False, True])
@pytest.mark.parametrize("legacy", [False, True])
def test_explicit_copy_preserves_file_bytes_without_conversion(
    h5msm, tmp_path, direct, legacy, monkeypatch
):
    from molsysmt.form.file_h5msm.copy import copy as direct_copy

    source = (
        Path(msm.systems["pentalanine"]["traj_pentalanine.h5msm"]) if legacy else h5msm
    )
    target = tmp_path / "copied.h5msm"
    before = digest(source)

    def forbidden(*args, **kwargs):
        pytest.fail("A raw file copy must not convert the molecular system")

    monkeypatch.setattr(msm.basic, "convert", forbidden)
    result = (direct_copy if direct else msm.copy)(
        str(source), output_filename=str(target)
    )
    assert result == str(target)
    assert digest(target) == before == digest(source)
    assert not os.path.samefile(source, target)
    with h5py.File(target, "r+") as file:
        file.attrs["copy_independence_probe"] = "destination only"
    assert digest(source) == before


def test_copy_retains_chemical_states_and_named_interactions(h5msm, tmp_path):
    target = tmp_path / "domains.h5msm"
    msm.copy(h5msm, output_filename=target)
    molsys = msm.convert(target)
    np.testing.assert_array_equal(molsys.chemical_states.get_bonds(), [[0, 1]])
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(molsys.structures.coordinates, to_unit="nm"),
        np.arange(18.0).reshape(2, 3, 3),
    )
    assert list(molsys.interactions) == ["test"]
    selected = molsys.interactions["test"].query(structure_indices=[1, 0]).to_dict()
    np.testing.assert_array_equal(selected["occurrence_indices"], [0])
    np.testing.assert_array_equal(selected["evaluated_structure_indices"], [1, 0])


@pytest.mark.parametrize("destination", ["one_destination.h5msm"])
def test_composite_file_copy_rejects_one_or_missing_destinations_before_resident_copy(
    h5msm, destination, monkeypatch, tmp_path
):
    from molsysmt.form import _dict_modules
    from molsysmt.native import Topology

    def forbidden(*args, **kwargs):
        pytest.fail("A composite destination error must precede resident copying")

    structures = msm.convert(h5msm).structures
    coordinate_file = tmp_path / "coordinates.h5msm"
    msm.h5msm.write_layers(str(coordinate_file), structures=structures)
    monkeypatch.setattr(_dict_modules["molsysmt.Topology"], "copy", forbidden)
    with pytest.raises(ArgumentError, match="output_filename"):
        msm.copy(
            [Topology(n_atoms=3), str(coordinate_file)], output_filename=destination
        )


def test_resident_composite_copy_stays_independent():
    from molsysmt.native import Topology

    topology = Topology(n_atoms=3)
    structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((1, 3, 3)), "nm")
    )
    copies = msm.copy([topology, structures])
    assert copies[0] is not topology
    assert copies[1] is not structures
    assert not np.shares_memory(
        msm.pyunitwizard.get_value(copies[1].coordinates),
        msm.pyunitwizard.get_value(structures.coordinates),
    )


def test_filesystem_path_protocol_is_supported_for_source_and_destination(
    h5msm, tmp_path
):
    class FilePath(os.PathLike):
        def __init__(self, path):
            self.path = path

        def __fspath__(self):
            return str(self.path)

    destination = tmp_path / "path_protocol.h5msm"
    result = msm.copy(FilePath(h5msm), output_filename=FilePath(destination))
    assert result == str(destination)
    assert digest(result) == digest(h5msm)


def test_composite_without_destination_copies_each_member(h5msm, tmp_path):
    from molsysmt.native import Topology

    coordinates = tmp_path / "coordinates.h5msm"
    msm.h5msm.write_layers(str(coordinates), structures=msm.convert(h5msm).structures)
    topology = Topology(n_atoms=3)
    result = msm.copy([topology, str(coordinates)])
    assert result[0] is not topology
    assert not os.path.samefile(result[1], coordinates)
    assert digest(result[1]) == digest(coordinates)
