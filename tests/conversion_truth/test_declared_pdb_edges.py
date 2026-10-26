"""Execute declared PDB edges with literal local input and owned resources."""

from contextlib import contextmanager
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from devtools.scripts.audit_conversion_execution import (
    declared_edges,
    planned_edges,
    read_plan,
)
from tests.conversion_truth.test_declared_native_edges import (
    DOCKING_FORMS,
    PDB_FORMS,
    _execute_direct,
    _water_coordinates,
)
from tests.conversion_truth.test_declared_native_edges import (
    _source as _resident_source,
)

EDGES = sorted(
    (s, t)
    for s, t in planned_edges(declared_edges(), read_plan())
    if {s, t} & PDB_FORMS and not ({s, t} & DOCKING_FORMS)
)


def _pdb_text():
    # Fixed-column PDB coordinates are in angstroms, independent of any writer.
    atoms = (
        "ATOM      1  O   HOH A   1       0.000   0.000   0.000  1.00  0.00           O  \n"
        "ATOM      2  H1  HOH A   1       0.950   0.000   0.000  1.00  0.00           H  \n"
        "ATOM      3  H2  HOH A   1      -0.240   0.920   0.000  1.00  0.00           H  \n"
    )
    second = (
        "ATOM      1  O   HOH A   1       1.000   2.000   3.000  1.00  0.00           O  \n"
        "ATOM      2  H1  HOH A   1       1.950   2.000   3.000  1.00  0.00           H  \n"
        "ATOM      3  H2  HOH A   1       0.760   2.920   3.000  1.00  0.00           H  \n"
    )
    return (
        "HEADER    LOCAL CONVERSION EXECUTION FIXTURE\n"
        "MODEL        1\n"
        + atoms
        + "ENDMDL\nMODEL        2\n"
        + second
        + "ENDMDL\nCONECT    1    2    3\nEND\n"
    )


@contextmanager
def _source(form, directory, native):
    directory.mkdir()
    if form == "file:pdb":
        filename = directory / "source.pdb"
        filename.write_text(_pdb_text())
        yield str(filename)
    elif form == "string:pdb_text":
        yield _pdb_text()
    elif form == "molsysmt.PDBFileHandler":
        from molsysmt.native import PDBFileHandler

        handler = PDBFileHandler(_pdb_text())
        try:
            yield handler
        finally:
            handler.close()
        assert handler.file.closed
    elif form == "molsysmt.MolSys":
        yield native.copy()
    elif form == "molsysmt.Topology":
        yield native.topology.copy()
    else:
        yield _resident_source(form)


def _arguments(source, target, output, native):
    kwargs = {"output_filename": str(output)} if target == "file:pdb" else {}
    if source == "molsysmt.Topology":
        kwargs.update(
            coordinates=native.structures.coordinates,
            box=native.structures.box,
        )
    elif source == "openmm.Topology":
        kwargs["coordinates"] = msm.pyunitwizard.quantity(
            _water_coordinates()[:1], "nm"
        )
    return kwargs


@pytest.mark.parametrize("source,target", EDGES, ids=[f"{s}->{t}" for s, t in EDGES])
def test_declared_pdb_edge_executes_directly_and_publicly(
    source, target, rich_molsys, tmp_path
):
    for form in (source, target):
        if form.startswith("mdtraj."):
            pytest.importorskip("mdtraj")
        elif form.startswith("openmm."):
            pytest.importorskip("openmm")
        elif form.startswith("MDAnalysis."):
            pytest.importorskip("MDAnalysis")
    for route in ("direct", "public"):
        with _source(source, tmp_path / route, rich_molsys) as item:
            assert msm.get_form(item) == source
            kwargs = _arguments(
                source, target, tmp_path / f"{route}-result.pdb", rich_molsys
            )
            result = (
                _execute_direct(source, target, item, **kwargs)
                if route == "direct"
                else msm.convert(item, to_form=target, **kwargs)
            )
            try:
                assert msm.get_form(result) == target
                if target == "file:pdb":
                    assert Path(result).is_file()
                    assert any(
                        line.startswith(("ATOM  ", "HETATM"))
                        for line in Path(result).read_text().splitlines()
                    )
            finally:
                if target == "molsysmt.PDBFileHandler" and result is not item:
                    result.close()
                    assert result.file.closed
            if source == "molsysmt.PDBFileHandler":
                assert not item.file.closed


@pytest.mark.parametrize("route", ["direct", "public"])
def test_pdb_to_mdanalysis_topology_preserves_literal_records(route, tmp_path):
    pytest.importorskip("MDAnalysis")
    source = tmp_path / "water.pdb"
    text = _pdb_text()
    source.write_text(text)

    if route == "direct":
        output = _execute_direct("file:pdb", "MDAnalysis.Topology", str(source))
    else:
        output = msm.convert(str(source), to_form="MDAnalysis.Topology")

    assert output.n_atoms == 3
    assert output.n_residues == 1
    assert output.n_segments == 1
    assert output.ids.values.tolist() == [1, 2, 3]
    assert output.names.values.tolist() == ["O", "H1", "H2"]
    assert output.resnames.values.tolist() == ["HOH"]
    np.testing.assert_array_equal(output.bonds.values, [(0, 1), (0, 2)])
    assert source.read_text() == text
