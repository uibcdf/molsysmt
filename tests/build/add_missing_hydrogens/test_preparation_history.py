"""Retaining original H-generation and attachment evidence across system domains."""

from copy import deepcopy

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import MolSys
from tests.build.add_missing_hydrogens.test_fixed_state import hydrogenate, prepared
from tests.native.test_preparation_history import assert_tree


@pytest.mark.parametrize("form", ["native", "h5msm"])
@pytest.mark.parametrize("return_report", [True, False])
def test_hydrogen_reports_persist_even_when_not_returned(
    tmp_path, monkeypatch, form, return_report
):
    source = prepared("CO", [[0, 0, 0], [1.4, 0, 0]])
    molecular_system = source
    if form == "h5msm":
        molecular_system = tmp_path / "input.h5msm"
        msm.convert(source, to_form=molecular_system)
    with msm.pyunitwizard.context(standard_units=["pm", "fs", "coulomb"]):
        result = msm.build.add_missing_hydrogens(
            molecular_system,
            mode="fixed_chemical_state",
            pH=None,
            engine="RDKit",
            return_report=return_report,
        )
    output = result["molecular_system"] if return_report else result
    history = output.chemical_states.get_preparation_history()
    assert [record["report"]["schema"] for record in history] == [
        "molsysmt.terminal_attachment@1",
        "molsysmt.hydrogen_addition@1",
    ]
    assert source.chemical_states.get_preparation_history() == ()
    assert all(record["index_scope"] == "operation" for record in history)
    assert all(
        record["output"] == dict(n_atoms=6, n_bonds=5, chemical_state_index=0)
        for record in history
    )
    for record in history:
        report = record["report"]
        assert report["source"]["n_atoms"] == 2
        assert report["source"]["n_structures"] == 1
        assert report["structure_indices"].dtype == np.dtype("int64")
        assert report["structure_indices"].tolist() == [0]
        assert report["coordinate_unit"] == "nm"
        assert report["software"]["molsysmt"]
    assert history[0]["report"]["coordinate_evidence"] == "supplied_coordinates"
    assert history[1]["report"]["coordinate_evidence"] == "generated_local_geometry"
    audit = history[1]["report"]["chemical_readiness"]["fields"]
    assert audit["formal_charge"]["values"] == [0, 0]
    assert all(type(value) is int for value in audit["formal_charge"]["values"])
    assert all(type(value) is bool for value in audit["atom_is_aromatic"]["values"])
    assert audit["isotope"]["values"] == [None, None]
    assert audit["formal_charge"]["origin"].dtype.kind == "U"
    if return_report:
        assert_tree(history[-1]["report"], result["report"])
        result["report"]["parent_hydrogen_pairs"][:] = -1
        assert (
            output.chemical_states.get_preparation_history()[-1]["report"][
                "parent_hydrogen_pairs"
            ]
            >= 0
        ).all()
    # Neither the writer's version nor read-time credit can replace producer evidence.
    monkeypatch.setattr(msm, "__version__", "999.reader")

    def reject_credit(*args, **kwargs):
        raise AssertionError(
            "Reading or importing history must not credit new preparation."
        )

    monkeypatch.setattr(msm._ackredit, "credit", reject_credit)
    path = tmp_path / "with-hydrogens.h5msm"
    msm.convert(output, to_form=path)
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    assert_tree(loaded.chemical_states.get_preparation_history(), history)
    payload = msm.convert(loaded, to_form="molsysmt.ChemicalStatesDict")
    restored = msm.convert(payload, to_form="molsysmt.ChemicalStates")
    assert_tree(restored.get_preparation_history(), history)
    for name in ["coordinates", "box"]:
        actual, expected = (
            getattr(loaded.structures, name),
            getattr(output.structures, name),
        )
        if expected is not None:
            np.testing.assert_array_equal(
                msm.pyunitwizard.get_value(actual, to_unit="nm"),
                msm.pyunitwizard.get_value(expected, to_unit="nm"),
            )


def test_import_preserves_original_domains_and_is_transactional(tmp_path):
    generated = hydrogenate(prepared("C", [[0, 0, 0]]))["molecular_system"]
    history = generated.chemical_states.get_preparation_history()
    destination = MolSys(n_atoms=20)
    assert destination.chemical_states.append_preparation_history(history) == (0, 1)
    assert_tree(destination.chemical_states.get_preparation_history(), history)
    assert destination.get_n_atoms() == 20
    assert all(record["output"]["n_atoms"] == 5 for record in history)
    assert (
        destination.chemical_states.get_preparation_history()[1]["report"]["source"][
            "n_atoms"
        ]
        == 1
    )
    # Stored reports and caller payloads never share editable arrays.
    history[1]["report"]["parent_hydrogen_pairs"][:] = -1
    assert (
        destination.chemical_states.get_preparation_history()[1]["report"][
            "parent_hydrogen_pairs"
        ]
        >= 0
    ).all()
    before = destination.chemical_states.get_preparation_history()
    invalid = deepcopy(before)
    invalid[1]["output"]["n_atoms"] = -1
    with pytest.raises(ArgumentError):
        destination.chemical_states.append_preparation_history(invalid)
    invalid = deepcopy(before)
    invalid[1]["report"]["unsupported"] = np.array([object()])
    with pytest.raises(ArgumentError):
        destination.chemical_states.append_preparation_history(invalid)
    assert_tree(destination.chemical_states.get_preparation_history(), before)
    assert destination.chemical_states.append_preparation_history(()) == ()
    destination.chemical_states.append_state()
    assert destination.chemical_states.append_preparation_history(
        before[-1:], chemical_state=1
    ) == (0,)
    assert (
        destination.chemical_states.get_preparation_history(1)[0]["report"]["schema"]
        == "molsysmt.hydrogen_addition@1"
    )
    path = tmp_path / "independent-history.h5msm"
    msm.h5msm.write_layers(path, chemical_states=destination.chemical_states)
    assert_tree(
        msm.h5msm.read_layers(path)["chemical_states"].get_preparation_history(), before
    )


def test_successful_no_addition_is_recorded_and_failure_does_not_touch_source():
    source = prepared("C", [[0, 0, 0]])
    full = hydrogenate(source)["molecular_system"]
    history = full.chemical_states.get_preparation_history()
    repeated = hydrogenate(full)
    next_history = repeated[
        "molecular_system"
    ].chemical_states.get_preparation_history()
    assert_tree(next_history[:-2], history)
    assert [entry["report"]["status"] for entry in next_history[-2:]] == [
        "unchanged",
        "unchanged",
    ]
    assert_tree(full.chemical_states.get_preparation_history(), history)
    with pytest.raises(StructuralInconsistencyError):
        msm.build.add_terminal_atoms(
            full,
            [dict(parent_atom_index=999, atom_type="H")],
            msm.pyunitwizard.quantity(np.zeros((1, 1, 3)), "nm"),
        )
    full.chemical_states._states[0].atom_attributes.loc[0, "n_unpaired_electrons"] = 1
    with pytest.raises(StructuralInconsistencyError):
        hydrogenate(full)
    assert_tree(full.chemical_states.get_preparation_history(), history)


def test_attachment_history_tracks_all_structures_before_selection(tmp_path):
    source = MolSys(n_atoms=1)
    source.structures.coordinates = msm.pyunitwizard.quantity(
        np.zeros((3, 1, 3)), "angstrom"
    )
    output = msm.build.add_terminal_atoms(
        source,
        [dict(parent_atom_index=0, atom_type="H")],
        msm.pyunitwizard.quantity(np.ones((3, 1, 3)), "angstrom"),
    )
    history = output["molecular_system"].chemical_states.get_preparation_history()
    assert history[0]["report"]["structure_indices"].tolist() == [0, 1, 2]
    assert history[0]["report"]["source"]["n_structures"] == 3
    selected = msm.extract(
        output["molecular_system"], selection=[1, 0], structure_indices=[2, 0]
    )
    assert selected.structures.n_structures == 2
    assert_tree(selected.chemical_states.get_preparation_history(), history)
    path = tmp_path / "selected.h5msm"
    msm.convert(selected, to_form=path)
    assert_tree(
        msm.convert(
            path, to_form="molsysmt.MolSys"
        ).chemical_states.get_preparation_history(),
        history,
    )
