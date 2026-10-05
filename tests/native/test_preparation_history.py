"""Protecting historical evidence, original axes and lossless persistence."""

from copy import deepcopy

import h5py
import numpy as np
import pytest

import molsysmt as msm
from tests.physchem.test_chemical_template import PROVENANCE, _source, _template


def prepared(source=None):
    source = _source() if source is None else source
    return msm.physchem.apply_chemical_template(
        source,
        template=_template(),
        atom_correspondence=np.column_stack((np.arange(6), np.arange(6))),
        template_provenance=PROVENANCE,
    )


def assert_tree(actual, expected):
    if isinstance(expected, np.ndarray):
        assert isinstance(actual, np.ndarray)
        assert actual.dtype == expected.dtype
        assert actual.shape == expected.shape
        np.testing.assert_array_equal(actual, expected)
    elif isinstance(expected, dict):
        assert list(actual) == list(expected)
        for key in expected:
            assert_tree(actual[key], expected[key])
    elif isinstance(expected, (list, tuple)):
        assert type(actual) is type(expected)
        assert len(actual) == len(expected)
        for value, reference in zip(actual, expected):
            assert_tree(value, reference)
    else:
        assert actual == expected


def test_success_attaches_detached_history_without_changing_input():
    source = _source()
    output = prepared(source)
    result = output["molecular_system"]
    assert source.chemical_states.get_preparation_history() == ()
    history = result.chemical_states.get_preparation_history()
    assert len(history) == 1
    assert history[0]["index_scope"] == "operation"
    assert history[0]["output"] == dict(n_atoms=6, n_bonds=5, chemical_state_index=0)
    assert_tree(history[0]["report"], output["report"])
    output["report"]["atom_correspondence"][:] = -1
    history[0]["report"]["template_provenance"]["identity"] = "edited"
    stored = result.chemical_states.get_preparation_history()[0]["report"]
    np.testing.assert_array_equal(
        stored["atom_correspondence"], np.column_stack((np.arange(6), np.arange(6)))
    )
    assert stored["template_provenance"] == PROVENANCE
    second = prepared(result)["molecular_system"]
    assert len(second.chemical_states.get_preparation_history()) == 2
    assert len(result.chemical_states.get_preparation_history()) == 1


@pytest.mark.parametrize("route", ["copy", "dict", "h5msm", "state_h5msm"])
def test_original_producer_and_typed_maps_survive_roundtrip(
    tmp_path, monkeypatch, route
):
    result = prepared()["molecular_system"]
    original = result.chemical_states.get_preparation_history()
    monkeypatch.setattr(msm, "__version__", "999.reading-version")
    if route == "copy":
        restored = result.copy().chemical_states
    elif route == "dict":
        payload = msm.convert(
            result.chemical_states, to_form="molsysmt.ChemicalStatesDict"
        )
        assert payload.data["version"] == 2
        restored = msm.convert(payload, to_form="molsysmt.ChemicalStates")
    else:
        path = tmp_path / "history.h5msm"
        if route == "h5msm":
            msm.convert(result, to_form=path)
            restored = msm.convert(path, to_form="molsysmt.MolSys").chemical_states
        else:
            msm.h5msm.write_layers(path, chemical_states=result.chemical_states)
            restored = msm.h5msm.read_layers(path)["chemical_states"]
        with h5py.File(path) as file:
            assert file.attrs["version"] == "0.5"
            assert file["chemical_states"].attrs["schema_version"] == 2
            assert (
                file["chemical_states/0/preparation_history/manifest"].compression
                == "gzip"
            )
    assert_tree(restored.get_preparation_history(), original)
    assert (
        restored.get_preparation_history()[0]["report"]["software"]["molsysmt"]
        != "999.reading-version"
    )


def test_extraction_merge_and_edits_keep_operation_indices_historical(tmp_path):
    result = prepared()["molecular_system"]
    original = result.chemical_states.get_preparation_history()
    subset = msm.extract(result, selection=[5, 1, 0], structure_indices=[2, 0, 1])
    assert subset.get_n_atoms() == 3
    assert_tree(subset.chemical_states.get_preparation_history(), original)
    msm.set(subset, element="atom", selection=[0], formal_charge=[1])
    assert_tree(subset.chemical_states.get_preparation_history(), original)
    merged = msm.merge([result, subset])
    assert merged.get_n_atoms() == 9
    assert_tree(merged.chemical_states.get_preparation_history(), original + original)
    path = tmp_path / "subset.h5msm"
    msm.convert(subset, to_form=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys")
    assert_tree(restored.chemical_states.get_preparation_history(), original)
    assert (
        restored.chemical_states.get_preparation_history()[0]["output"]["n_atoms"] == 6
    )


def test_assessment_and_failure_do_not_attach_history():
    source = _source()
    args = dict(
        template=_template(),
        atom_correspondence=np.column_stack((np.arange(6), np.arange(6))),
        template_provenance=PROVENANCE,
    )
    assert (
        msm.physchem.assess_chemical_template(source, **args)["status"] == "compatible"
    )
    assert source.chemical_states.get_preparation_history() == ()
    source.chemical_states._states[0].set_atom_attribute(
        "formal_charge", [1], atom_indices=[0]
    )
    from molsysmt._private.smonitor import StructuralInconsistencyError

    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.apply_chemical_template(source, **args)
    assert source.chemical_states.get_preparation_history() == ()


def test_old_records_and_files_have_empty_history(tmp_path):
    source = _source()
    payload = msm.convert(source.chemical_states, to_form="molsysmt.ChemicalStatesDict")
    assert payload.data["version"] == 1
    assert (
        msm.convert(
            payload, to_form="molsysmt.ChemicalStates"
        ).get_preparation_history()
        == ()
    )
    path = tmp_path / "no-history.h5msm"
    msm.convert(source, to_form=path)
    with h5py.File(path) as file:
        assert file["chemical_states"].attrs["schema_version"] == 1
        assert "preparation_history" not in file["chemical_states/0"]
    assert (
        msm.convert(
            path, to_form="molsysmt.MolSys"
        ).chemical_states.get_preparation_history()
        == ()
    )
    state = source.chemical_states._states[0]
    del state._preparation_history
    state._ensure_compatibility(6)
    assert source.chemical_states.get_preparation_history() == ()


@pytest.mark.parametrize(
    "damage", ["layer", "history", "array_shape", "array_dtype", "orphan"]
)
def test_corrupt_history_is_rejected_instead_of_silently_lost(tmp_path, damage):
    result = prepared()["molecular_system"]
    path = tmp_path / "damaged.h5msm"
    msm.convert(result, to_form=path)
    with h5py.File(path, "r+") as file:
        history = file["chemical_states/0/preparation_history"]
        if damage == "layer":
            file["chemical_states"].attrs["schema_version"] = 1
        elif damage == "history":
            history.attrs["schema_version"] = 999
        elif damage == "orphan":
            history["arrays"].create_dataset("extra", data=[1]).attrs["numpy_dtype"] = (
                "<i8"
            )
        else:
            arrays = history["arrays"]
            key = next(iter(arrays))
            values = arrays[key][()]
            dtype = arrays[key].attrs["numpy_dtype"]
            del arrays[key]
            if damage == "array_shape":
                values = values.reshape(-1, 1)
            else:
                values = values.astype(np.int32)
            arrays.create_dataset(key, data=values).attrs["numpy_dtype"] = dtype
    with pytest.raises(ValueError):
        msm.convert(path, to_form="molsysmt.MolSys")


def test_legacy_molsys_dict_rejects_report_loss():
    result = prepared()["molecular_system"]
    report = msm.get_conversion_report(result, to_form="molsysmt.MolSysDict")
    assert any(issue.attribute == "preparation_history" for issue in report.issues)
    with pytest.raises(ValueError, match="preparation history"):
        msm.convert(result, to_form="molsysmt.MolSysDict")


def test_only_selected_state_receives_history_and_atom_expansion_retains_evidence():
    source = _source()
    source.chemical_states._append_state(source.chemical_states._states[0].copy())
    result = msm.physchem.apply_chemical_template(
        source,
        template=_template(),
        atom_correspondence=np.column_stack((np.arange(6), np.arange(6))),
        template_provenance=PROVENANCE,
        chemical_state=1,
    )["molecular_system"]
    assert result.chemical_states.get_preparation_history(0) == ()
    assert (
        result.chemical_states.get_preparation_history(1)[0]["output"][
            "chemical_state_index"
        ]
        == 1
    )
    assert source.chemical_states.get_preparation_history(1) == ()
    result = prepared()["molecular_system"]
    history = result.chemical_states.get_preparation_history()
    expanded = msm.build.add_terminal_atoms(
        result,
        [dict(parent_atom_index=0, atom_type="H")],
        msm.pyunitwizard.quantity(np.zeros((3, 1, 3)), "nm"),
    )["molecular_system"]
    assert expanded.get_n_atoms() == 7
    expanded_history = expanded.chemical_states.get_preparation_history()
    assert_tree(expanded_history[:-1], history)
    assert expanded_history[-1]["report"]["schema"] == "molsysmt.terminal_attachment@1"
    assert expanded_history[-1]["report"]["structure_indices"].tolist() == [0, 1, 2]
    assert expanded_history[-1]["output"]["n_atoms"] == 7


def test_codec_handles_empty_and_unicode_arrays_and_rejects_objects(tmp_path):
    from molsysmt._private.preparation_history import decode_history, encode_history

    history = list(
        prepared()["molecular_system"].chemical_states.get_preparation_history()
    )
    history[0]["report"]["control"] = dict(
        empty=np.empty((0, 2), dtype=np.int32),
        unicode=np.array(["α", ""], dtype="U2"),
        scalar=np.array(1, dtype=np.uint8),
        sequence=(None, True, 3.5),
    )
    assert_tree(decode_history(encode_history(history)), history)
    from molsysmt.form._h5msm_preparation_history import read_history, write_history

    with h5py.File(tmp_path / "typed-history.h5", "w") as file:
        write_history(file, history)
        assert_tree(read_history(file), history)
    invalid = deepcopy(history)
    invalid[0]["report"]["control"] = np.array([object()])
    with pytest.raises(ValueError, match="dtype"):
        encode_history(invalid)
