"""Protecting read-only protonation decisions and prepublication atom maps."""

import copy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentConflictError, ArgumentError


@pytest.fixture(scope="module")
def reference():
    return msm.convert(
        msm.systems["chicken villin HP35"]["1vii.pdb"],
        to_form="molsysmt.MolSys",
        structure_indices=[0, 0, 0],
    )


@pytest.fixture
def native(reference):
    return reference.copy()


def _unchanged(source, before):
    for name in ("atoms", "groups", "chains", "molecules", "entities"):
        pd.testing.assert_frame_equal(
            getattr(source.topology, name), getattr(before.topology, name)
        )
    assert source.chemical_states._inventory_equals(before.chemical_states)
    np.testing.assert_array_equal(
        puw.get_value(source.structures.coordinates, to_unit="nm"),
        puw.get_value(before.structures.coordinates, to_unit="nm"),
    )
    assert source.molecular_mechanics.to_dict() == before.molecular_mechanics.to_dict()


def test_assessment_is_read_only_and_maps_source_indices(native):
    before = copy.deepcopy(native)
    plan = msm.build.assess_protonation(native, pH=12.0)
    assert isinstance(plan, msm.build.ProtonationAssessment)
    report = plan.to_dict()
    assert report["schema"] == "molsysmt.protonation_assessment@1"
    assert report["status"] == "removal_required"
    assert report["parameters"]["pH"] == 12.0
    removed = report["removed_atom_indices"]
    assert len(removed) == 6
    assert native.topology.atoms.iloc[removed]["atom_name"].tolist().count("HZ3") == 5
    keep = report["atom_map"]["output_to_source_atom_indices"]
    reverse = report["atom_map"]["source_to_output_atom_indices"]
    assert keep.dtype == reverse.dtype == np.dtype("int64")
    assert keep.shape == (590,) and reverse.shape == (596,)
    assert np.all(np.diff(keep) > 0)
    np.testing.assert_array_equal(reverse[keep], np.arange(590))
    np.testing.assert_array_equal(reverse[removed], -np.ones(6, dtype=np.int64))
    np.testing.assert_array_equal(report["structure_indices"], [0, 1, 2])
    _unchanged(native, before)


def test_execution_reuses_the_exact_decision_without_reference_queries(
    native, monkeypatch
):
    plan = msm.build.assess_protonation(native, pH=12.0)
    keep = plan.to_dict()["atom_map"]["output_to_source_atom_indices"]
    coordinates = puw.get_value(native.structures.coordinates, to_unit="nm").copy()
    import molsysmt.build._protonation as criteria

    def forbidden(*args, **kwargs):
        pytest.fail(
            "Applying a prepared assessment must not repeat protonation inference"
        )

    monkeypatch.setattr(criteria, "get_expected_hydrogens", forbidden)
    output = plan.apply(native)
    assert output is not native
    assert output.get(n_atoms=True) == 590
    np.testing.assert_array_equal(
        puw.get_value(output.structures.coordinates, to_unit="nm"), coordinates[:, keep]
    )
    assert native.get(n_atoms=True) == 596
    assert plan.to_dict()["execution"]["status"] == "applied"
    with pytest.raises(ArgumentConflictError, match="consumed"):
        plan.apply(native)


def test_independent_noop_is_a_real_copy_and_inplace_noop_keeps_domains(native):
    plan = msm.build.assess_protonation(native, pH=7.4)
    assert plan.to_dict()["status"] == "no_change"
    independent = plan.apply(native)
    assert independent is not native
    assert independent.topology is not native.topology
    assert not np.shares_memory(
        puw.get_value(independent.structures.coordinates),
        puw.get_value(native.structures.coordinates),
    )
    domains = native.topology, native.chemical_states, native.structures
    plan = msm.build.assess_protonation(native, pH=7.4)
    assert plan.apply(native, in_place=True) is None
    assert (native.topology, native.chemical_states, native.structures) == domains


@pytest.mark.parametrize("edit", ["name", "naming", "bonds", "structures", "identity"])
@pytest.mark.parametrize("skip_digestion", [False, True])
def test_stale_or_foreign_source_is_rejected_before_removal(
    native, edit, skip_digestion, monkeypatch
):
    plan = msm.build.assess_protonation(native, pH=12.0)
    target = native
    if edit == "name":
        native.topology.atoms.loc[0, "atom_name"] = "CHANGED"
    elif edit == "naming":
        native.topology.set_group_naming_schemes("amber")
    elif edit == "bonds":
        native.chemical_states.remove_bonds([0])
    elif edit == "structures":
        msm.append_structures(native, msm.extract(native, structure_indices=0))
    else:
        target = native.copy()

    def forbidden(*args, **kwargs):
        pytest.fail("A stale decision must fail before candidate extraction")

    monkeypatch.setattr(msm.basic, "remove", forbidden)
    with pytest.raises(ArgumentConflictError):
        plan.apply(target, skip_digestion=skip_digestion)


def test_coordinate_edits_with_unchanged_axes_do_not_repeat_chemistry(native):
    plan = msm.build.assess_protonation(native, pH=12.0)
    keep = plan.to_dict()["atom_map"]["output_to_source_atom_indices"]
    coordinates = (
        puw.get_value(native.structures.coordinates, to_unit="nm").copy() + 0.125
    )
    msm.set(native, coordinates=puw.quantity(coordinates, "nm"))
    output = plan.apply(native)
    np.testing.assert_array_equal(
        puw.get_value(output.structures.coordinates, to_unit="nm"), coordinates[:, keep]
    )


@pytest.mark.parametrize("storage", ["native", "h5msm"])
def test_retained_coordinates_preserve_nondefault_application_units(
    native, storage, tmp_path
):
    xyz = puw.get_value(native.structures.coordinates, to_unit="nm").copy()
    with puw.context(standard_units=["pm", "ps", "kcal/mol", "K", "e", "radians"]):
        msm.set(native, coordinates=puw.quantity(xyz * 1000, "pm"))
        source = native
        if storage == "h5msm":
            source = str(tmp_path / "units.h5msm")
            msm.h5msm.write(native, source)
        policy = {
            key: value
            for key, value in puw.configure.report().items()
            if key != "loaded_libraries"
        }
        plan = msm.build.assess_protonation(source, pH=12.0)
        keep = plan.to_dict()["atom_map"]["output_to_source_atom_indices"]
        output = plan.apply(source)
        np.testing.assert_allclose(
            puw.get_value(output.structures.coordinates, to_unit="nm"),
            xyz[:, keep],
            atol=1e-14,
        )
        assert {
            key: value
            for key, value in puw.configure.report().items()
            if key != "loaded_libraries"
        } == policy


def test_a_failed_candidate_does_not_publish_or_consume_the_plan(native, monkeypatch):
    plan = msm.build.assess_protonation(native, pH=12.0)
    before = native.copy()
    original = msm.basic.remove

    def failed(*args, **kwargs):
        raise RuntimeError("controlled subset failure")

    monkeypatch.setattr(msm.basic, "remove", failed)
    with pytest.raises(RuntimeError, match="controlled subset"):
        plan.apply(native, in_place=True)
    _unchanged(native, before)
    assert plan.to_dict()["execution"]["status"] == "prepared"
    monkeypatch.setattr(msm.basic, "remove", original)
    assert plan.apply(native, in_place=True) is None
    assert native.get(n_atoms=True) == 590


def test_candidate_axis_failure_precedes_native_publication(native, monkeypatch):
    from molsysmt._private.smonitor import StructuralInconsistencyError

    plan = msm.build.assess_protonation(native, pH=12.0)
    retained = plan.to_dict()["atom_map"]["output_to_source_atom_indices"]
    incomplete = msm.extract(native, selection=retained, structure_indices=[0, 1])
    before = native.copy()
    monkeypatch.setattr(msm.basic, "remove", lambda *args, **kwargs: incomplete)
    with pytest.raises(StructuralInconsistencyError, match="structure axis"):
        plan.apply(native, in_place=True)
    _unchanged(native, before)
    assert plan.to_dict()["execution"]["status"] == "prepared"


def test_terminal_context_honors_nonjoining_edges_without_rebuilding(native):
    bonds = native.chemical_states._get_chemical_state_bonds()
    groups = native.topology.atoms["group_index"].to_numpy()
    first = bonds["atom1_index"].to_numpy(dtype=int)
    second = bonds["atom2_index"].to_numpy(dtype=int)
    boundary = ((groups[first] == 0) & (groups[second] == 1)) | (
        (groups[first] == 1) & (groups[second] == 0)
    )
    assert np.count_nonzero(boundary) == 1
    bonds.loc[boundary, "joins_components"] = False
    before = native.copy()
    report = msm.build.assess_protonation(native, pH=7.4).to_dict()
    contexts = {entry["group_index"]: entry for entry in report["group_contexts"]}
    assert contexts[0]["is_c_terminal"]
    assert contexts[1]["is_n_terminal"]
    assert not contexts[1]["is_c_terminal"]
    _unchanged(native, before)


@pytest.mark.parametrize("pH", [True, np.nan, np.inf, [7.4], "7.4"])
def test_invalid_ph_never_creates_a_prepared_decision(native, pH):
    with pytest.raises(ArgumentError, match="pH"):
        msm.build.assess_protonation(native, pH=pH)


@pytest.mark.parametrize("scope", ["one", "all", "named_terminal"])
def test_empty_removal_distinguishes_unassessed_chemistry(native, scope):
    if scope == "all":
        native.topology.groups["group_name"] = "UNSUPPORTED"
    else:
        native.topology.groups.loc[0, "group_name"] = (
            "LYN" if scope == "named_terminal" else "UNSUPPORTED"
        )
        if scope == "named_terminal":
            native.topology.set_group_naming_schemes("amber", group_indices=0)
    before = native.copy()
    plan = msm.build.assess_protonation(native, pH=7.4)
    report = plan.to_dict()
    assert report["status"] == ("unassessed" if scope == "all" else "partial_no_change")
    assert not report["coverage"]["complete"]
    assert len(report["removed_atom_indices"]) == 0
    assert 0 in report["coverage"]["unassessed_group_indices"]
    contexts = report["group_contexts"]
    assert len(contexts) == native.topology.n_groups
    assert contexts[0]["status"] == "unassessed"
    assert contexts[0]["group_name"] == native.topology.groups.loc[0, "group_name"]
    assert contexts[0]["naming_scheme"] == native.topology.group_naming_schemes[0]
    assert contexts[0]["reason"] == report["coverage"]["unassessed_reasons"][0]
    if scope == "named_terminal":
        assert (
            report["coverage"]["unassessed_reasons"][0]
            == "named_state_terminal_reference_unavailable"
        )
    output = plan.apply(native)
    assert output.get(n_atoms=True) == 596
    _unchanged(native, before)


def test_declared_internal_state_is_not_overwritten_by_the_ph_rule(native):
    native.topology.groups.loc[7, "group_name"] = "LYN"
    native.topology.set_group_naming_schemes("amber", group_indices=7)
    report = msm.build.assess_protonation(native, pH=7.4).to_dict()
    removed = report["removed_atom_indices"]
    assert len(removed) == 1
    assert native.topology.atoms.iloc[removed]["group_index"].tolist() == [7]
    assert native.topology.atoms.iloc[removed]["atom_name"].iloc[0] in {
        "HZ1",
        "HZ2",
        "HZ3",
    }
    for pH in (2.0, 12.0):
        other = msm.build.assess_protonation(native, pH=pH).to_dict()[
            "removed_atom_indices"
        ]
        in_group = other[
            native.topology.atoms.iloc[other]["group_index"].to_numpy() == 7
        ]
        np.testing.assert_array_equal(in_group, removed)


def test_nonunique_labels_never_determine_the_atom_map(native):
    native.topology.atoms["atom_id"] = "repeated"
    native.topology.groups["group_id"] = "repeated"
    plan = msm.build.assess_protonation(native, pH=12.0)
    keep = plan.to_dict()["atom_map"]["output_to_source_atom_indices"]
    xyz = puw.get_value(native.structures.coordinates, to_unit="nm").copy()
    output = plan.apply(native)
    assert output.get(n_atoms=True) == 590
    assert set(output.topology.atoms["atom_id"]) == {"repeated"}
    np.testing.assert_array_equal(
        puw.get_value(output.structures.coordinates, to_unit="nm"), xyz[:, keep]
    )


def test_two_completed_maps_compose_through_the_existing_public_tool(native):
    first = msm.build.assess_protonation(native, pH=9.8)
    intermediate = first.apply(native)
    assert intermediate.get(n_atoms=True) == 595
    second = msm.build.assess_protonation(intermediate, pH=12.0)
    output = second.apply(intermediate)
    assert output.get(n_atoms=True) == 590
    composed = msm.basic.compose_atom_maps(
        [first.to_dict()["atom_map"], second.to_dict()["atom_map"]]
    )
    direct = msm.build.assess_protonation(native, pH=12.0).to_dict()["atom_map"]
    for name in ("source_to_output_atom_indices", "output_to_source_atom_indices"):
        np.testing.assert_array_equal(composed[name], direct[name])


def test_report_mutation_cannot_change_the_prepared_decision(native):
    plan = msm.build.assess_protonation(native, pH=12.0)
    report = plan.to_dict()
    report["removed_atom_indices"][:] = 0
    report["atom_map"]["output_to_source_atom_indices"][:] = 0
    report["parameters"]["pH"] = 7.4
    report["coverage"]["assessed_group_indices"][:] = 0
    assert len(np.unique(plan.to_dict()["removed_atom_indices"])) == 6
    assert plan.apply(native).get(n_atoms=True) == 590


def test_assessment_neither_reads_coordinate_values_nor_retains_the_source(
    native, monkeypatch
):
    import gc
    import weakref

    source = native.copy()
    coords = source.structures.coordinates
    original = puw.get_value

    def guarded(value, *args, **kwargs):
        if value is coords:
            pytest.fail("A name/graph decision must not read trajectory values")
        return original(value, *args, **kwargs)

    monkeypatch.setattr(puw, "get_value", guarded)
    plan = msm.build.assess_protonation(source, pH=12.0)
    reference = weakref.ref(source)
    del source
    gc.collect()
    assert reference() is None
    assert len(plan.to_dict()["removed_atom_indices"]) == 6


def test_modular_assessment_projects_no_coordinate_or_interaction_payload(
    native, tmp_path, monkeypatch
):
    import importlib

    path = str(tmp_path / "protonation.h5msm")
    msm.h5msm.write(native, path)
    module = importlib.import_module("molsysmt.form._h5msm05_modular")
    with monkeypatch.context() as patch:

        def forbidden(*args, **kwargs):
            pytest.fail(
                "Read-only protonation assessment needs no saved coordinate/analysis payload"
            )

        patch.setattr(module, "read_molsys_file", forbidden)
        patch.setattr(module, "read_independent_structures", forbidden)
        patch.setattr(module, "read_named_analyses", forbidden)
        plan = msm.build.assess_protonation(path, pH=12.0)
    output = plan.apply(path)
    assert output.get(n_atoms=True) == 590
    assert output.get(n_structures=True) == 3


@pytest.mark.parametrize("in_place", [False, True])
def test_current_named_analyses_and_mechanical_arrays_follow_the_retained_axis(
    native, in_place
):
    plan = msm.build.assess_protonation(native, pH=12.0)
    report = plan.to_dict()
    removed = int(report["removed_atom_indices"][0])
    keep = report["atom_map"]["output_to_source_atom_indices"]
    records = [
        dict(
            structure_index=index,
            interaction_type="synthetic",
            participants=[
                dict(role="a", atom_indices=[atom]),
                dict(role="b", atom_indices=[int(keep[1])]),
            ],
        )
        for index, atom in [(0, removed), (2, 0)]
    ]
    native.interactions = {
        "probe": msm.Interactions.from_records(
            records,
            n_atoms=596,
            n_structures=3,
            evaluated_structure_indices=[0, 2],
            method="synthetic_map_control",
        )
    }
    charges = np.linspace(-0.1, 0.1, 596)
    msm.set(native, element="atom", partial_charge=puw.quantity(charges, "e"))
    outcome = plan.apply(native, in_place=in_place)
    output = native if in_place else outcome
    if in_place:
        assert outcome is None
    else:
        assert native.interactions["probe"].query().n_interactions == 2
    observed = output.interactions["probe"].query().to_dict()
    np.testing.assert_array_equal(observed["structure_indices"], [2])
    # Remapping creates a new complete analysis; row positions belong to it.
    np.testing.assert_array_equal(observed["occurrence_indices"], [0])
    np.testing.assert_array_equal(
        output.interactions["probe"].atom_source_indices, keep
    )
    np.testing.assert_array_equal(observed["evaluated_structure_indices"], [0, 2])
    np.testing.assert_allclose(
        np.asarray(output.molecular_mechanics.partial_charge, dtype=float),
        charges[keep],
    )


@pytest.mark.parametrize("storage", ["native", "h5msm"])
def test_all_stored_states_and_structure_associations_are_projected_without_selection(
    native, storage, tmp_path
):
    native.chemical_states.append_state()
    native.chemical_states._set_reference_index(0)
    native._set_structure_chemical_state_indices([0, 1, 0])
    source = native
    if storage == "h5msm":
        source = str(tmp_path / "states.h5msm")
        msm.h5msm.write(native, source)
    plan = msm.build.assess_protonation(source, pH=12.0)
    report = plan.to_dict()
    np.testing.assert_array_equal(
        report["source"]["structure_chemical_state_indices"], [0, 1, 0]
    )
    np.testing.assert_array_equal(
        report["coverage"]["assessed_chemical_state_indices"], [0]
    )
    np.testing.assert_array_equal(
        report["coverage"]["unassessed_chemical_state_indices"], [1]
    )
    assert not report["coverage"]["complete"]
    output = plan.apply(source)
    assert output.chemical_states.n_chemical_states == 2
    assert output.chemical_states.reference_chemical_state_index == 0
    assert output.get(structure_chemical_state_index=True) == [0, 1, 0]
    assert native.get(n_atoms=True) == 596


def test_changed_structure_state_association_invalidates_a_prepared_decision(native):
    plan = msm.build.assess_protonation(native, pH=12.0)
    msm.set(native, structure_indices=0, structure_chemical_state_index=pd.NA)
    with pytest.raises(ArgumentConflictError):
        plan.apply(native)


def test_empty_native_assessment_has_typed_axes_without_coordinate_data():
    from molsysmt.native import MolSys

    source = MolSys()
    plan = msm.build.assess_protonation(source)
    report = plan.to_dict()
    assert report["status"] == "no_change"
    for values in (
        report["removed_atom_indices"],
        report["structure_indices"],
        report["atom_map"]["output_to_source_atom_indices"],
    ):
        assert values.shape == (0,) and values.dtype == np.int64
    output = plan.apply(source)
    assert output is not source and output.get(n_atoms=True) == 0


def test_inventory_only_input_does_not_acquire_an_invented_empty_chemical_graph(
    native, monkeypatch
):
    from molsysmt._private.smonitor import NotWithThisFormError

    def forbidden(*args, **kwargs):
        pytest.fail("Missing source chemistry must not be invented by conversion")

    monkeypatch.setattr(msm.basic, "convert", forbidden)
    with pytest.raises(NotWithThisFormError):
        msm.build.assess_protonation(native.topology)


def test_optional_tracking_absence_retains_the_actual_reference_records(
    native, monkeypatch
):
    from molsysmt import _ackredit

    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    plan = msm.build.assess_protonation(native, pH=12.0)
    report = plan.to_dict()
    assert (
        report["attribution"]["items"][0]["id"]
        == "software:molsysmt:" + msm.__version__
    )
    assert any(item["type"] == "dataset" for item in report["attribution"]["items"])
    assert plan.apply(native).get(n_atoms=True) == 590


def test_real_tracking_reused_references_and_report_ownership(native):
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("prepared protonation"):
        with ackredit.capture("first decision") as first:
            plan = msm.build.assess_protonation(native, pH=12.0)
        with ackredit.capture("second decision") as second:
            other = msm.build.assess_protonation(native, pH=7.4)
        original = plan.to_dict()
        expected = {item["id"] for item in original["attribution"]["items"]}
        assert expected.issubset(
            {item["id"] for item in first.attribution.to_dict()["items"]}
        )
        assert expected.issubset(
            {item["id"] for item in second.attribution.to_dict()["items"]}
        )
        assert original["software"] == {"molsysmt": msm.__version__}
        original["attribution"]["items"][0]["title"] = "caller-owned edit"
        assert plan.to_dict()["attribution"]["items"][0]["title"] == "MolSysMT"
        assert other.to_dict()["attribution"]["items"][0]["title"] == "MolSysMT"
    with ackredit.session("apply already prepared decision"):
        plan.apply(native)
        assert not ackredit.get_used_items()


def test_direct_public_constructor_uses_the_same_validated_contract(native):
    plan = msm.build.ProtonationAssessment(native, pH=12.0)
    assert len(plan.to_dict()["removed_atom_indices"]) == 6
    with pytest.raises(ArgumentError, match="pH"):
        msm.build.ProtonationAssessment(native, pH=np.nan)
