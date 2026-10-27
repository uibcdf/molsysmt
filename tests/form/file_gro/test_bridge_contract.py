"""Protect GRO OpenMM bridges and independent reader copies with literal oracles."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from tests.conversion_truth.test_declared_gro_edges import GRO_TEXT
from tests.conversion_truth.test_declared_native_edges import _execute_direct

BOX = np.array([[2, 0, 0], [0.3, 3, 0], [0.5, 0.6, 4]])
XYZ = np.array([[0.1, 0.2, 0.3], [0.195, 0.2, 0.3], [0.076, 0.292, 0.3]])


@pytest.mark.parametrize("route", ["direct", "public"])
@pytest.mark.parametrize("target", ["openmm.Topology", "openmm.Modeller"])
@pytest.mark.parametrize("selection", [[2, 0], [1], [0, 1, 2]])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_file_gro_openmm_selected_values_and_labels(
    route, target, selection, unit, tmp_path
):
    pytest.importorskip("openmm")
    path = tmp_path / "source.gro"
    path.write_text(GRO_TEXT)
    expected = np.sort(selection)
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = (
            _execute_direct("file:gro", target, str(path), atom_indices=selection)
            if route == "direct"
            else msm.convert(path, to_form=target, selection=selection)
        )
    topology = result.topology if target == "openmm.Modeller" else result
    assert [a.name for a in topology.atoms()] == np.array(["O", "H1", "H2"])[
        expected
    ].tolist()
    assert [a.id for a in topology.atoms()] == np.array(["17", "3", "45"])[
        expected
    ].tolist()
    assert [(g.name, g.id) for g in topology.residues()] == [("HOH", "7")]
    actual_bonds = {tuple(sorted((a.index, b.index))) for a, b in topology.bonds()}
    inverse = {int(atom): i for i, atom in enumerate(expected)}
    expected_bonds = {
        tuple(sorted((inverse[a], inverse[b])))
        for a, b in [(0, 1), (0, 2)]
        if a in inverse and b in inverse
    }
    assert actual_bonds == expected_bonds
    np.testing.assert_allclose(
        puw.get_value(topology.getPeriodicBoxVectors(), to_unit="nm"), BOX
    )
    if target == "openmm.Modeller":
        np.testing.assert_allclose(
            puw.get_value(result.positions, to_unit="nm"), XYZ[expected]
        )
    assert path.read_text() == GRO_TEXT


@pytest.mark.parametrize(
    "form", ["molsysmt.GROFileHandler", "mdtraj.GroTrajectoryFile"]
)
@pytest.mark.parametrize("operation", ["convert", "copy", "extract"])
def test_reader_copy_has_independent_ownership_and_preserves_cursor(
    form, operation, tmp_path
):
    path = tmp_path / "source.gro"
    path.write_text(GRO_TEXT)
    if form == "molsysmt.GROFileHandler":
        from molsysmt.native import GROFileHandler

        source = GROFileHandler(path)
        stream = source.file
    else:
        formats = pytest.importorskip("mdtraj.formats")
        source = formats.GroTrajectoryFile(str(path))
        source.read(n_frames=1)
        stream = source._file
    position = stream.tell() if form == "molsysmt.GROFileHandler" else None
    result = None
    try:
        result = (
            msm.convert(source, to_form=form)
            if operation == "convert"
            else msm.copy(source)
            if operation == "copy"
            else msm.extract(source)
        )
        assert result is not source
        copy_stream = result.file if form == "molsysmt.GROFileHandler" else result._file
        assert copy_stream is not stream and not copy_stream.closed
        if form == "molsysmt.GROFileHandler":
            assert copy_stream.tell() == position == stream.tell()
            assert not np.shares_memory(
                puw.get_value(result.entry.coordinates),
                puw.get_value(source.entry.coordinates),
            )
            result.entry.atom_names[0] = "changed"
            assert source.entry.atom_names.tolist() == ["O", "H1", "H2"]
            assert copy_stream.getvalue() == stream.getvalue() == GRO_TEXT
        else:
            assert result.topology is not source.topology
            assert copy_stream.read() == GRO_TEXT
            result.topology.atom(0).name = "changed"
            assert source.topology.atom(0).name == "O"
        result.close()
        assert not stream.closed
        if form == "molsysmt.GROFileHandler":
            assert stream.tell() == position
        else:
            assert stream.read() == ""
        assert path.read_text() == GRO_TEXT
    finally:
        if result is not None:
            result.close()
        source.close()


@pytest.mark.parametrize("route", ["direct", "public"])
def test_native_handler_identity_can_explicitly_alias(route, tmp_path):
    path = tmp_path / "source.gro"
    path.write_text(GRO_TEXT)
    from molsysmt.native import GROFileHandler

    source = GROFileHandler(path)
    try:
        result = (
            _execute_direct(
                "molsysmt.GROFileHandler",
                "molsysmt.GROFileHandler",
                source,
                copy_if_all=False,
            )
            if route == "direct"
            else msm.convert(
                source, to_form="molsysmt.GROFileHandler", copy_if_all=False
            )
        )
        assert result is source and not source.file.closed
    finally:
        source.close()


@pytest.mark.parametrize(
    "form", ["molsysmt.GROFileHandler", "mdtraj.GroTrajectoryFile"]
)
def test_unsupported_handler_subset_does_not_change_source(form, tmp_path):
    from molsysmt._private.smonitor import NotImplementedMethodError
    from molsysmt.native import GROFileHandler

    path = tmp_path / "source.gro"
    path.write_text(GRO_TEXT)
    if form == "molsysmt.GROFileHandler":
        source = GROFileHandler(path)
        stream = source.file
        remaining = ""
    else:
        formats = pytest.importorskip("mdtraj.formats")
        source = formats.GroTrajectoryFile(str(path))
        stream = source._file
        remaining = GRO_TEXT
    try:
        with pytest.raises(NotImplementedMethodError):
            msm.extract(source, selection=[0])
        assert not stream.closed
        assert stream.read() == remaining
        assert path.read_text() == GRO_TEXT
    finally:
        source.close()
