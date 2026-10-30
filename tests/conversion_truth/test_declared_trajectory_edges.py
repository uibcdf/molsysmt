"""Execute DCD/XTC bridges using provider-written literals and owned resources."""

from contextlib import contextmanager
from pathlib import Path

import h5py
import numpy as np
import pytest

import molsysmt as msm
from devtools.scripts.audit_conversion_execution import (
    declared_edges,
    planned_edges,
    read_plan,
)
from tests.conversion_truth.test_declared_native_edges import (
    TRAJECTORY_FORMS,
    _execute_direct,
)

EDGES = sorted(
    (s, t)
    for s, t in planned_edges(declared_edges(), read_plan())
    if {s, t} & TRAJECTORY_FORMS
)


def payload():
    """Independent three-structure coordinates and varying triclinic cells in nm."""
    xyz = np.arange(36, dtype=np.float32).reshape(3, 4, 3) / 100
    box = np.array(
        [[[2 + k, 0, 0], [0.2, 3 + k, 0], [0.1, 0.3, 4 + k]] for k in range(3)]
    )
    return xyz, box, np.array([1.25, 4.5, 8.75], dtype=np.float32)


def write_source(filename):
    md = pytest.importorskip("mdtraj")
    xyz, box, time = payload()
    if filename.suffix == ".xtc":
        with md.formats.XTCTrajectoryFile(str(filename), "w") as writer:
            writer.write(xyz, time=time, step=np.array([11, 27, 55]), box=box)
    else:
        # DCD's provider boundary uses angstroms and degrees, unlike XTC.
        # Form the source cell without the MolSysMT forward/inverse box tools:
        # a paired error in those tools must not cancel inside this oracle.
        lengths = np.linalg.norm(box, axis=2)
        cosine = np.stack(
            [
                np.sum(box[:, first] * box[:, second], axis=1)
                / (lengths[:, first] * lengths[:, second])
                for first, second in [(1, 2), (0, 2), (0, 1)]
            ],
            axis=1,
        )
        angles = np.rad2deg(np.arccos(cosine))
        with md.formats.DCDTrajectoryFile(str(filename), "w") as writer:
            writer.write(xyz * 10, lengths * 10, angles)


@contextmanager
def source(form, directory):
    md = pytest.importorskip("mdtraj")
    directory.mkdir()
    if form == "mdtraj.Trajectory":
        topology = md.Topology()
        group = topology.add_residue("LIG", topology.add_chain())
        for index in range(4):
            topology.add_atom(f"C{index}", md.element.carbon, group)
        xyz, box, time = payload()
        item = md.Trajectory(xyz, topology, time=time)
        item.unitcell_vectors = box
        yield item
        return
    extension = "dcd" if "dcd" in form.lower() else "xtc"
    filename = directory / f"source.{extension}"
    write_source(filename)
    original = filename.read_bytes()
    if form.startswith("file:"):
        yield str(filename)
    else:
        cls = getattr(md.formats, extension.upper() + "TrajectoryFile")
        with cls(str(filename), "r") as item:
            item.seek(1)
            yield item
            assert item.tell() == 1
    assert filename.read_bytes() == original


@pytest.mark.parametrize(
    "source_form,target", EDGES, ids=[f"{s}->{t}" for s, t in EDGES]
)
def test_declared_trajectory_edge_executes_directly_and_publicly(
    source_form, target, tmp_path
):
    pytest.importorskip("mdtraj")
    for route in ("direct", "public"):
        with source(source_form, tmp_path / route) as item:
            assert msm.get_form(item) == source_form
            kwargs = (
                {"output_filename": str(tmp_path / f"{route}.{target.split(':')[-1]}")}
                if target.startswith("file:")
                else {}
            )
            result = (
                _execute_direct(source_form, target, item, **kwargs)
                if route == "direct"
                else msm.convert(item, to_form=target, **kwargs)
            )
            assert msm.get_form(result) == target
            if target == "file:h5msm":
                with h5py.File(result, "r") as file:
                    assert file.attrs["version"] == (
                        "0.5" if route == "public" else "0.4"
                    )
            elif target in {"file:dcd", "file:xtc"} and source_form.startswith("file:"):
                assert Path(result).read_bytes() == Path(item).read_bytes()


@pytest.mark.parametrize("source_form", sorted(TRAJECTORY_FORMS))
@pytest.mark.parametrize("unit", ["nm", "angstrom"])
def test_trajectory_selection_preserves_literal_values_units_and_reader(
    source_form, unit, tmp_path
):
    puw = msm.pyunitwizard
    xyz, box, time = payload()
    atoms, structures = [3, 1], [2, 0, 2]
    with source(source_form, tmp_path / "source") as item:
        with puw.context(standard_units=[unit, "ps", "radians"]):
            result = msm.convert(
                item,
                to_form="molsysmt.Structures",
                selection=atoms,
                structure_indices=structures,
            )
        np.testing.assert_allclose(
            puw.get_value(result.coordinates, to_unit="nm"),
            xyz[np.ix_(structures, atoms, [0, 1, 2])],
            atol=1e-6,
        )
        np.testing.assert_allclose(
            puw.get_value(result.box, to_unit="nm"), box[structures], atol=3e-6
        )
        assert result.structure_id.tolist() == (
            [55, 11, 55] if "xtc" in source_form.lower() else structures
        )
        if "xtc" in source_form.lower():
            np.testing.assert_allclose(
                puw.get_value(result.time, to_unit="ps"), time[structures]
            )


@pytest.mark.parametrize("extension", ["dcd", "xtc"])
def test_trajectory_identity_uses_owned_copy_and_rejects_source_alias(
    extension, tmp_path
):
    from molsysmt._private.smonitor import ArgumentError

    filename = tmp_path / f"input.{extension}"
    write_source(filename)
    original = filename.read_bytes()
    result = msm.convert(str(filename), to_form=f"file:{extension}")
    assert Path(result) != filename
    assert Path(result).read_bytes() == original
    assert msm.convert(
        str(filename), to_form=f"file:{extension}", copy_if_all=False
    ) == str(filename)
    with pytest.raises(ArgumentError, match="output_filename"):
        msm.convert(str(filename), to_form=str(filename))
    assert filename.read_bytes() == original


@pytest.mark.parametrize("extension", ["dcd", "xtc"])
@pytest.mark.parametrize("operation", ["convert", "extract"])
def test_subset_file_serialization_refuses_before_writing(
    extension, operation, tmp_path
):
    from molsysmt._private.smonitor import NotImplementedMethodError

    filename = tmp_path / f"input.{extension}"
    write_source(filename)
    original = filename.read_bytes()
    target = tmp_path / f"target.{extension}"
    target.write_bytes(b"caller-owned destination")
    kwargs = (
        {"to_form": str(target)}
        if operation == "convert"
        else {"output_filename": str(target)}
    )
    with pytest.raises(NotImplementedMethodError, match="Subset file serialization"):
        getattr(msm, operation)(
            str(filename), selection=[3, 1], structure_indices=[2, 0], **kwargs
        )
    assert filename.read_bytes() == original
    assert target.read_bytes() == b"caller-owned destination"


@pytest.mark.parametrize("extension", ["dcd", "xtc"])
@pytest.mark.parametrize("route", ["direct", "public"])
def test_selected_trajectory_h5msm_retains_explicit_unit_payload(
    extension, route, tmp_path
):
    puw = msm.pyunitwizard
    filename = tmp_path / f"input.{extension}"
    write_source(filename)
    xyz, box, time = payload()
    destination = tmp_path / "selection.h5msm"
    with puw.context(
        standard_units=[
            "angstrom" if unit == "nm" else unit
            for unit in puw.configure.get_standard_units()
        ]
    ):
        if route == "direct":
            _execute_direct(
                f"file:{extension}",
                "file:h5msm",
                str(filename),
                atom_indices=[3, 1],
                structure_indices=[2, 0, 2],
                output_filename=str(destination),
            )
        else:
            msm.convert(
                str(filename),
                to_form=destination,
                selection=[3, 1],
                structure_indices=[2, 0, 2],
            )
        restored = msm.get(destination, coordinates=True, box=True)
    np.testing.assert_allclose(
        puw.get_value(restored[0], to_unit="nm"),
        xyz[np.ix_([2, 0, 2], [3, 1], [0, 1, 2])],
        atol=1e-6,
    )
    np.testing.assert_allclose(
        puw.get_value(restored[1], to_unit="nm"), box[[2, 0, 2]], atol=3e-6
    )
    if extension == "xtc":
        np.testing.assert_allclose(
            puw.get_value(msm.get(destination, time=True), to_unit="ps"),
            time[[2, 0, 2]],
        )


@pytest.mark.parametrize("extension", ["dcd", "xtc"])
@pytest.mark.parametrize("route", ["public", "positional"])
def test_legacy_destination_alias_and_conflict_keep_source_intact(
    extension, route, tmp_path
):
    from molsysmt._private.smonitor import ArgumentConflictError

    filename = tmp_path / f"input.{extension}"
    write_source(filename)
    destination = tmp_path / f"legacy.{extension}"
    original = filename.read_bytes()
    if route == "public":
        result = msm.convert(
            str(filename), to_form=f"file:{extension}", output_name=str(destination)
        )
    else:
        from molsysmt.form import _dict_modules, load_converter

        module = _dict_modules[f"file:{extension}"]
        converter = load_converter(module, module._convert_to[f"file:{extension}"])
        result = converter(str(filename), "all", "all", str(destination), True, False)
    assert Path(result).read_bytes() == original
    with pytest.raises(ArgumentConflictError):
        msm.convert(
            str(filename),
            to_form=f"file:{extension}",
            output_name=str(destination),
            output_filename=str(filename),
        )
    assert filename.read_bytes() == original
    assert destination.read_bytes() == original


@pytest.mark.parametrize("extension", ["dcd", "xtc"])
def test_selected_codec_reads_one_structure_at_a_time_and_restores_position(
    extension, tmp_path
):
    from importlib import import_module

    md = pytest.importorskip("mdtraj")
    path = tmp_path / f"selected.{extension}"
    write_source(path)
    reader_type = getattr(md.formats, extension.upper() + "TrajectoryFile")
    module = import_module(
        f"molsysmt.form.mdtraj_{extension.upper()}TrajectoryFile.to_molsysmt_Structures"
    )
    convert = module.to_molsysmt_Structures

    class ObservedReader:
        def __init__(self, handle):
            self.handle = handle
            self.reads = []

        def read(self, *args, **kwargs):
            count = args[0] if args else kwargs.get("n_frames")
            self.reads.append((self.tell(), count))
            assert count == 1, (
                "A selected conversion must not bulk-read the trajectory."
            )
            return self.handle.read(*args, **kwargs)

        def seek(self, *args):
            return self.handle.seek(*args)

        def tell(self):
            return self.handle.tell()

        def __len__(self):
            return len(self.handle)

    with reader_type(str(path), "r") as handle:
        handle.seek(1)
        observed = ObservedReader(handle)
        result = convert(
            observed,
            atom_indices=[3, 1],
            structure_indices=[2, 0, 2],
            skip_digestion=True,
        )
        assert observed.reads == [(2, 1), (0, 1), (2, 1)]
        assert handle.tell() == 1
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result.coordinates, to_unit="nm"),
        payload()[0][[2, 0, 2]][:, [3, 1]],
        atol=2e-6,
        rtol=0,
    )
