"""Reconstruction evidence must identify insertions without downstream matching."""

import gzip
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.preparation_history import append_report
from molsysmt._private.smonitor import (
    ArgumentError,
    NotImplementedMethodError,
    StructuralAttributeDropWarning,
    StructuralInconsistencyError,
    UnassessedPeptideBackboneWarning,
    UnassessedResidueWarning,
)


@pytest.fixture(scope="module")
def two_chains():
    peptide = msm.build.build_peptide("AA", engine="MolSysMT")
    peptide = msm.remove(peptide, selection='atom_type=="H" or atom_name=="OXT"')
    source = msm.merge([peptide, peptide], keep_ids=False)
    source.molecular_mechanics = None
    assert source.get_n_atoms() == 20
    return source


def same_tree(actual, expected):
    if isinstance(expected, np.ndarray):
        np.testing.assert_array_equal(actual, expected)
        assert actual.dtype == expected.dtype
    elif isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for key in expected:
            same_tree(actual[key], expected[key])
    elif isinstance(expected, (list, tuple)):
        assert len(actual) == len(expected)
        for left, right in zip(actual, expected):
            same_tree(left, right)
    else:
        assert actual == expected


def assert_observed_geometry(source, output, report):
    mapping = report["source_to_output_atom_indices"]
    assert mapping.dtype == np.int64
    np.testing.assert_array_equal(
        puw.get_value(output.structures.coordinates, to_unit="nm")[:, mapping],
        puw.get_value(source.structures.coordinates, to_unit="nm"),
    )
    inverse = report["output_to_source_atom_indices"]
    np.testing.assert_array_equal(inverse[mapping], np.arange(source.get_n_atoms()))
    assert np.all(inverse[report["generated_atom_indices"]] == -1)


@pytest.mark.parametrize("unit", ["nm", "angstrom"])
def test_exact_multichain_map_preserves_both_structures_and_source(two_chains, unit):
    source = msm.append_structures(two_chains, two_chains, in_place=False)
    source.structures.coordinates = puw.convert(
        source.structures.coordinates, to_unit=unit
    )
    before = source.copy()
    result = msm.build.add_missing_terminal_cappings(source, return_report=True)
    output, report = result["molecular_system"], result["report"]
    assert report["schema"] == "molsysmt.terminal_completion@1"
    np.testing.assert_array_equal(
        report["source_to_output_atom_indices"], np.r_[np.arange(10), np.arange(11, 21)]
    )
    np.testing.assert_array_equal(report["generated_atom_indices"], [10, 21])
    np.testing.assert_array_equal(report["structure_indices"], [0, 1])
    assert report["bond_index_scope"] == "output"
    np.testing.assert_array_equal(
        report["introduced_bond_atom_pairs"], [[8, 10], [19, 21]]
    )
    assert report["coordinate_unit"] == "nm"
    assert report["complete_chemical_state_assigned"] is False
    assert_observed_geometry(source, output, report)
    pd.testing.assert_frame_equal(source.topology.atoms, before.topology.atoms)
    same_tree(
        source.chemical_states.get_preparation_history(),
        before.chemical_states.get_preparation_history(),
    )
    np.testing.assert_array_equal(
        puw.get_value(source.structures.coordinates),
        puw.get_value(before.structures.coordinates),
    )


def test_substeps_compose_heavy_repair_and_cap_new_to_new_bonds(two_chains):
    source = msm.remove(two_chains, selection='group_index==0 and atom_name=="CB"')
    result = msm.build.add_missing_terminal_cappings(
        source, N_terminal="ACE", C_terminal="NME", return_report=True
    )
    output, report = result["molecular_system"], result["report"]
    assert [step["method"] for step in report["steps"]] == [
        "native_heavy_atom_completion",
        "native_planar_terminal_caps",
    ]
    assert report["steps"][0]["generated_atom_indices"].size == 1
    assert_observed_geometry(source, output, report)
    generated = set(report["generated_atom_indices"])
    assert any(
        a in generated and b in generated
        for a, b in report["introduced_bond_atom_pairs"]
    )
    evidence = report["steps"][0]["steps"][0]["coordinate_evidence"][0]
    assert evidence["template"]["name"] == "ALA"
    assert len(evidence["template"]["sha256"]) == 64
    assert evidence["anchor_atom_names"]["CB"]
    assert report["references"][0]["doi"] == "10.1364/JOSAA.4.000629"
    mapped = msm.basic.compose_atom_maps([report])
    np.testing.assert_array_equal(
        mapped["source_to_output_atom_indices"], report["source_to_output_atom_indices"]
    )
    assert set(mapped["generated_output_atom_indices"]) == generated


def test_selected_source_groups_do_not_complete_other_chain(two_chains):
    result = msm.build.add_missing_terminal_cappings(
        two_chains, selection=[7, 5], return_report=True
    )
    report = result["report"]
    np.testing.assert_array_equal(report["selected_source_atom_indices"], [7, 5])
    np.testing.assert_array_equal(report["selected_source_group_indices"], [1])
    np.testing.assert_array_equal(report["generated_atom_indices"], [10])
    assert result["molecular_system"].get_n_atoms() == 21
    assert_observed_geometry(two_chains, result["molecular_system"], report)


@pytest.mark.parametrize("caps", [False, True])
def test_strict_rejects_actual_attribute_loss_and_keeps_source(two_chains, caps):
    source = two_chains.copy()
    source.structures.occupancy = np.ones((1, 20))
    kwargs = dict(N_terminal="ACE", C_terminal="NME") if caps else {}
    with pytest.raises(StructuralInconsistencyError):
        msm.build.add_missing_terminal_cappings(
            source, attribute_policy="strict", return_report=True, **kwargs
        )
    assert source.get_n_atoms() == 20
    assert source.structures.occupancy.shape == (1, 20)
    with pytest.warns(StructuralAttributeDropWarning):
        result = msm.build.add_missing_terminal_cappings(
            source, return_report=True, **kwargs
        )
    assert result["report"]["dropped_attributes"] == ["occupancy"]
    assert result["molecular_system"].structures.occupancy is None


@pytest.mark.parametrize("selection", [[], 'group_name=="ABSENT"'])
def test_empty_selection_has_identity_maps_and_its_own_history(two_chains, selection):
    result = msm.build.add_missing_terminal_cappings(
        two_chains, selection=selection, return_report=True
    )
    assert result["molecular_system"] is not two_chains
    report = result["report"]
    assert report["status"] == "unchanged"
    assert report["coordinate_evidence"] == "not_generated"
    assert report["generated_atom_indices"].shape == (0,)
    assert report["introduced_bond_atom_pairs"].shape == (0, 2)
    assert report["steps"] == []
    np.testing.assert_array_equal(
        report["source_to_output_atom_indices"], np.arange(20)
    )
    same_tree(
        result["molecular_system"].chemical_states.get_preparation_history()[-1][
            "report"
        ],
        report,
    )


def test_history_is_detached_and_persists_with_original_operation_axes(
    two_chains, tmp_path
):
    source = msm.append_structures(two_chains, two_chains, in_place=False)
    append_report(
        source.chemical_states._states[0],
        dict(schema="other.operation@9", note="keep me"),
        0,
    )
    before = deepcopy(source.chemical_states.get_preparation_history())
    result = msm.build.add_missing_terminal_cappings(source, return_report=True)
    output, report = result["molecular_system"], result["report"]
    history = output.chemical_states.get_preparation_history()
    same_tree(history[: len(before)], before)
    same_tree(history[-1]["report"], report)
    path = tmp_path / "completion.h5msm"
    msm.convert(output, to_form=str(path))
    restored = msm.convert(path)
    same_tree(restored.chemical_states.get_preparation_history(), history)
    extracted = msm.extract(restored, selection=[21, 10, 1], structure_indices=[1, 0])
    same_tree(extracted.chemical_states.get_preparation_history(), history)
    report["source_to_output_atom_indices"][:] = -1
    same_tree(output.chemical_states.get_preparation_history(), history)
    same_tree(source.chemical_states.get_preparation_history(), before)


def test_native_report_is_available_for_dictionary_input(two_chains):
    source = msm.convert(two_chains, to_form="molsysmt.MolSysDict")
    result = msm.build.add_missing_terminal_cappings(source, return_report=True)
    assert msm.get_form(result["molecular_system"]) == "molsysmt.MolSys"
    assert_observed_geometry(two_chains, result["molecular_system"], result["report"])
    assert (
        msm.get_form(msm.build.add_missing_terminal_cappings(source))
        == "molsysmt.MolSysDict"
    )


@pytest.mark.parametrize(
    "kwargs", [{"return_report": 1}, {"attribute_policy": "invent"}]
)
def test_new_arguments_use_public_validation(two_chains, kwargs):
    with pytest.raises(ArgumentError):
        msm.build.add_missing_terminal_cappings(two_chains, **kwargs)


@pytest.mark.parametrize(
    "function", ["add_missing_terminal_cappings", "add_missing_heavy_atoms"]
)
def test_external_report_is_rejected_before_provider_execution(two_chains, function):
    with pytest.raises(NotImplementedMethodError):
        getattr(msm.build, function)(two_chains, engine="PDBFixer", return_report=True)


def test_report_maps_reject_misdeclared_generation_and_bond_axes(two_chains):
    report = msm.build.add_missing_terminal_cappings(two_chains, return_report=True)[
        "report"
    ]
    for field, value in [
        ("generated_atom_indices", np.array([0, 21])),
        ("introduced_bond_atom_pairs", np.array([[0, 99]])),
        ("bond_index_scope", "source"),
    ]:
        invalid = deepcopy(report)
        invalid[field] = value
        with pytest.raises(StructuralInconsistencyError):
            msm.basic.compose_atom_maps([invalid])


@pytest.mark.parametrize("pH,n_hydrogens", [(7.4, 2), (10.0, 1)])
def test_terminal_hydrogen_stage_records_actual_rule_and_map(pH, n_hydrogens):
    source = msm.build.build_peptide("AA", engine="MolSysMT")
    source.molecular_mechanics = None
    result = msm.build.add_missing_terminal_cappings(source, pH=pH, return_report=True)
    output, report = result["molecular_system"], result["report"]
    assert len(report["generated_atom_indices"]) == 1 + n_hydrogens
    evidence = report["steps"][-1]["coordinate_evidence"][0]
    assert len(evidence["generated_atom_names"]) == n_hydrogens
    assert evidence["bond_length_nm"] == 0.101
    assert evidence["pH_charge_threshold"] == 9.6
    assert report["references"] == []
    assert_observed_geometry(source, output, report)
    again = msm.build.add_missing_terminal_cappings(output, pH=pH, return_report=True)
    assert again["report"]["status"] == "unchanged"
    assert_observed_geometry(output, again["molecular_system"], again["report"])


def test_repair_report_retains_unassessed_reason():
    source = msm.build.build_peptide("AV", engine="MolSysMT")
    source = msm.remove(
        source, selection='group_index==1 and atom_name in ["CG1", "CG2"]'
    )
    with pytest.warns(UnassessedResidueWarning):
        result = msm.build.add_missing_heavy_atoms(source, return_report=True)
    report = result["report"]
    assert report["status"] == "unchanged"
    assert report["unassessed"][0]["group_index"] == 1
    assert "multiple missing side-chain" in report["unassessed"][0]["reason"]
    assert report["references"] == []


def test_optional_attribution_credits_only_executed_fit(two_chains, monkeypatch):
    from molsysmt import _ackredit

    class Provider:
        def __init__(self):
            self.tracked = []

        def register_item(self, **record):
            pass

        def track_item(self, identity, **context):
            self.tracked.append(identity)

        def scope(self, target):
            from contextlib import nullcontext

            return nullcontext()

    provider = Provider()
    monkeypatch.setattr(_ackredit, "backend", lambda: provider)
    msm.build.add_missing_terminal_cappings(two_chains, return_report=True)
    assert not any(identity.startswith("doi:") for identity in provider.tracked)
    source = msm.remove(two_chains, selection='group_index==0 and atom_name=="CB"')
    result = msm.build.add_missing_terminal_cappings(source, return_report=True)
    assert "doi:10.1364/JOSAA.4.000629" in provider.tracked
    assert result["report"]["references"][0]["roles"] == ["scientific_criterion"]


def test_actual_expansion_invalidates_named_analysis_but_noop_retains_coverage(
    two_chains,
):
    source = two_chains.copy()
    source.interactions = dict(
        example=msm.Interactions.from_records(
            [],
            n_atoms=20,
            n_structures=1,
            evaluated_structure_indices=[0],
            method="test",
        )
    )
    result = msm.build.add_missing_terminal_cappings(source, return_report=True)
    assert result["report"]["invalidated_interactions"] == ["example"]
    analysis = result["molecular_system"].interactions["example"]
    assert analysis.n_atoms == 22
    assert analysis.evaluated_structure_indices.tolist() == []
    assert source.interactions["example"].evaluated_structure_indices.tolist() == [0]
    noop = msm.build.add_missing_terminal_cappings(
        source, selection=[], return_report=True
    )
    assert noop["report"]["invalidated_interactions"] == []
    assert noop["molecular_system"].interactions[
        "example"
    ].evaluated_structure_indices.tolist() == [0]


@pytest.mark.parametrize("infer_connectivity", [False, True])
def test_original_1hsg_separates_backbone_context_from_generation_evidence(
    tmp_path, infer_connectivity
):
    fixture = Path(__file__).with_name("data") / "1hsg.pdb.gz"
    original = gzip.decompress(fixture.read_bytes())
    assert (
        sha256(original).hexdigest()
        == "d430675c358060808ef614002cfdcfcfa824714d89f1240adf5749d2ba60fed2"
    )
    path = tmp_path / "1hsg.pdb"
    path.write_bytes(original)
    source = msm.convert(path, get_missing_bonds=False)
    source = msm.extract(source, selection='group_type=="amino acid"')
    if infer_connectivity:
        source = msm.build.infer_covalent_bonds(source, structure_indices=0)
    before = deepcopy(source.chemical_states.get_preparation_history())
    expected_warning = (
        StructuralAttributeDropWarning
        if infer_connectivity
        else UnassessedPeptideBackboneWarning
    )
    with pytest.warns(expected_warning):
        result = msm.build.add_missing_terminal_cappings(
            source, keep_ids=True, return_report=True
        )
    output, report = result["molecular_system"], result["report"]
    assert source.get_n_atoms() == 1514
    assert_observed_geometry(source, output, report)
    same_tree(output.chemical_states.get_preparation_history()[: len(before)], before)
    same_tree(source.chemical_states.get_preparation_history(), before)
    if infer_connectivity:
        assert output.get_n_atoms() == 1516
        np.testing.assert_array_equal(report["generated_atom_indices"], [757, 1515])
        np.testing.assert_array_equal(
            report["source_to_output_atom_indices"],
            np.r_[np.arange(757), np.arange(758, 1515)],
        )
        assert report["dropped_attributes"] == ["b_factor", "occupancy"]
    else:
        assert output.get_n_atoms() == 1514
        assert report["status"] == "unchanged"
        assert [entry["chain_index"] for entry in report["unassessed"]] == [0, 1]
        assert all(
            "stored N-CA-C backbone bonds" in entry["reason"]
            for entry in report["unassessed"]
        )
    assert path.read_bytes() == original


def test_default_unchanged_multistate_copy_does_not_require_report_support(two_chains):
    source = msm.build.add_missing_terminal_cappings(two_chains)
    source.chemical_states._append_state(source.chemical_states._states[0].copy())
    result = msm.build.add_missing_terminal_cappings(source)
    assert result is not source
    assert result.chemical_states.n_chemical_states == 2
    assert result.get_n_atoms() == source.get_n_atoms()
    np.testing.assert_array_equal(
        puw.get_value(result.structures.coordinates),
        puw.get_value(source.structures.coordinates),
    )
    with pytest.raises(StructuralInconsistencyError, match="one chemical state"):
        msm.build.add_missing_terminal_cappings(source, return_report=True)


@pytest.mark.parametrize("return_report", [False, True])
@pytest.mark.parametrize(
    "argument, cap",
    [
        ("C_terminal", "NH2"),
        ("C_terminal", "NHE"),
        ("C_terminal", "ACE"),
        ("N_terminal", "NME"),
        ("C_terminal", "ALA"),
        ("N_terminal", "ALA"),
        ("N_terminal", "ace"),
        ("C_terminal", "unknown"),
    ],
)
def test_native_rejects_unsupported_cap_requests(
    two_chains, return_report, argument, cap
):
    before = two_chains.copy()
    with pytest.raises(NotImplementedMethodError, match=f"{argument}={cap!r}"):
        msm.build.add_missing_terminal_cappings(
            two_chains, return_report=return_report, **{argument: cap}
        )
    pd.testing.assert_frame_equal(two_chains.topology.atoms, before.topology.atoms)
    np.testing.assert_array_equal(
        puw.get_value(two_chains.structures.coordinates),
        puw.get_value(before.structures.coordinates),
    )
    same_tree(
        two_chains.chemical_states.get_preparation_history(),
        before.chemical_states.get_preparation_history(),
    )


@pytest.mark.parametrize("selection", ["all", []])
@pytest.mark.parametrize("skip_digestion", [False, True])
@pytest.mark.parametrize("return_report", [False, True])
def test_unsupported_cap_refuses_before_selection_copy_or_reconstruction(
    two_chains, monkeypatch, selection, skip_digestion, return_report
):
    def unexpected_work(*args, **kwargs):
        pytest.fail("Unsupported capping must be refused before resolving the system.")

    monkeypatch.setattr(msm.basic, "select", unexpected_work)
    monkeypatch.setattr(msm.basic, "copy", unexpected_work)
    with pytest.raises(NotImplementedMethodError, match="C_terminal='NH2'"):
        msm.build.add_missing_terminal_cappings(
            two_chains,
            N_terminal="ACE",
            C_terminal="NH2",
            selection=selection,
            skip_digestion=skip_digestion,
            return_report=return_report,
        )


def test_native_cap_profile_does_not_restrict_pdbfixer_delegation(two_chains, monkeypatch):
    class ProviderConversionReached(Exception):
        pass

    def stop_conversion(molecular_system, to_form, **kwargs):
        assert molecular_system is two_chains
        assert to_form == "pdbfixer.PDBFixer"
        raise ProviderConversionReached

    monkeypatch.setattr(msm.basic, "convert", stop_conversion)
    with pytest.raises(ProviderConversionReached):
        msm.build.add_missing_terminal_cappings(
            two_chains, C_terminal="NH2", engine="PDBFixer"
        )
