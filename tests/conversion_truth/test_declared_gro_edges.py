"""Execute declared GRO bridges with literal records and explicit resource owners."""

from contextlib import contextmanager
from pathlib import Path

import pytest

import molsysmt as msm
from devtools.scripts.audit_conversion_execution import (
    declared_edges,
    planned_edges,
    read_plan,
)
from tests.conversion_truth.test_declared_native_edges import GRO_FORMS, _execute_direct

EDGES = sorted(
    (s, t)
    for s, t in planned_edges(declared_edges(), read_plan())
    if {s, t} & GRO_FORMS
)

# Standard fixed-column record, independent of every MolSysMT writer. Positions
# are in nm; the lower triangular box follows the GROMACS row-vector convention.
GRO_TEXT = (
    "Local water t= 2.5\n"
    "    3\n"
    "    7HOH      O   17   0.100   0.200   0.300\n"
    "    7HOH     H1    3   0.195   0.200   0.300\n"
    "    7HOH     H2   45   0.076   0.292   0.300\n"
    "   2.00000   3.00000   4.00000   0.00000   0.00000   0.30000   0.00000   0.50000   0.60000\n"
)


@contextmanager
def source(form, directory):
    directory.mkdir()
    filename = directory / "source.gro"
    filename.write_text(GRO_TEXT)
    item = None
    if form == "file:gro":
        item = str(filename)
    elif form == "molsysmt.GROFileHandler":
        from molsysmt.native import GROFileHandler

        item = GROFileHandler(filename)
    elif form == "openmm.GromacsGroFile":
        app = pytest.importorskip("openmm.app")
        item = app.GromacsGroFile(str(filename))
    elif form == "mdtraj.GroTrajectoryFile":
        formats = pytest.importorskip("mdtraj.formats")
        item = formats.GroTrajectoryFile(str(filename))
    else:
        raise AssertionError(form)
    try:
        yield item
        assert filename.read_text() == GRO_TEXT
        if form == "molsysmt.GROFileHandler":
            assert not item.file.closed
        elif form == "mdtraj.GroTrajectoryFile":
            # MDTraj's public seek() is unimplemented for GRO. Inspect ownership
            # directly rather than mistaking that provider limitation for a bridge failure.
            assert not item._file.closed
    finally:
        if form in {"molsysmt.GROFileHandler", "mdtraj.GroTrajectoryFile"}:
            item.close()
            if form == "molsysmt.GROFileHandler":
                assert item.file.closed


@pytest.mark.parametrize(
    "source_form,target", EDGES, ids=[f"{s}->{t}" for s, t in EDGES]
)
def test_declared_gro_edge_executes_directly_and_publicly(
    source_form, target, tmp_path
):
    # Optional provider absence is checked during setup, never after conversion.
    for form in (source_form, target):
        if form.startswith("mdtraj."):
            pytest.importorskip("mdtraj")
        elif form.startswith("openmm."):
            pytest.importorskip("openmm")
    if target in {"openmm.Topology", "openmm.Modeller"}:
        pytest.importorskip("openmm")
    for route in ("direct", "public"):
        with source(source_form, tmp_path / route) as item:
            assert msm.get_form(item) == source_form
            kwargs = (
                {"output_filename": str(tmp_path / f"{route}-copy.gro")}
                if target == "file:gro"
                else {}
            )
            result = (
                _execute_direct(source_form, target, item, **kwargs)
                if route == "direct"
                else msm.convert(item, to_form=target, **kwargs)
            )
            try:
                assert msm.get_form(result) == target
                if target == "file:gro":
                    assert Path(result).read_text() == GRO_TEXT
            finally:
                if (
                    target in {"molsysmt.GROFileHandler", "mdtraj.GroTrajectoryFile"}
                    and result is not item
                ):
                    result.close()
                    if target == "molsysmt.GROFileHandler":
                        assert result.file.closed
