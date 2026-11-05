"""Check declared group meaning across native lifecycle and lossy boundaries."""

import copy
import json

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentChoiceError, ArgumentError
from molsysmt.native import MolSys, Structures, Topology


@pytest.fixture
def source():
    system = MolSys(n_atoms=4, n_groups=4, n_chains=1, n_molecules=1, n_entities=1)
    topology = system.topology
    topology.atoms["atom_id"] = ["1", "2", "3", "4"]
    topology.atoms["atom_name"] = ["CA"] * 4
    topology.atoms["atom_type"] = ["C"] * 4
    topology.atoms["group_index"] = pd.array([2, 0, 3, 1], dtype="Int64")
    topology.atoms["chain_index"] = pd.array([0] * 4, dtype="Int64")
    topology.groups["group_name"] = ["GLH", "GLH", "GLH", "ALA"]
    topology.groups["group_id"] = ["a", "b", "c", "d"]
    topology.groups["group_type"] = ["unknown"] * 4
    topology.groups["molecule_index"] = pd.array([0] * 4, dtype="Int64")
    topology.molecules["entity_index"] = pd.array([0], dtype="Int64")
    topology.chains["chain_id"] = ["A"]
    topology.set_group_naming_schemes(["amber", "legacy", None, "sequence"])
    system.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.arange(36).reshape(3, 4, 3), "nm")
    )
    return system


def naming_issues(report):
    return [
        issue for issue in report.issues if issue.attribute == "group_naming_schemes"
    ]


@pytest.mark.parametrize(
    "target",
    [
        "file:pdb",
        "string:pdb_text",
        "openmm.Topology",
        "mdtraj.Topology",
        "molsysmt.Structures",
        "string:amino_acids_1",
    ],
)
def test_label_or_coordinate_targets_report_declared_meaning_loss(source, target):
    before = source.topology.group_naming_schemes
    report = msm.get_conversion_report(source.topology, to_form=target)
    (issue,) = naming_issues(report)
    assert issue.kind == "unsupported" and issue.scope == "topology"
    assert report.is_lossy
    assert "topology" in report.audited_scopes
    assert source.topology.group_naming_schemes == before


@pytest.mark.parametrize(
    "target",
    [
        "molsysmt.Topology",
        "molsysmt.MolSys",
        "molsysmt.TopologyDict",
        "molsysmt.MolSysDict",
        "molsysmt.MolSysBuilder",
        "file:h5msm",
    ],
)
def test_supported_native_routes_preserve_actual_declarations_and_report_no_naming_loss(
    source, target, tmp_path
):
    output_target = (
        str(tmp_path / "retained.h5msm") if target == "file:h5msm" else target
    )
    converted, report = msm.convert(source, to_form=output_target, return_report=True)
    assert not naming_issues(report)
    restored = msm.convert(converted, to_form="molsysmt.MolSys")
    assert restored.topology.group_naming_schemes == (
        "amber",
        "legacy",
        None,
        "sequence",
    )
    assert restored.topology.groups.group_name.tolist() == ["GLH", "GLH", "GLH", "ALA"]
    assert source.topology.group_naming_schemes == ("amber", "legacy", None, "sequence")


@pytest.mark.parametrize(
    "atoms,expected", [([0], False), ([3], True), ([2, 0], True), ([], False)]
)
def test_naming_loss_is_scoped_to_selected_atoms_not_the_whole_source(
    source, atoms, expected
):
    report = msm.get_conversion_report(
        source.topology, to_form="openmm.Topology", selection=atoms
    )
    assert bool(naming_issues(report)) is expected


@pytest.mark.parametrize("existing", [False, True])
def test_strict_loss_rejects_before_creating_or_replacing_a_file(
    source, tmp_path, existing
):
    filename = tmp_path / "preserve.pdb"
    if existing:
        filename.write_bytes(b"original destination")
    with pytest.raises(msm.NotCompatibleConversionError, match="group_naming_schemes"):
        msm.convert(source, to_form=filename, strict=True)
    assert filename.exists() is existing
    if existing:
        assert filename.read_bytes() == b"original destination"


def test_unknown_source_context_is_not_reported_as_a_known_declaration(source):
    source.topology.set_group_naming_schemes(None)
    assert not naming_issues(
        msm.get_conversion_report(source.topology, to_form="openmm.Topology")
    )


def test_prospective_source_declaration_is_audited_without_mutation(source, tmp_path):
    source.topology.set_group_naming_schemes(None)
    filename = tmp_path / "prospective.pdb"
    report = msm.get_conversion_report(
        source, to_form=filename, from_naming_scheme="amber"
    )
    assert naming_issues(report)
    with pytest.raises(msm.NotCompatibleConversionError, match="group_naming_schemes"):
        msm.convert(source, to_form=filename, strict=True, from_naming_scheme="amber")
    assert not filename.exists()
    assert source.topology.group_naming_schemes == (None,) * 4
    converted, written_report = msm.convert(
        source, to_form=filename, return_report=True, from_naming_scheme="amber"
    )
    assert written_report == report
    restored = msm.convert(
        converted, to_form="molsysmt.MolSys", get_missing_bonds=False
    )
    assert restored.topology.group_naming_schemes == (None,) * 4
    assert dict(
        zip(restored.topology.groups.group_id, restored.topology.groups.group_name)
    ) == {
        "a": "GLH",
        "b": "GLH",
        "c": "GLH",
        "d": "ALA",
    }


def test_preflight_and_conversion_use_the_same_conflict_scope(source):
    for operation in (msm.get_conversion_report, msm.convert):
        with pytest.raises(ArgumentError) as error:
            operation(source, to_form="molsysmt.Topology", from_naming_scheme="amber")
        assert error.value.extra["argument"] == "from_naming_scheme"
    # Atom zero belongs to the undeclared group, rather than group zero.
    result, report = msm.convert(
        source.topology,
        to_form="molsysmt.TopologyDict",
        selection=[0],
        from_naming_scheme="amber",
        strict=True,
        return_report=True,
    )
    assert not naming_issues(report)
    topology = msm.convert(result, to_form="molsysmt.Topology")
    assert topology.group_naming_schemes == ("amber",)
    assert topology.groups.group_id.tolist() == ["c"]
    assert source.topology.group_naming_schemes == ("amber", "legacy", None, "sequence")


@pytest.mark.parametrize(
    "form",
    ["molsysmt.TopologyDict", "molsysmt.MolSysDict", "molsysmt.MolSysBuilder", "file"],
)
def test_persisted_and_editable_sources_do_not_escape_the_fidelity_audit(
    source, form, tmp_path
):
    target = str(tmp_path / "source.h5msm") if form == "file" else form
    value = msm.convert(source, to_form=target)
    assert naming_issues(msm.get_conversion_report(value, to_form="openmm.Topology"))


def test_partial_system_without_topology_has_no_group_context_to_lose():
    source = MolSys._from_partial_domains(structures=Structures())
    assert not naming_issues(
        msm.get_conversion_report(source, to_form="molsysmt.Structures")
    )


@pytest.mark.parametrize("with_context", [False, True])
def test_native_composition_audits_the_actual_inventory_owner(source, with_context):
    if not with_context:
        source.topology.set_group_naming_schemes(None)
    report = msm.get_conversion_report(
        [source.topology, source.structures], to_form="string:pdb_text"
    )
    assert bool(naming_issues(report)) is with_context


@pytest.mark.parametrize("wire", ["molsysmt.MolSysDict", "file"])
def test_transport_then_reorder_preserves_context_coordinates_and_source_group_labels(
    source, wire, tmp_path
):
    target = str(tmp_path / "system.h5msm") if wire == "file" else wire
    restored = msm.convert(
        msm.convert(source, to_form=target), to_form="molsysmt.MolSys"
    )
    selected = msm.extract(restored, selection=[3, 1, 0], structure_indices=[2, 0])
    association = dict(
        zip(selected.topology.groups.group_id, selected.topology.group_naming_schemes)
    )
    assert association == {"a": "amber", "b": "legacy", "c": None}
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(selected.structures.coordinates, to_unit="nm"),
        np.arange(36).reshape(3, 4, 3)[[2, 0]][:, [0, 1, 3]],
    )
    assert source.topology.group_naming_schemes == ("amber", "legacy", None, "sequence")
    assert not naming_issues(msm.get_conversion_report(selected, to_form="file:h5msm"))


def test_atom_free_reorder_and_merge_preserves_mixed_context_across_json_wire():
    source = msm.convert("amino_acids_3:GLHGLHGLH", to_form="molsysmt.Topology")
    source.set_group_naming_schemes(["amber", "legacy", None])
    wire = msm.convert(source, to_form="molsysmt.TopologyDict")
    restored = msm.convert(
        type(wire)(json.loads(json.dumps(wire.data))), to_form="molsysmt.Topology"
    )
    selected = msm.extract(restored, element="group", selection=[2, 0])
    other = Topology(n_groups=1)
    other.groups["group_name"] = ["GLH"]
    merged = msm.merge([selected, other])
    assert merged.group_naming_schemes == (None, "amber", None)
    assert source.group_naming_schemes == ("amber", "legacy", None)


@pytest.mark.parametrize(
    "copier", [copy.copy, copy.deepcopy, lambda x: x.copy(deep=False)]
)
def test_declarations_remain_independent_during_native_system_snapshots(source, copier):
    result = copier(source)
    result.topology.set_group_naming_schemes("ccd", group_indices=[2])
    assert result.topology.group_naming_schemes == (
        "amber",
        "legacy",
        "ccd",
        "sequence",
    )
    assert source.topology.group_naming_schemes == ("amber", "legacy", None, "sequence")


@pytest.mark.parametrize("bad", ["unknown", 0, False])
def test_public_preflight_validates_its_source_context_argument(source, bad):
    with pytest.raises(ArgumentChoiceError) as error:
        msm.get_conversion_report(source, from_naming_scheme=bad)
    assert error.value.extra["argument"] == "from_naming_scheme"


@pytest.mark.parametrize("source_kind", ["structures", "partial"])
def test_missing_stable_inventory_has_an_explicit_context_diagnostic(source_kind):
    source = (
        Structures()
        if source_kind == "structures"
        else MolSys._from_partial_domains(structures=Structures())
    )
    with pytest.raises(ArgumentError) as error:
        msm.get_conversion_report(
            source, to_form="molsysmt.MolSys", from_naming_scheme="amber"
        )
    assert error.value.extra["argument"] == "from_naming_scheme"


@pytest.mark.parametrize("wire", ["molsysmt.MolSysDict", "file"])
def test_mixed_context_transport_does_not_replace_states_or_named_occurrences(
    source, wire, tmp_path
):
    source.chemical_states._states[0].state_id = "reference"
    alternate = source.chemical_states.append_state()
    source.chemical_states._states[alternate].state_id = "alternate"
    source._set_structure_chemical_state_indices([0, alternate, 0])
    analysis = msm.Interactions.from_records(
        [
            dict(
                structure_index=0,
                interaction_type="synthetic",
                participants=[
                    dict(role="a", atom_indices=[0]),
                    dict(role="b", atom_indices=[1]),
                ],
                evidence="test_fixture",
            )
        ],
        n_atoms=4,
        n_structures=3,
        evaluated_structure_indices=[0, 1],
        method="fidelity_fixture",
    )
    source.interactions = {"review": analysis}
    target = str(tmp_path / "state-analysis.h5msm") if wire == "file" else wire
    restored = msm.convert(
        msm.convert(source, to_form=target), to_form="molsysmt.MolSys"
    )
    assert restored.topology.group_naming_schemes == (
        "amber",
        "legacy",
        None,
        "sequence",
    )
    assert [s.state_id for s in restored.chemical_states._states] == [
        "reference",
        "alternate",
    ]
    np.testing.assert_array_equal(
        restored._get_structure_chemical_state_indices(), [0, alternate, 0]
    )
    received = restored.interactions["review"].query().to_dict()
    np.testing.assert_array_equal(received["occurrence_indices"], [0])
    np.testing.assert_array_equal(received["evaluated_structure_indices"], [0, 1])
    selected = msm.extract(restored, selection=[0, 1], structure_indices=[1, 0])
    assert dict(
        zip(selected.topology.groups.group_id, selected.topology.group_naming_schemes)
    ) == {"a": "amber", "c": None}
    np.testing.assert_array_equal(
        selected._get_structure_chemical_state_indices(), [alternate, 0]
    )
    selected_analysis = selected.interactions["review"].query().to_dict()
    np.testing.assert_array_equal(selected_analysis["structure_indices"], [1])
    np.testing.assert_array_equal(
        selected_analysis["evaluated_structure_indices"], [0, 1]
    )
    assert source.interactions["review"] is analysis


def test_foreign_identity_with_a_prospective_declaration_is_not_certified_as_a_byte_copy():
    source = msm.systems["caffeine"]["caffeine.sdf"]
    ordinary = msm.get_conversion_report(source, to_form="file:sdf")
    assert ordinary.is_exhaustive and ordinary.outcome == "exact"
    interpreted = msm.get_conversion_report(
        source, to_form="file:sdf", from_naming_scheme="amber"
    )
    # Native SDF inventory is group-free: no declaration is invented for it.
    assert not naming_issues(interpreted)
    assert interpreted.outcome == "equivalent" and not interpreted.is_exhaustive


def test_partial_native_inventory_has_no_mechanics_semantics_to_drop(source):
    partial = MolSys._from_partial_domains(topology=source.topology.copy())
    partial.molecular_mechanics = None
    converted, report = msm.convert(
        partial, to_form="molsysmt.MolSysDict", strict=True, return_report=True
    )
    assert not report.issues
    restored = msm.convert(converted, to_form="molsysmt.MolSys")
    assert restored.topology.group_naming_schemes == (
        "amber",
        "legacy",
        None,
        "sequence",
    )
    assert restored.chemical_states is restored.structures is None
    assert restored.molecular_mechanics.forcefield is None
    assert restored.molecular_mechanics.atom_ff_type is None


def test_foreign_pdb_identity_with_declared_context_reports_actual_metadata_loss(
    source, tmp_path
):
    filename = msm.convert(source, to_form=str(tmp_path / "source.pdb"))
    report = msm.get_conversion_report(
        filename, to_form="file:pdb", from_naming_scheme="amber"
    )
    assert naming_issues(report)
    assert report.is_lossy and not report.is_exhaustive


def test_atomic_permutation_keeps_group_context_attached_to_the_stable_axis(
    source, tmp_path
):
    permuted = msm.permute_atoms(source, [3, 1, 0, 2])
    assert permuted.topology.group_naming_schemes == (
        "amber",
        "legacy",
        None,
        "sequence",
    )
    assert permuted.topology.atoms.atom_id.tolist() == ["4", "2", "1", "3"]
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(permuted.structures.coordinates, to_unit="nm"),
        np.arange(36).reshape(3, 4, 3)[:, [3, 1, 0, 2]],
    )
    filename = msm.convert(permuted, to_form=str(tmp_path / "permuted.h5msm"))
    restored = msm.convert(filename, to_form="molsysmt.MolSys")
    assert (
        restored.topology.group_naming_schemes == permuted.topology.group_naming_schemes
    )
    assert restored.topology.atoms.atom_id.tolist() == ["4", "2", "1", "3"]


def test_non_strict_foreign_conversion_reports_loss_and_reader_keeps_unknown_context(
    source,
):
    pytest.importorskip("openmm")
    converted, report = msm.convert(
        source.topology, to_form="openmm.Topology", return_report=True
    )
    assert naming_issues(report)
    assert report == msm.get_conversion_report(
        source.topology, to_form="openmm.Topology"
    )
    restored = msm.convert(
        converted, to_form="molsysmt.Topology", get_missing_bonds=False
    )
    assert restored.group_naming_schemes == (None,) * 4
    assert dict(zip(restored.groups.group_id, restored.groups.group_name)) == {
        "a": "GLH",
        "b": "GLH",
        "c": "GLH",
        "d": "ALA",
    }
    assert source.topology.group_naming_schemes == ("amber", "legacy", None, "sequence")


def test_target_list_preflight_audits_prospective_context_in_order_without_assignment(
    source,
):
    source.topology.set_group_naming_schemes(None)
    reports = msm.get_conversion_report(
        source.topology,
        to_form=["molsysmt.TopologyDict", "openmm.Topology"],
        from_naming_scheme="amber",
    )
    assert [report.to_form for report in reports] == [
        "molsysmt.TopologyDict",
        "openmm.Topology",
    ]
    assert not naming_issues(reports[0]) and naming_issues(reports[1])
    assert source.topology.group_naming_schemes == (None,) * 4


@pytest.mark.parametrize("domain", ["topology", "structures"])
def test_pdb_preflight_inspects_only_the_domains_present_in_a_partial_system(
    source, domain
):
    partial = MolSys._from_partial_domains(**{domain: getattr(source, domain).copy()})
    report = msm.get_conversion_report(partial, to_form="string:pdb_text")
    assert bool(naming_issues(report)) is (domain == "topology")
    assert partial.chemical_states is None
    assert (
        getattr(partial, "structures" if domain == "topology" else "topology") is None
    )


def evaluated_empty(source, evaluated):
    source.interactions = {
        "empty": msm.Interactions.from_records(
            [],
            n_atoms=4,
            n_structures=3,
            evaluated_structure_indices=evaluated,
            method="evaluated_empty_fidelity_fixture",
        )
    }
    return source.interactions["empty"]


@pytest.mark.parametrize("form", ["native", "dictionary"])
@pytest.mark.parametrize("target", ["molsysmt.MolSys", "molsysmt.MolSysDict", "file"])
def test_prospective_context_invalidation_is_reported_before_target_publication(
    source, form, target, tmp_path
):
    source.topology.set_group_naming_schemes(None)
    snapshot = evaluated_empty(source, [0, 1])
    value = (
        source
        if form == "native"
        else msm.convert(source, to_form="molsysmt.MolSysDict")
    )
    destination = str(tmp_path / "changed.h5msm") if target == "file" else target
    report = msm.get_conversion_report(
        value, to_form=destination, from_naming_scheme="amber"
    )
    (issue,) = [item for item in report.issues if item.attribute == "interactions"]
    assert issue.kind == "invalidation" and issue.scope == "interactions"
    with pytest.raises(msm.NotCompatibleConversionError, match="interactions"):
        msm.convert(value, to_form=destination, strict=True, from_naming_scheme="amber")
    assert not (tmp_path / "changed.h5msm").exists()
    result, conversion_report = msm.convert(
        value, to_form=destination, return_report=True, from_naming_scheme="amber"
    )
    assert conversion_report == report
    restored = msm.convert(result, to_form="molsysmt.MolSys")
    assert restored.interactions["empty"].evaluated_structure_indices.size == 0
    assert source.interactions["empty"] is snapshot
    np.testing.assert_array_equal(snapshot.evaluated_structure_indices, [0, 1])
    assert source.topology.group_naming_schemes == (None,) * 4


@pytest.mark.parametrize(
    "mode", ["matching_context", "unevaluated", "unselected_structures"]
)
def test_no_reported_invalidation_without_loss_of_selected_evaluated_coverage(
    source, mode
):
    source.topology.set_group_naming_schemes(
        "amber" if mode == "matching_context" else None
    )
    evaluated_empty(source, [] if mode == "unevaluated" else [0])
    structures = [2] if mode == "unselected_structures" else "all"
    report = msm.get_conversion_report(
        source,
        to_form="molsysmt.MolSys",
        from_naming_scheme="amber",
        structure_indices=structures,
    )
    assert not [item for item in report.issues if item.attribute == "interactions"]
    result = msm.convert(
        source,
        to_form="molsysmt.MolSys",
        from_naming_scheme="amber",
        strict=True,
        structure_indices=structures,
    )
    expected = [0] if mode == "matching_context" else []
    np.testing.assert_array_equal(
        result.interactions["empty"].evaluated_structure_indices, expected
    )


@pytest.mark.parametrize(
    "target",
    [
        "molsysmt.Topology",
        "molsysmt.TopologyDict",
        "molsysmt.MolSysBuilder",
        "molsysmt.Structures",
    ],
)
def test_named_analysis_projection_is_an_explicit_loss_even_for_empty_results(
    source, target
):
    evaluated_empty(source, [])
    report = msm.get_conversion_report(source, to_form=target)
    (issue,) = [item for item in report.issues if item.attribute == "interactions"]
    assert issue.kind == "unsupported" and issue.scope == "interactions"
    with pytest.raises(msm.NotCompatibleConversionError, match="interactions"):
        msm.convert(source, to_form=target, strict=True)


def test_dictionary_preflight_reads_coverage_without_decoding_occurrence_columns(
    source, monkeypatch
):
    source.topology.set_group_naming_schemes(None)
    evaluated_empty(source, [0])
    wire = msm.convert(source, to_form="molsysmt.MolSysDict")
    from molsysmt._private.naming_fidelity import analysis_metadata
    from molsysmt.form import _serialization

    original = _serialization.decode_array

    def coverage_only(payload):
        assert payload["shape"] == [1]
        return original(payload)

    monkeypatch.setattr(_serialization, "decode_array", coverage_only)
    names, affected = analysis_metadata(wire, [0], coverage=True)
    assert names == ("empty",) and affected
