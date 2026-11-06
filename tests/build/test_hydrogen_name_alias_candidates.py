"""Qualifying explicit H-name alternatives without changing chemical identity."""

import builtins
from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from tests.build.test_get_covalent_bond_candidates import _hydrogen_source, _source

METHOD = "observed_hydrogen_alias_consensus"
APPLICATION = "supported_group_templates_with_hydrogen_aliases"


def test_opt_in_alias_parents_preserve_literal_names_geometry_and_default():
    source = _hydrogen_source(("HN1", "1HB", "XX"))
    before = source.topology.atoms.copy(deep=True)
    coordinates = msm.pyunitwizard.get_value(
        source.structures.coordinates, to_unit="nm"
    ).copy()
    exact = msm.build.get_covalent_bond_candidates(
        source, method="observed_hydrogen_template_consensus"
    )
    assert exact["bonded_atom_pairs"].tolist() == [[4, 6]]
    result = msm.build.get_covalent_bond_candidates(source, method=METHOD)
    assert result["bonded_atom_pairs"].tolist() == [[0, 5], [4, 6]]
    h = result["groups"][0]["hydrogen_coverage"]
    assert h["parent_atom_indices"].tolist() == [0, 4, -1]
    assert h["alias_mask"].tolist() == [True, True, False]
    assert h["reference_name_offsets"].tolist() == [0, 2, 4, 5]
    assert h["reference_names"].tolist() == ["HN1", "H", "1HB", "HB1", "XX"]
    assert h["inventory_status"] == "unassessed"
    assert h["joint_variant_indices"].size == 0
    assert (
        result["hydrogen_name_policy"]["reference"]["sha256"]
        == "740c56071d092940ce386074447ce88ed2b07c77d0065f2bd0d1087e9ef76969"
    )
    assert result["hydrogen_name_policy"]["references"][0]["type"] == "dataset"
    pd.testing.assert_frame_equal(source.topology.atoms, before)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"),
        coordinates,
    )
    assert source.chemical_states.get_bonds().empty


@pytest.mark.parametrize(
    "selection,expected", [([0, 5], [[0, 5]]), ([5], []), ([], [])]
)
def test_alias_candidates_require_both_endpoints_in_original_selection(
    selection, expected
):
    result = msm.build.get_covalent_bond_candidates(
        _hydrogen_source(("HN1",)), selection=selection, method=METHOD
    )
    assert result["bonded_atom_pairs"].tolist() == expected
    assert result["bonded_atom_pairs"].shape == (len(expected), 2)


def test_applied_alias_policy_is_explicit_and_history_roundtrips(tmp_path):
    source = _hydrogen_source(("HN1",))
    exact = msm.build.infer_covalent_bonds(source)
    assert len(exact.chemical_states.get_bonds()) == 4
    result = msm.build.infer_covalent_bonds(
        source, method=APPLICATION, return_report=True
    )
    output = result["molecular_system"]
    assert len(output.chemical_states.get_bonds()) == 5
    assert result["report"]["method"] == APPLICATION
    assert result["report"]["candidate_methods"][1] == METHOD
    assert result["report"]["hydrogen_name_policy"]["reference"]["sha256"]
    filename = tmp_path / "aliases.h5msm"
    msm.convert(output, to_form=str(filename))
    loaded = msm.convert(filename)
    report = loaded.chemical_states.get_preparation_history()[0]["report"]
    assert report["method"] == APPLICATION
    assert report["hydrogen_name_policy"] == result["report"]["hydrogen_name_policy"]
    assert source.chemical_states.get_bonds().empty


def test_alias_data_is_not_an_openmm_dependency(monkeypatch):
    original = builtins.__import__

    def block(name, *args, **kwargs):
        if name == "openmm" or name.startswith("openmm."):
            pytest.fail("Name-reference lookup imported the OpenMM engine")
        return original(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", block)
    result = msm.build.get_covalent_bond_candidates(
        _hydrogen_source(("HN1",)), method=METHOD
    )
    assert result["bonded_atom_pairs"].tolist() == [[0, 5]]


def test_alias_policy_preserves_declared_partner_conflicts():
    source = _hydrogen_source(("HN1",))
    source.chemical_states.add_bonds([[4, 5]])
    result = msm.build.get_covalent_bond_candidates(source, method=METHOD)
    assert result["bonded_atom_pairs"].tolist() == []
    assert (
        "conflicting_stored_hydrogen_partner"
        in result["groups"][0]["hydrogen_coverage"]["issues"][0]["reason_codes"]
    )


def test_distinct_reference_parents_block_alias_consensus(monkeypatch):
    from molsysmt._private import residue_chemical_coverage as owner

    original = owner._template

    def conflicting(*args, **kwargs):
        data = deepcopy(original(*args, **kwargs))
        for _, variant in data["candidates"]:
            if "H" in variant["atoms"]:
                variant["bonds"] = [
                    pair for pair in variant["bonds"] if "H" not in pair
                ] + [["H", "CB"]]
                break
        return data

    monkeypatch.setattr(owner, "_template", conflicting)
    result = msm.build.get_covalent_bond_candidates(
        _hydrogen_source(("HN1",)), method=METHOD
    )
    assert result["bonded_atom_pairs"].tolist() == []
    assert (
        "ambiguous_hydrogen_parent"
        in result["groups"][0]["hydrogen_coverage"]["issues"][0]["reason_codes"]
    )


def test_reference_group_aliases_do_not_reinterpret_amber_or_ccd_group_names():
    names = msm.element.group.amino_acid.get_expected_heavy_atoms(
        "HID", naming_scheme="amber"
    )
    names = list(names) + ["H", "HN"]
    source = _source(
        [
            (
                "HID",
                names,
                [msm.element.atom.get_atom_type_from_atom_name(name) for name in names],
            )
        ]
    )
    source.topology.set_group_naming_schemes(["amber"])
    parent = names.index("N")
    result = msm.build.get_covalent_bond_candidates(source, method=METHOD)
    assert result["bonded_atom_pairs"].tolist() == [sorted([parent, len(names) - 2])]
    assert result["groups"][0]["template"]["naming_scheme"] == "amber"
    assert result["groups"][0]["hydrogen_coverage"]["alias_mask"].tolist() == [
        False,
        False,
    ]
    assert result["groups"][0]["hydrogen_coverage"]["parent_atom_indices"].tolist() == [
        parent,
        -1,
    ]
    assert source.topology.groups["group_name"].tolist() == ["HID"]


def test_missing_source_names_do_not_become_literal_none_reference_labels():
    source = _hydrogen_source(("HN1",))
    source.topology.atoms.loc[5, "atom_name"] = None
    result = msm.build.get_covalent_bond_candidates(source, method=METHOD)
    h = result["groups"][0]["hydrogen_coverage"]
    assert result["bonded_atom_pairs"].tolist() == []
    assert h["reference_name_offsets"].tolist() == [0, 0]
    assert h["reference_names"].size == 0


def test_real_ackredit_captures_reused_dataset_without_claiming_engine_execution():
    ackredit = pytest.importorskip("ackredit")
    source = _hydrogen_source(("HN1",))
    captured = []
    with ackredit.session("H name reference receiving"):
        for index in range(2):
            with ackredit.capture(str(index)) as capture:
                report = msm.build.get_covalent_bond_candidates(source, method=METHOD)
            items = capture.attribution.to_dict()["items"]
            actual = [
                item
                for item in items
                if item["id"].startswith("dataset:openmm-pdb-hydrogen-aliases:")
            ]
            assert len(actual) == 1
            assert actual[0]["type"] == "dataset"
            assert (
                actual[0]["version"]
                == report["hydrogen_name_policy"]["reference"]["commit"]
            )
            captured.append(actual)
    assert captured[0] == captured[1]
    report["hydrogen_name_policy"]["reference"]["title"] = "changed by consumer"
    fresh = msm.build.get_covalent_bond_candidates(source, method=METHOD)
    assert fresh["hydrogen_name_policy"]["reference"]["title"] != "changed by consumer"


def test_absent_attribution_provider_preserves_candidates_and_detached_references(
    monkeypatch,
):
    from molsysmt import _ackredit

    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    result = msm.build.get_covalent_bond_candidates(
        _hydrogen_source(("HN1",)), method=METHOD
    )
    assert result["bonded_atom_pairs"].tolist() == [[0, 5]]
    assert result["hydrogen_name_policy"]["references"][0]["type"] == "dataset"


def test_no_alias_reference_is_credited_when_no_selected_hydrogen_is_examined():
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("no H lookup"):
        with ackredit.capture("empty") as capture:
            report = msm.build.get_covalent_bond_candidates(
                _hydrogen_source(("HN1",)), selection=[], method=METHOD
            )
        assert not any(
            item["id"].startswith("dataset:openmm-pdb-hydrogen-aliases:")
            for item in capture.attribution.to_dict()["items"]
        )
    assert report["hydrogen_name_policy"]["reference"] is None


def test_provider_failure_warns_without_replacing_completed_parent_candidates(
    monkeypatch,
):
    from contextlib import nullcontext

    from molsysmt import _ackredit
    from molsysmt._private.smonitor.warnings import AckreditTrackingWarning

    class UnavailableRecorder:
        def scope(self, *args, **kwargs):
            return nullcontext()

        def register_item(self, **kwargs):
            raise RuntimeError("unavailable recorder control")

    monkeypatch.setattr(_ackredit, "backend", lambda: UnavailableRecorder())
    with pytest.warns(AckreditTrackingWarning):
        report = msm.build.get_covalent_bond_candidates(
            _hydrogen_source(("HN1",)), method=METHOD
        )
    assert report["bonded_atom_pairs"].tolist() == [[0, 5]]
    assert report["hydrogen_name_policy"]["references"]


def test_named_state_and_nondefault_units_preserve_all_source_structures():
    source = _hydrogen_source(("HN1",), n_structures=3)
    source.chemical_states.append_state()
    msm.set(source, structure_chemical_state_index=[0, 1, None])
    before = msm.pyunitwizard.get_value(
        source.structures.coordinates, to_unit="nm"
    ).copy()
    with msm.pyunitwizard.context(standard_units=["pm", "fs"]):
        result = msm.build.infer_covalent_bonds(
            source,
            method=APPLICATION,
            chemical_state="structure",
            structure_indices=1,
            return_report=True,
        )
    output = result["molecular_system"]
    assert output.structures.n_structures == 3
    assert output.chemical_states.get_bonds(chemical_state=0).empty
    assert len(output.chemical_states.get_bonds(chemical_state=1)) == 5
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(output.structures.coordinates, to_unit="nm"), before
    )
    assert source.chemical_states.get_bonds(chemical_state=1).empty
