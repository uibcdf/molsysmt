"""Verify GRO provider selections against literal coordinate and box populations."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from tests.conversion_truth.test_declared_gro_edges import GRO_TEXT
from tests.conversion_truth.test_declared_native_edges import _execute_direct

FIRST = np.array([[0.1, 0.2, 0.3], [0.195, 0.2, 0.3], [0.076, 0.292, 0.3]])
FIRST_BOX = np.array([[2, 0, 0], [0.3, 3, 0], [0.5, 0.6, 4]])
SECOND = (
    "Local water t= 7.5\n"
    "    3\n"
    "    7HOH      O   17   0.400   0.500   0.600\n"
    "    7HOH     H1    3   0.495   0.500   0.600\n"
    "    7HOH     H2   45   0.376   0.592   0.600\n"
    "   5.00000   6.00000   7.00000   0.00000   0.00000   0.20000   0.00000   0.40000   0.70000\n"
)
XYZ = np.stack([FIRST, FIRST + [0.3, 0.3, 0.3]])
BOX = np.stack([FIRST_BOX, [[5, 0, 0], [0.2, 6, 0], [0.4, 0.7, 7]]])


@pytest.mark.parametrize("route", ["direct", "public"])
@pytest.mark.parametrize("form", ["openmm.GromacsGroFile", "mdtraj.GroTrajectoryFile"])
@pytest.mark.parametrize("target", ["molsysmt.MolSys", "molsysmt.Structures"])
@pytest.mark.parametrize("selection", [[2, 0], [1]])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_provider_coordinates_boxes_and_source_cursor(
    route, form, target, selection, unit, tmp_path
):
    path = tmp_path / "source.gro"
    text = GRO_TEXT + SECOND
    path.write_text(text)
    if form == "openmm.GromacsGroFile":
        app = pytest.importorskip("openmm.app")
        source = app.GromacsGroFile(str(path))
        snapshot = [
            np.asarray(puw.get_value(source.getPositions(frame=i), to_unit="nm")).copy()
            for i in range(2)
        ]
        cursor = None
    else:
        formats = pytest.importorskip("mdtraj.formats")
        source = formats.GroTrajectoryFile(str(path))
        source.read(n_frames=1)
        cursor = source._frame_index
    try:
        with puw.context(standard_units=[unit, "ps", "radians"]):
            out = (
                _execute_direct(
                    form,
                    target,
                    source,
                    atom_indices=selection,
                    structure_indices=[1, 0, 1],
                )
                if route == "direct"
                else msm.convert(
                    source,
                    to_form=target,
                    selection=selection,
                    structure_indices=[1, 0, 1],
                )
            )
            structures = out.structures if target == "molsysmt.MolSys" else out
            atom_order = (
                np.sort(selection)
                if form == "openmm.GromacsGroFile" and target == "molsysmt.MolSys"
                else selection
            )
            np.testing.assert_allclose(
                puw.get_value(structures.coordinates, to_unit="nm"),
                XYZ[[1, 0, 1]][:, atom_order],
                atol=1e-7,
            )
            np.testing.assert_allclose(
                puw.get_value(structures.box, to_unit="nm"), BOX[[1, 0, 1]], atol=1e-7
            )
            if form == "openmm.GromacsGroFile" and target == "molsysmt.MolSys":
                assert (
                    out.topology.atoms.atom_name.tolist()
                    == np.array(["O", "H1", "H2"])[atom_order].tolist()
                )
                assert out.topology.groups.group_id.tolist() == ["7"]
            if form == "mdtraj.GroTrajectoryFile":
                np.testing.assert_allclose(
                    puw.get_value(structures.time, to_unit="ps"), [7.5, 2.5, 7.5]
                )
                assert source._frame_index == cursor
                assert source._file.read() == SECOND
                assert not source._file.closed
            else:
                for i in range(2):
                    np.testing.assert_array_equal(
                        puw.get_value(source.getPositions(frame=i), to_unit="nm"),
                        snapshot[i],
                    )
            assert path.read_text() == text
    finally:
        if form == "mdtraj.GroTrajectoryFile":
            source.close()


def test_mdt_gro_public_attribute_queries_keep_source_iteration(tmp_path):
    formats = pytest.importorskip("mdtraj.formats")
    path = tmp_path / "source.gro"
    path.write_text(GRO_TEXT + SECOND)
    with formats.GroTrajectoryFile(str(path)) as source:
        source.read(n_frames=1)
        names = [atom.name for atom in source.topology.atoms]
        n_atoms, n_structures = msm.get(source, n_atoms=True, n_structures=True)
        assert (n_atoms, n_structures) == (3, 2)
        coords, boxes, times = msm.get(source, coordinates=True, box=True, time=True)
        np.testing.assert_allclose(puw.get_value(coords, to_unit="nm"), XYZ, atol=1e-7)
        np.testing.assert_allclose(puw.get_value(boxes, to_unit="nm"), BOX, atol=1e-7)
        np.testing.assert_allclose(puw.get_value(times, to_unit="ps"), [2.5, 7.5])
        assert [atom.name for atom in source.topology.atoms] == names
        assert source._file.read() == SECOND


@pytest.mark.parametrize("failure", [RuntimeError, KeyboardInterrupt])
def test_mdt_gro_closes_independent_readers_on_failure(failure, monkeypatch, tmp_path):
    formats = pytest.importorskip("mdtraj.formats")
    path = tmp_path / "source.gro"
    path.write_text(GRO_TEXT + SECOND)
    with formats.GroTrajectoryFile(str(path)) as source:
        source.read(n_frames=1)
        created = []
        initialize = formats.GroTrajectoryFile.__init__

        def observe(reader, *args, **kwargs):
            initialize(reader, *args, **kwargs)
            created.append(reader)

        def fail(reader, *args, **kwargs):
            raise failure("independent GRO reader interrupted")

        monkeypatch.setattr(formats.GroTrajectoryFile, "__init__", observe)
        monkeypatch.setattr(formats.GroTrajectoryFile, "read", fail)
        with pytest.raises(failure, match="independent GRO reader interrupted"):
            msm.get(source, coordinates=True)
        assert created and all(reader._file.closed for reader in created)
        assert not source._file.closed
        assert source._file.read() == SECOND
        assert path.read_text() == GRO_TEXT + SECOND
