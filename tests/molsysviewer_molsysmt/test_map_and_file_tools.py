"""Receive explicit map/file contracts without adopting outputs or editing scenes."""

import copy
import inspect
import json
from pathlib import Path

import h5py
import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentError,
    FormatError,
    LegacyH5MSMWarning,
    StructuralInconsistencyError,
)
from molsysmt.native import MolSys, Structures

puw = msm.pyunitwizard
PATHS = [
    "basic.compose_atom_maps",
    "basic.permute_atoms",
    *[
        f"h5msm.{name}"
        for name in (
            "read",
            "write",
            "read_layers",
            "write_layers",
            "append_structures",
            "migrate_04_to_05",
            "migrate_to_05",
        )
    ],
    "form.file_fasta.read_records",
    "form.file_fasta.parse_records",
]
PRIMARY = {"basic.permute_atoms", "h5msm.write"}


def resolve(root, path):
    for name in path.split("."):
        root = getattr(root, name)
    return root


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as result:
            yield result


@pytest.fixture
def chemical_view():
    from rdkit import Chem

    source = msm.convert(Chem.MolFromSmiles("CCO"))
    source.structures = Structures(
        coordinates=puw.quantity(np.arange(27).reshape(3, 3, 3), "nm")
    )
    with msv.new_view(source) as result:
        yield result


@pytest.mark.parametrize("path", PATHS)
def test_exact_native_signature_and_digestion(path):
    with msv.new_view() as view:
        method = resolve(view.addons.molsysmt, path)
        native = inspect.signature(resolve(msm, path))
        parameters = list(native.parameters.values())
        if path in PRIMARY:
            parameters = parameters[1:]
        assert inspect.signature(method) == native.replace(parameters=parameters)
        assert method.digestion_plan is not None
        assert "update_view" not in inspect.signature(method).parameters
        assert "View integration" in inspect.getdoc(method)
        if path.startswith("basic."):
            assert resolve(view.addons.molsysmt, path.split(".")[-1]) == method
        else:
            assert not hasattr(view.addons.molsysmt, path.split(".")[-1])


def atom_map(n_source, inverse):
    forward = [-1] * n_source
    for output, source in enumerate(inverse):
        if source >= 0:
            forward[source] = output
    return dict(
        schema="molsysmt.atom_map@1",
        n_source_atoms=n_source,
        n_output_atoms=len(inverse),
        source_to_output_atom_indices=forward,
        output_to_source_atom_indices=inverse,
    )


def test_compose_explicit_maps_before_loading_and_preserve_inputs():
    maps = [atom_map(2, [0, 1, -1]), atom_map(3, [2, 0])]
    before = copy.deepcopy(maps)
    with msv.new_view() as view:
        tools = view.addons.molsysmt
        state, status = view.export_state(), tools.get_sync_status()
        first = tools.basic.compose_atom_maps(maps)
        second = tools.basic.compose_atom_maps(json.loads(json.dumps(maps)))
        assert first["source_to_output_atom_indices"].tolist() == [1, -1]
        assert first["output_to_source_atom_indices"].tolist() == [-1, 0]
        first["output_to_source_atom_indices"][0] = 55
        assert second["output_to_source_atom_indices"].tolist() == [-1, 0]
        assert maps == before
        assert view.molsys is None
        assert view.export_state() == state and tools.get_sync_status() == status


@pytest.mark.parametrize(
    "maps,error",
    [
        ([], ArgumentError),
        ([atom_map(2, [0]), atom_map(2, [1])], StructuralInconsistencyError),
    ],
)
def test_compose_retains_native_errors(view, maps, error):
    with pytest.raises(error) as native:
        msm.basic.compose_atom_maps(maps)
    with pytest.raises(type(native.value)):
        view.addons.molsysmt.basic.compose_atom_maps(maps)


@pytest.mark.parametrize("report", [False, True])
@pytest.mark.parametrize("skip", [False, True])
def test_permutation_is_independent_and_reads_pending_source(
    chemical_view, report, skip
):
    view = chemical_view
    tools = view.addons.molsysmt
    scene_before = copy.deepcopy(view.widget.initial_messages)
    tools.basic.set(
        coordinates=puw.quantity(np.arange(27).reshape(3, 3, 3), "nm"),
        update_view=False,
    )
    source = view.molsys
    order = np.array([2, 0, 1])
    order.flags.writeable = False
    status = tools.get_sync_status()
    before = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    result = tools.basic.permute_atoms(order, return_report=report, skip_digestion=skip)
    output = result["molecular_system"] if report else result
    assert output is not source and view.molsys is source
    np.testing.assert_array_equal(
        puw.get_value(output.structures.coordinates, to_unit="nm"), before[:, order]
    )
    assert (
        output.topology.atoms.atom_name.tolist()
        == source.topology.atoms.atom_name.iloc[order].tolist()
    )
    if report:
        assert (
            result["report"]["output_to_source_atom_indices"].tolist() == order.tolist()
        )
    output.structures.coordinates = puw.quantity(np.full((3, 3, 3), -99), "nm")
    np.testing.assert_array_equal(
        puw.get_value(source.structures.coordinates, to_unit="nm"), before
    )
    assert (
        view.widget.initial_messages == scene_before
        and tools.get_sync_status() == status
    )


@pytest.mark.parametrize("order", [[0], [0] * 62, list(range(1, 63)), [True] * 62])
@pytest.mark.parametrize("skip", [False, True])
def test_permutation_rejects_invalid_bijections_without_effect(view, order, skip):
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    with pytest.raises(ArgumentError):
        view.addons.molsysmt.basic.permute_atoms(order, skip_digestion=skip)
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status() == status


def test_cached_permutation_follows_replacement_and_rich_domain_maps(chemical_view):
    from tests.basic.test_permute_atoms import ORDER, rich_system

    view = chemical_view
    method = view.addons.molsysmt.basic.permute_atoms
    assert method([2, 0, 1]).get_n_atoms() == 3
    view.load(rich_system(), mode="replace")
    source, state = view.molsys, view.export_state()
    result = method(ORDER, return_report=True)
    output = result["molecular_system"]
    expected = msm.basic.permute_atoms(source, ORDER)
    assert result["report"]["source_to_output_atom_indices"].tolist() == [
        2,
        0,
        4,
        3,
        5,
        1,
    ]
    assert (
        output.interactions["rings"].participant_atoms.tolist()
        == expected.interactions["rings"].participant_atoms.tolist()
    )
    assert output.interactions["rings"].evaluated_structure_indices.tolist() == [0, 1]
    assert output.interactions["rings"].n_interactions == 2
    np.testing.assert_array_equal(
        output.molecular_mechanics.partial_charge,
        expected.molecular_mechanics.partial_charge,
    )
    pd.testing.assert_frame_equal(
        output.chemical_states.get_bonds(), expected.chemical_states.get_bonds()
    )
    assert view.molsys is source and view.export_state() == state


def test_legacy_demo_consistency_rejection_is_not_hidden(view):
    order = list(range(61, -1, -1))
    with pytest.raises(StructuralInconsistencyError, match="chain_index"):
        msm.basic.permute_atoms(view.molsys, order)
    with pytest.raises(StructuralInconsistencyError, match="chain_index"):
        view.addons.molsysmt.basic.permute_atoms(order)


def test_write_reads_pending_primary_and_read_does_not_adopt(chemical_view, tmp_path):
    view = chemical_view
    tools = view.addons.molsysmt
    scene_before = copy.deepcopy(view.widget.initial_messages)
    coordinates = puw.quantity(np.arange(27).reshape(3, 3, 3), "angstrom")
    tools.basic.set(coordinates=coordinates, update_view=False)
    source = view.molsys
    status = tools.get_sync_status()
    path = str(tmp_path / "pending.h5msm")
    assert tools.h5msm.write(path) == path
    restored = tools.h5msm.read(path)
    assert restored is not source and view.molsys is source
    np.testing.assert_allclose(
        puw.get_value(restored.structures.coordinates, to_unit="nm"),
        puw.get_value(coordinates, to_unit="nm"),
    )
    assert (
        view.widget.initial_messages == scene_before
        and tools.get_sync_status() == status
    )


def test_write_preserves_native_mechanics_rejection(view, tmp_path):
    view.molsys.molecular_mechanics.forcefield = "explicit-unsupported-forcefield"
    path = tmp_path / "rejected.h5msm"
    with pytest.raises(ValueError, match="molecular mechanics"):
        view.addons.molsysmt.h5msm.write(path)
    assert not path.exists()


@pytest.mark.parametrize("coordinates", [False, True])
def test_explicit_layers_and_append_work_without_primary(tmp_path, coordinates):
    structures = (
        Structures(coordinates=puw.quantity(np.arange(12).reshape(2, 2, 3), "nm"))
        if coordinates
        else Structures(time=puw.quantity([0, 1], "ps"))
    )
    path = str(tmp_path / "only_structures.h5msm")
    with msv.new_view() as view:
        files = view.addons.molsysmt.h5msm
        assert files.write_layers(path, structures=structures) == path
        assert files.append_structures(path, structures, block_size=1) == path
        restored = files.read(path)
        assert restored.topology is None
        assert restored.structures.n_structures == 4
        if coordinates:
            np.testing.assert_array_equal(
                puw.get_value(restored.structures.coordinates, to_unit="nm"),
                np.tile(np.arange(12).reshape(2, 2, 3), (2, 1, 1)),
            )
        else:
            np.testing.assert_array_equal(
                puw.get_value(restored.structures.time, to_unit="ps"), [0, 1, 0, 1]
            )
        assert files.read_layers(path, layers="interactions")["interactions"] is None
        assert view.molsys is None


def test_append_explicit_file_never_edits_primary_and_rejects_before_resize(
    chemical_view, tmp_path
):
    view = chemical_view
    files = view.addons.molsysmt.h5msm
    state, status = view.export_state(), view.addons.molsysmt.get_sync_status()
    before = puw.get_value(view.molsys.structures.coordinates).copy()
    filename = str(tmp_path / "external.h5msm")
    files.write_layers(filename, structures=view.molsys.structures)
    files.append_structures(filename, view.molsys.structures, block_size=2)
    assert files.read(filename).structures.n_structures == 6
    invalid = Structures(coordinates=puw.quantity(np.zeros((1, 2, 3)), "nm"))
    with pytest.raises(ValueError):
        files.append_structures(filename, invalid)
    assert files.read(filename).structures.n_structures == 6
    np.testing.assert_array_equal(
        puw.get_value(view.molsys.structures.coordinates), before
    )
    assert (
        view.export_state() == state
        and view.addons.molsysmt.get_sync_status() == status
    )


def test_empty_and_named_interactions_remain_distinct_and_unattached(view, tmp_path):
    files = view.addons.molsysmt.h5msm
    state = view.export_state()
    analysis = msm.Interactions.from_records(
        [],
        n_atoms=3,
        n_structures=4,
        evaluated_structure_indices=[0, 3],
        method="explicit-native-test",
    )
    path = str(tmp_path / "analyses.h5msm")
    files.write_layers(path, interactions={"first": analysis, "second": analysis})
    layers = files.read_layers(path, layers="interactions", analysis_names=["second"])
    assert set(layers["interactions"]) == {"second"}
    assert layers["interactions"]["second"].evaluated_structure_indices.tolist() == [
        0,
        3,
    ]
    restored = files.read(path)
    assert restored.topology is None and restored.structures is None
    assert restored.get_n_atoms() == 3
    empty = str(tmp_path / "empty.h5msm")
    files.write_layers(empty, interactions={})
    assert files.read_layers(empty, layers="interactions")["interactions"] == {}
    with pytest.raises(ValueError, match="read_layers"):
        files.read(empty)
    assert view.export_state() == state and not view.molsys.interactions


@pytest.mark.parametrize("name", ["migrate_04_to_05", "migrate_to_05"])
def test_legacy_migration_preserves_source_and_does_not_load(tmp_path, name):
    from molsysmt.form.molsysmt_MolSys.to_file_h5msm import to_file_h5msm

    source = MolSys(n_atoms=2)
    source.structures = Structures(coordinates=puw.quantity(np.zeros((1, 2, 3)), "nm"))
    old, new = str(tmp_path / "old.h5msm"), str(tmp_path / "new.h5msm")
    to_file_h5msm(source, output_filename=old)
    before = Path(old).read_bytes()
    with msv.new_view() as view:
        with pytest.warns(LegacyH5MSMWarning):
            result = getattr(view.addons.molsysmt.h5msm, name)(old, new)
        assert Path(result) == Path(new)
        assert Path(old).read_bytes() == before
        with h5py.File(new) as file:
            assert file.attrs["version"] == "0.5"
        assert view.addons.molsysmt.h5msm.read(new).get_n_atoms() == 2
        assert view.molsys is None


@pytest.mark.parametrize("ending", ["\r", "\n", "\r\n"])
def test_fasta_exact_text_spans_occurrences_and_independent_results(tmp_path, ending):
    text = ending + ending.join(
        [">β  ", " acD ", "A*", ">repeat", "M[mod]", ">repeat", "M[mod]", ">", ""]
    )
    path = tmp_path / "submitted.fasta"
    path.write_bytes(text.encode("utf-8"))
    with msv.new_view() as view:
        files = view.addons.molsysmt.form.file_fasta
        parsed = files.parse_records(text, source_label=str(path))
        read = files.read_records(path)
        assert read == parsed == msm.form.file_fasta.read_records(path)
        assert json.loads(json.dumps(read)) == read
        assert [r["record_index"] for r in read["records"]] == [0, 1, 2, 3]
        assert (
            read["preamble"] + "".join(r["raw_record"] for r in read["records"]) == text
        )
        for record in read["records"]:
            start, end = record["source_span"]
            assert text[start:end] == record["raw_record"]
        read["records"][0]["source_span"][0] = -99
        assert files.read_records(path) == parsed
        assert path.read_bytes() == text.encode("utf-8") and view.molsys is None


def test_fasta_native_errors_remain_explicit(tmp_path):
    with msv.new_view() as view:
        files = view.addons.molsysmt.form.file_fasta
        for text in ["ACD\n>a\nM", " >a\nM", "\ufeff>a\nM"]:
            with pytest.raises(FormatError):
                files.parse_records(text)
        with pytest.raises(ArgumentError):
            files.parse_records(b">a\nM")
        with pytest.raises(FileNotFoundError):
            files.read_records(tmp_path / "missing.fasta")
        path = tmp_path / "invalid.fasta"
        path.write_bytes(b">a\n\xff")
        with pytest.raises(FormatError) as caught:
            files.read_records(path)
        assert isinstance(caught.value.__cause__, UnicodeDecodeError)


def test_primary_methods_need_system_and_cached_utilities_observe_closed_view(tmp_path):
    view = msv.new_view()
    tools = view.addons.molsysmt
    with pytest.raises(ValueError, match="Load a molecular system"):
        tools.basic.permute_atoms([])
    with pytest.raises(ValueError, match="Load a molecular system"):
        tools.h5msm.write(tmp_path / "missing.h5msm")
    view.close()
    for method, arguments in [
        (tools.basic.compose_atom_maps, ([atom_map(0, [])],)),
        (tools.basic.permute_atoms, ([],)),
        (tools.h5msm.read, (tmp_path / "absent.h5msm",)),
        (tools.h5msm.write, (tmp_path / "absent.h5msm",)),
        (tools.h5msm.write_layers, (tmp_path / "absent.h5msm",)),
        (tools.form.file_fasta.read_records, (tmp_path / "absent.fasta",)),
        (tools.form.file_fasta.parse_records, (">a\nM",)),
    ]:
        with pytest.raises(RuntimeError, match="closed view"):
            method(*arguments)
    assert not list(tmp_path.iterdir())
