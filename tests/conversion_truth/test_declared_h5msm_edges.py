"""Execute declared legacy-H5MSM edges and separately check the public 0.5 route.

The registered low-level disk/handler adapters use 0.4. Public convert writes
0.5 and materializes modular inputs before resident conversion. These versions
must be asserted explicitly rather than mistaken for equivalent raw codecs.
"""

from contextlib import contextmanager

import h5py
import numpy as np
import pytest

import molsysmt as msm
from devtools.scripts.audit_conversion_execution import (
    declared_edges,
    planned_edges,
    read_plan,
)
from molsysmt import pyunitwizard as puw
from molsysmt.native import H5MSMFileHandler
from tests.conversion_truth.test_declared_native_edges import (
    DOCKING_FORMS,
    H5MSM_FORMS,
    PDB_FORMS,
    TRAJECTORY_FORMS,
    _execute_direct,
)

EDGES = sorted(
    (s, t)
    for s, t in planned_edges(declared_edges(), read_plan())
    if {s, t} & H5MSM_FORMS
    and not ({s, t} & (PDB_FORMS | DOCKING_FORMS | TRAJECTORY_FORMS))
)


@contextmanager
def _source(form, directory, native):
    directory.mkdir()
    system = native.copy()
    if form not in H5MSM_FORMS:
        yield {
            "molsysmt.MolSys": system,
            "molsysmt.Topology": system.topology,
            "molsysmt.Structures": system.structures,
        }[form]
        return
    from molsysmt.form.molsysmt_MolSys.to_file_h5msm import to_file_h5msm

    filename = str(directory / "source04.h5msm")
    to_file_h5msm(system, output_filename=filename)
    with h5py.File(filename, "r") as file:
        assert file.attrs["version"] == "0.4"
    if form == "file:h5msm":
        yield filename
    else:
        with H5MSMFileHandler(filename) as handler:
            yield handler
        assert not handler.file.id.valid


def _check_and_close(result, target, source, version):
    try:
        assert msm.get_form(result) == target
        if target == "file:h5msm":
            with h5py.File(result, "r") as file:
                assert file.attrs["version"] == version
    finally:
        if isinstance(result, H5MSMFileHandler) and result is not source:
            result.close()
            assert not result.file.id.valid


@pytest.mark.parametrize("source,target", EDGES, ids=[f"{s}->{t}" for s, t in EDGES])
def test_declared_h5msm_edge_executes_directly_and_publicly(
    source, target, rich_molsys, tmp_path
):
    for route in ("direct", "public"):
        with _source(source, tmp_path / route, rich_molsys) as item:
            assert msm.get_form(item) == source
            kwargs = (
                {"output_filename": str(tmp_path / f"{route}-result.h5msm")}
                if target == "file:h5msm"
                else {}
            )
            result = (
                _execute_direct(source, target, item, **kwargs)
                if route == "direct"
                else msm.convert(item, to_form=target, **kwargs)
            )
            _check_and_close(
                result, target, item, "0.4" if route == "direct" else "0.5"
            )
            if isinstance(item, H5MSMFileHandler):
                assert item.file.id.valid


def _analysis():
    return msm.Interactions.from_records(
        [
            {
                "structure_index": 0,
                "interaction_type": "pair",
                "participants": [
                    {"role": "first", "atom_indices": [0]},
                    {"role": "second", "atom_indices": [2]},
                ],
                "evidence": evidence,
                "measurements": {"distance": 0.20 + 0.01 * index},
            }
            for index, evidence in enumerate(("first", "parallel"))
        ],
        n_atoms=4,
        n_structures=3,
        evaluated_structure_indices=[0, 1],
        method="h5msm-execution-control",
        parameters={"cutoff": 0.3},
        measure_units={"distance": "nm"},
        software={"producer": "h5msm-test-1"},
        source_id="declared-source",
        atom_source_indices=[10, 30, 40, 70],
        structure_source_indices=[9, 7, 5],
        source_n_atoms=80,
        source_n_structures=10,
    )


@pytest.mark.parametrize(
    "layers", ["complete", "topology", "structures", "chemical_states", "interactions"]
)
def test_public_modular_roundtrip_preserves_present_domains(
    layers, rich_molsys, tmp_path
):
    system = rich_molsys.copy()
    system.interactions = {"review": _analysis()}
    filename = tmp_path / "modular05.h5msm"
    if layers == "complete":
        msm.convert(system, to_form="file:h5msm", output_filename=filename)
    else:
        payload = {
            "topology": system.topology,
            "structures": system.structures,
            "chemical_states": system.chemical_states,
            "interactions": dict(system.interactions),
        }[layers]
        msm.h5msm.write_layers(filename, **{layers: payload})
    with h5py.File(filename, "r") as file:
        assert file.attrs["version"] == "0.5"
    restored = msm.convert(filename, to_form="molsysmt.MolSys")
    assert (restored.topology is not None) == (layers in {"complete", "topology"})
    assert (restored.structures is not None) == (layers in {"complete", "structures"})
    assert (restored.chemical_states is not None) == (
        layers in {"complete", "chemical_states"}
    )
    assert bool(restored.interactions) == (layers in {"complete", "interactions"})
    if restored.structures is not None:
        np.testing.assert_array_equal(
            puw.get_value(restored.structures.coordinates, to_unit="nm"),
            puw.get_value(system.structures.coordinates, to_unit="nm"),
        )
        np.testing.assert_array_equal(
            puw.get_value(restored.structures.box, to_unit="nm"),
            puw.get_value(system.structures.box, to_unit="nm"),
        )
    if restored.interactions:
        before = _analysis()
        after = restored.interactions["review"]
        for key in ("atom_source_indices", "structure_source_indices"):
            np.testing.assert_array_equal(getattr(after, key), getattr(before, key))
        assert after.method == before.method
        assert after.parameters == before.parameters
        assert after.measure_units == before.measure_units
        assert after.software == {"producer": "h5msm-test-1"}
        np.testing.assert_array_equal(
            after.to_dict()["measurements"]["distance"],
            before.to_dict()["measurements"]["distance"],
        )
        for key in ("occurrence_indices", "evaluated_structure_indices"):
            np.testing.assert_array_equal(after.to_dict()[key], before.to_dict()[key])
        assert (
            restored.interactions["review"].query(structure_indices=[1]).n_interactions
            == 0
        )
        assert (
            restored.interactions["review"]
            .query(structure_indices=[2])
            .to_dict()["evaluated_structure_indices"]
            .size
            == 0
        )


def test_public_modular_selection_remaps_analysis_and_geometry(rich_molsys, tmp_path):
    system = rich_molsys.copy()
    system.interactions = {"review": _analysis()}
    filename = tmp_path / "complete05.h5msm"
    msm.convert(system, to_form="file:h5msm", output_filename=filename)
    restored = msm.convert(
        filename,
        to_form="molsysmt.MolSys",
        selection=[2, 0],
        structure_indices=[2, 0, 2],
    )
    expected = puw.get_value(system.structures.coordinates, to_unit="nm")[[2, 0, 2]][
        :, [0, 2], :
    ]
    np.testing.assert_array_equal(
        puw.get_value(restored.structures.coordinates, to_unit="nm"), expected
    )
    analysis = restored.interactions["review"]
    payload = analysis.to_dict()
    np.testing.assert_array_equal(analysis.atom_source_indices, [10, 40])
    np.testing.assert_array_equal(analysis.structure_source_indices, [5, 9, 5])
    np.testing.assert_array_equal(payload["evaluated_structure_indices"], [1])
    np.testing.assert_array_equal(payload["structure_indices"], [1, 1])
    np.testing.assert_array_equal(payload["occurrence_indices"], [0, 1])


def test_modular_handler_rejection_does_not_materialize_domains(
    rich_molsys, tmp_path, monkeypatch
):
    from molsysmt._private.smonitor import FormatError
    from molsysmt.form import _h5msm05_modular
    from molsysmt.form.file_h5msm.to_molsysmt_H5MSMFileHandler import (
        to_molsysmt_H5MSMFileHandler,
    )

    filename = tmp_path / "modular05.h5msm"
    msm.h5msm.write(rich_molsys, filename)

    def reject_loading(*args, **kwargs):
        pytest.fail("Legacy-handler rejection must precede resident domain loading")

    monkeypatch.setattr(_h5msm05_modular, "read_molsys_file", reject_loading)
    for operation in (
        to_molsysmt_H5MSMFileHandler,
        lambda item: msm.convert(item, to_form="molsysmt.H5MSMFileHandler"),
    ):
        with pytest.raises(FormatError, match="supports only H5MSM 0.3 and 0.4"):
            operation(filename)
    with h5py.File(filename, "r") as file:
        assert file.attrs["version"] == "0.5"
