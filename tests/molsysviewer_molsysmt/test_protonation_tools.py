"""Receive independent reference-rule H removal without implicit scene editing."""

import inspect

import molsysviewer as msv
import numpy as np
import pandas as pd
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError
from molsysmt.native import Structures
from tests.build.test_get_residue_chemical_coverage import _system
from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
    same,
    snapshot,
    unchanged,
)

puw = msm.pyunitwizard
# Bounded deposited-villin control, independent of the private H selector:
# N-terminal H3 and the third NZ proton on five lysines at pH 12.
REMOVED_LABELS = {("H3", 0)} | {("HZ3", i) for i in (7, 24, 29, 30, 32)}


@pytest.fixture(scope="module")
def source():
    source = msm.convert(
        msm.systems["chicken villin HP35"]["1vii.pdb"],
        to_form="molsysmt.MolSys",
    )
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm")
    source.structures = Structures(
        coordinates=puw.quantity(
            np.repeat(xyz, 3, axis=0) + np.arange(3)[:, None, None], "nm"
        ),
        box=puw.quantity(np.repeat((np.eye(3) * 6)[None], 3, axis=0), "nm"),
        time=puw.quantity([2, 5, 11], "ps"),
        structure_id=["C", "A", "C"],
    )
    assert source.get_n_atoms() == 596
    return source


@pytest.fixture
def view(source):
    with msv.new_view(source.copy()) as view:
        view.regions.add(selection=[0, 2], tag="keep")
        view.shapes.add_sphere(atom_indices=[1], tag="anchor")
        view.interactions.attach(
            msm.Interactions.from_records(
                [],
                n_atoms=596,
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.protonation",
            ),
            name="saved",
            assume_aligned=True,
        )
        yield view


def retained_indices(source, pH):
    labels = list(
        zip(source.topology.atoms.atom_name, source.topology.atoms.group_index)
    )
    if pH == 12.0:
        assert set(labels) & REMOVED_LABELS == REMOVED_LABELS
    return [
        i for i, label in enumerate(labels) if pH != 12.0 or label not in REMOVED_LABELS
    ]


def test_signature_help_discovery_and_default(view):
    call = view.addons.molsysmt.build.reconcile_protonation
    native = inspect.signature(msm.build.reconcile_protonation)
    expected = list(native.parameters.values())[1:]
    expected.append(
        inspect.Parameter("update_view", inspect.Parameter.KEYWORD_ONLY, default=True)
    )
    assert inspect.signature(call) == native.replace(parameters=expected)
    assert call.digestion_plan is not None
    assert "reconcile_protonation" in dir(view.addons.molsysmt.build)
    assert not hasattr(view.addons.molsysmt, "reconcile_protonation")
    text = inspect.getdoc(call)
    assert "public native ProtonationAssessment" in text
    assert "update_view" in text and "pKa" in text
    for parameter in inspect.signature(call).parameters:
        assert f"{parameter} :" in text
    before = snapshot(view)
    result = call()
    assert result is not view.molsys
    same(result, view.molsys)
    unchanged(view, before)


@pytest.mark.parametrize("pH", [7.4, 12.0])
@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("unit", ["nm", "angstrom"])
def test_reference_removals_all_poses_units_and_independent_ownership(
    view, pH, skip, unit
):
    target = view.molsys
    indices = retained_indices(target, pH)
    expected = msm.build.reconcile_protonation(target.copy(), pH=pH)
    before = snapshot(view)
    with puw.context(standard_units=[unit, "ps", "radians"]):
        policy = dict(puw.configure.get_standard_units())
        result = view.addons.molsysmt.build.reconcile_protonation(
            pH=pH, skip_digestion=skip
        )
        assert dict(puw.configure.get_standard_units()) == policy
    assert result is not target
    assert result.get_n_atoms() == (590 if pH == 12 else 596)
    assert result.structures.n_structures == 3
    assert result.structures.structure_id.tolist() == ["C", "A", "C"]
    np.testing.assert_array_equal(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        puw.get_value(target.structures.coordinates, to_unit="nm")[:, indices],
    )
    for field in ("box", "time"):
        same(getattr(result.structures, field), getattr(target.structures, field))
    pd.testing.assert_frame_equal(
        result.topology.atoms,
        target.topology.atoms.iloc[indices].reset_index(drop=True),
        check_frame_type=False,
        # Native extraction normalizes nullable index dtypes. Strict dtype
        # parity with the native result is checked separately below.
        check_dtype=False,
    )
    same(result, expected)
    unchanged(view, before)
    # Neither result data nor its remapped analysis owns the source arrays.
    msm.set(result, coordinates=result.structures.coordinates + puw.quantity(1, "nm"))
    result.interactions = {}
    unchanged(view, before)


@pytest.mark.parametrize("skip", [False, True])
def test_repeated_id_labels_do_not_define_correspondence(view, skip):
    msm.set(view.molsys, element="atom", atom_id=["same"] * 596)
    before = snapshot(view)
    result = view.addons.molsysmt.build.reconcile_protonation(
        pH=12.0, skip_digestion=skip
    )
    assert result.get_n_atoms() == 590
    assert set(result.topology.atoms.atom_id) == {"same"}
    unchanged(view, before)


@pytest.mark.parametrize("pH", [7.4, 12.0])
def test_named_analysis_occurrences_follow_native_subset_without_recalculation(
    view, pH
):
    target = view.molsys
    indices = retained_indices(target, 12.0)
    removed = next(i for i in range(596) if i not in indices)
    records = [
        {
            "structure_index": frame,
            "interaction_type": "contact",
            "participants": [
                {"role": "first", "atom_indices": [atom]},
                {"role": "second", "atom_indices": [indices[-1]]},
            ],
        }
        for frame in range(3)
        for atom in (indices[0], removed)
    ]
    observations = msm.Interactions.from_records(
        records,
        n_atoms=596,
        n_structures=3,
        evaluated_structure_indices=[0, 1, 2],
        method="synthetic.stored-observations",
    )
    target.interactions = {**target.interactions, "observations": observations}
    before = snapshot(view)
    expected = msm.remove(
        target,
        selection=[i for i in range(596) if i not in indices] if pH == 12 else None,
    )
    result = view.addons.molsysmt.build.reconcile_protonation(pH=pH)
    analysis = result.interactions["observations"]
    assert len(analysis.occurrence_structures) == (3 if pH == 12 else 6)
    assert analysis.n_atoms == result.get_n_atoms()
    np.testing.assert_array_equal(analysis.evaluated_structure_indices, [0, 1, 2])
    assert analysis is not target.interactions["observations"]
    assert analysis.method == expected.interactions["observations"].method
    same(analysis.to_dict(), expected.interactions["observations"].to_dict())
    assert len(result.interactions["saved"].occurrence_structures) == 0
    unchanged(view, before)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("parameters", [{"engine": "OpenMM"}, {"pH": "invalid"}])
def test_native_errors_remain_native_and_preserve_source(view, skip, parameters):
    before = snapshot(view)
    with pytest.raises(Exception) as native:
        msm.build.reconcile_protonation(
            view.molsys.copy(), **parameters, skip_digestion=skip
        )
    with pytest.raises(type(native.value)) as actual:
        view.addons.molsysmt.build.reconcile_protonation(
            **parameters, skip_digestion=skip
        )
    assert str(actual.value) == str(native.value)
    unchanged(view, before)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("update_view", [False, True])
@pytest.mark.parametrize("unit", ["nm", "angstrom"])
def test_managed_protonation_uses_public_maps_and_all_structure_subset(
    view, skip, update_view, unit
):
    target = view.molsys
    original = target.copy()
    keep = np.asarray(retained_indices(target, 12.0), dtype=np.int64)
    expected = msm.build.reconcile_protonation(original, pH=12.0)
    with puw.context(standard_units=[unit, "ps", "radians"]):
        result = view.addons.molsysmt.build.reconcile_protonation(
            pH=12.0, in_place=True, skip_digestion=skip, update_view=update_view
        )
    assert result is None and view.molsys is target
    assert target.get_n_atoms() == 590
    same(target, expected)
    same(target.structures.box, original.structures.box)
    same(target.structures.time, original.structures.time)
    np.testing.assert_array_equal(
        target.structures.structure_id, original.structures.structure_id
    )
    np.testing.assert_array_equal(
        puw.get_value(target.structures.coordinates, to_unit="nm"),
        puw.get_value(original.structures.coordinates, to_unit="nm")[:, keep],
    )
    status = view.addons.molsysmt.get_sync_status()
    assert status["state"] == ("synchronized" if update_view else "pending")
    assert status["target_revision"] == 1
    if not update_view:
        view.addons.molsysmt.sync_view()
    assert view.whole.get(n_atoms=True) == 590
    assert view.player.n_structures == 3
    assert view.shapes["anchor"].info()["atom_indices"] == [
        int(np.flatnonzero(keep == 1)[0])
    ]
    assert view.molsys.interactions["saved"].evaluated_structure_indices.tolist() == [
        0,
        1,
        2,
    ]
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("value", [1, None, "yes"])
def test_integration_admission_cannot_bypass_boolean_validation(view, skip, value):
    before = snapshot(view)
    with pytest.raises(ArgumentError):
        view.addons.molsysmt.build.reconcile_protonation(
            in_place=value, skip_digestion=skip
        )
    unchanged(view, before)


def test_no_implicit_preparation_structure_or_scene_controls(view):
    call = view.addons.molsysmt.build.reconcile_protonation
    for key in (
        "molecular_system",
        "selection",
        "structure_indices",
        "return_report",
    ):
        with pytest.raises(UnknownArgumentError):
            call(**{key: None})


def test_pending_primary_and_cached_method_follow_lifetime(view, source):
    tools = view.addons.molsysmt
    call = tools.build.reconcile_protonation
    tools.structure.translate(
        translation="[0.1,0,0] nm", in_place=True, update_view=False
    )
    before = snapshot(view)
    result = call(pH=12.0)
    np.testing.assert_array_equal(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[
            :, retained_indices(view.molsys, 12.0)
        ],
    )
    unchanged(view, before)
    tools.sync_view()
    replacement = msm.build.reconcile_protonation(source, pH=12.0)
    view.load(replacement, mode="replace")
    assert call(pH=7.4).get_n_atoms() == 590
    view.close()
    with pytest.raises(RuntimeError, match="closed view"):
        call()
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.build.reconcile_protonation()


def test_unassessed_group_is_retained_without_claiming_protonation_readiness():
    source = _system(
        [("UNL", (["C1", "H99"], ["C", "H"], [("C1", "H99", 1)]))], n_frames=2
    )
    with msv.new_view(source) as view:
        before = snapshot(view)
        result = view.addons.molsysmt.build.reconcile_protonation(pH=12.0)
        assert result is not view.molsys and result.get_n_atoms() == 2
        same(result, view.molsys)
        unchanged(view, before)


def test_explicit_amber_histidine_state_keeps_its_sidechain_hydrogen():
    source = msm.build.build_peptide("AHA", engine="MolSysMT")
    source = msm.remove(source, selection='atom_type=="H"')
    middle = int(
        source.topology.groups.index[source.topology.groups.group_name == "HIS"][0]
    )
    source.topology.groups.at[middle, "group_name"] = "HID"
    source.topology.set_group_naming_schemes("amber", group_indices=[middle])
    source = msm.build.add_missing_hydrogens(source, pH=12.0, engine="MolSysMT")
    with msv.new_view(source) as view:
        before = snapshot(view)
        result = view.addons.molsysmt.build.reconcile_protonation(pH=12.0)
        atoms = result.topology.atoms
        names = set(atoms.loc[atoms.group_index == middle, "atom_name"])
        assert "HD1" in names and "HE2" not in names
        assert (
            result.topology.group_naming_schemes == source.topology.group_naming_schemes
        )
        unchanged(view, before)


def test_assessment_signature_and_read_only_expert_result(view):
    call = view.addons.molsysmt.build.assess_protonation
    native = inspect.signature(msm.build.assess_protonation)
    assert inspect.signature(call) == native.replace(
        parameters=list(native.parameters.values())[1:]
    )
    assert call.digestion_plan is not None
    assert "assess_protonation" in dir(view.addons.molsysmt.build)
    assert "not a managed addon edit" in inspect.getdoc(call)
    assert "\nmolecular_system :" not in inspect.getdoc(call)
    with pytest.raises(UnknownArgumentError):
        call(molecular_system=view.molsys)
    with pytest.raises(UnknownArgumentError):
        call(update_view=True)
    with pytest.raises(ArgumentError):
        call(skip_digestion="yes")


@pytest.mark.parametrize("pH", [7.4, 12.0])
@pytest.mark.parametrize("skip", [False, True])
def test_assessment_maps_are_public_positional_and_do_not_change_the_view(
    view, pH, skip
):
    before = snapshot(view)
    result = view.addons.molsysmt.build.assess_protonation(pH=pH, skip_digestion=skip)
    assert isinstance(result, msm.build.ProtonationAssessment)
    report = result.to_dict()
    keep = np.array(retained_indices(view.molsys, pH), dtype=np.int64)
    reverse = np.full(596, -1, dtype=np.int64)
    reverse[keep] = np.arange(len(keep))
    np.testing.assert_array_equal(
        report["atom_map"]["output_to_source_atom_indices"], keep
    )
    np.testing.assert_array_equal(
        report["atom_map"]["source_to_output_atom_indices"], reverse
    )
    np.testing.assert_array_equal(report["structure_indices"], [0, 1, 2])
    assert report["status"] == ("removal_required" if pH == 12.0 else "no_change")
    assert report["parameters"]["pH"] == pH
    assert report["execution"]["status"] == "prepared"
    report["atom_map"]["output_to_source_atom_indices"][:] = 0
    report["parameters"]["pH"] = -200
    np.testing.assert_array_equal(
        result.to_dict()["atom_map"]["output_to_source_atom_indices"], keep
    )
    assert result.to_dict()["parameters"]["pH"] == pH
    unchanged(view, before)


@pytest.mark.parametrize("pH", [7.4, 12.0])
def test_native_assessment_independent_application_retains_result_type_and_single_use(
    view, pH
):
    from molsysmt._private.smonitor import ArgumentConflictError

    before = snapshot(view)
    assessment = view.addons.molsysmt.build.assess_protonation(pH=pH)
    output = assessment.apply(view.molsys)
    keep = retained_indices(view.molsys, pH)
    assert output is not view.molsys and output.get_n_atoms() == len(keep)
    np.testing.assert_array_equal(
        puw.get_value(output.structures.coordinates, to_unit="nm"),
        puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[:, keep],
    )
    assert assessment.to_dict()["execution"]["status"] == (
        "applied" if pH == 12.0 else "no_op"
    )
    with pytest.raises(ArgumentConflictError, match="consumed"):
        assessment.apply(view.molsys)
    unchanged(view, before)


def test_assessment_uses_pending_coordinates_at_application_without_scene_projection(
    view,
):
    tools = view.addons.molsysmt
    assessment = tools.build.assess_protonation(pH=12.0)
    tools.structure.translate(
        translation="[0.2,0,0] nm", in_place=True, update_view=False
    )
    before = snapshot(view)
    assert before[3]["state"] == "pending"
    later = tools.build.assess_protonation(pH=12.0)
    np.testing.assert_array_equal(
        later.to_dict()["removed_atom_indices"],
        assessment.to_dict()["removed_atom_indices"],
    )
    result = assessment.apply(view.molsys)
    keep = retained_indices(view.molsys, 12.0)
    np.testing.assert_array_equal(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        puw.get_value(view.molsys.structures.coordinates, to_unit="nm")[:, keep],
    )
    unchanged(view, before)


def test_assessment_native_staleness_and_cached_reader_follow_source_replacement(view):
    from molsysmt._private.smonitor import ArgumentConflictError

    call = view.addons.molsysmt.build.assess_protonation
    original = view.molsys
    assessment = call(pH=12.0)
    replacement = original.copy()
    view.load(replacement, mode="replace")
    before = snapshot(view)
    with pytest.raises(ArgumentConflictError):
        assessment.apply(view.molsys)
    fresh = call(pH=12.0)
    assert len(fresh.to_dict()["removed_atom_indices"]) == 6
    unchanged(view, before)
    target = view.molsys
    view.close()
    result = fresh.apply(target)
    assert result.get_n_atoms() == 590
    with pytest.raises(RuntimeError, match="closed view"):
        call()
    with msv.new_view() as empty:
        with pytest.raises(ValueError, match="Load a molecular system"):
            empty.addons.molsysmt.build.assess_protonation()


@pytest.mark.parametrize(
    "parameters", [{"pH": True}, {"pH": np.nan}, {"pH": np.inf}, {"engine": "OpenMM"}]
)
def test_assessment_native_errors_preserve_data_scene_and_sync(view, parameters):
    before = snapshot(view)
    with pytest.raises(Exception) as native:
        msm.build.assess_protonation(view.molsys, **parameters)
    with pytest.raises(type(native.value)) as actual:
        view.addons.molsysmt.build.assess_protonation(**parameters)
    assert str(actual.value) == str(native.value)
    unchanged(view, before)


@pytest.mark.parametrize("update_view", [False, True])
def test_managed_protonation_noop_preserves_domains_history_and_revision(
    view, update_view
):
    target = view.molsys
    before = snapshot(view)
    domains = (
        target.topology,
        target.chemical_states,
        target.structures,
        target.molecular_mechanics,
    )
    assert (
        view.addons.molsysmt.build.reconcile_protonation(
            in_place=True, update_view=update_view
        )
        is None
    )
    assert domains == (
        target.topology,
        target.chemical_states,
        target.structures,
        target.molecular_mechanics,
    )
    assert view.export_state() == before[2]
    assert (list(view.history._undo), list(view.history._redo)) == before[4]
    status = view.addons.molsysmt.get_sync_status()
    assert (
        status["state"] == "synchronized"
        and status["target_revision"] == 0
        and status["pending_operations"] == 0
    )


def test_managed_protonation_composes_with_prior_deferred_removal(view):
    tools = view.addons.molsysmt
    original = view.molsys.copy()
    keep = np.asarray(retained_indices(original, 12.0))
    removed_elsewhere = int(keep[-1])
    tools.basic.remove(selection=[removed_elsewhere], in_place=True, update_view=False)
    expected = msm.build.reconcile_protonation(view.molsys.copy(), pH=12.0)
    tools.build.reconcile_protonation(pH=12.0, in_place=True, update_view=False)
    assert tools.get_sync_status()["pending_operations"] == 2
    same(view.molsys, expected)
    tools.sync_view()
    assert view.molsys.get_n_atoms() == view.whole.get(n_atoms=True) == 589
    assert tools.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize("update_view", [False, True])
def test_managed_protonation_noop_can_preserve_or_complete_earlier_pending_work(
    view, update_view
):
    tools = view.addons.molsysmt
    tools.structure.translate(
        translation="[0.1,0,0] nm", in_place=True, update_view=False
    )
    before = snapshot(view)
    assert (
        tools.build.reconcile_protonation(in_place=True, update_view=update_view)
        is None
    )
    same(view.molsys, before[1])
    status = tools.get_sync_status()
    assert status["state"] == ("synchronized" if update_view else "pending")
    assert status["target_revision"] == 1


@pytest.mark.parametrize(
    "parameters", [{"pH": True}, {"pH": np.inf}, {"engine": "OpenMM"}]
)
def test_managed_protonation_preparation_failures_preserve_prior_pending_work(
    view, parameters
):
    tools = view.addons.molsysmt
    tools.structure.translate(
        translation="[0.1,0,0] nm", in_place=True, update_view=False
    )
    before = snapshot(view)
    with pytest.raises(Exception) as native:
        msm.build.reconcile_protonation(view.molsys.copy(), in_place=True, **parameters)
    with pytest.raises(type(native.value)):
        tools.build.reconcile_protonation(in_place=True, **parameters)
    unchanged(view, before)


@pytest.mark.parametrize("value", [None, 1, "yes"])
def test_managed_protonation_update_control_is_strict_even_with_digest_skipped(
    view, value
):
    before = snapshot(view)
    with pytest.raises((ArgumentError, TypeError)):
        view.addons.molsysmt.build.reconcile_protonation(
            in_place=True, update_view=value, skip_digestion=True
        )
    unchanged(view, before)


def test_managed_protonation_rejects_invalid_public_maps_before_removal(
    view, monkeypatch
):
    original = msm.build.ProtonationAssessment.to_dict

    def broken(assessment, *args, **kwargs):
        report = original(assessment, *args, **kwargs)
        report["atom_map"]["source_to_output_atom_indices"][0] = -1
        return report

    monkeypatch.setattr(msm.build.ProtonationAssessment, "to_dict", broken)
    before = snapshot(view)
    with pytest.raises(ValueError, match="incompatible atom or structure maps"):
        view.addons.molsysmt.build.reconcile_protonation(pH=12.0, in_place=True)
    unchanged(view, before)


def test_managed_protonation_sync_retry_does_not_repeat_assessment_or_removal(
    source, monkeypatch
):
    from molsysviewer.system_edits import SystemEditSyncError

    from tests.molsysviewer_molsysmt.test_minimization_tools import (
        InterruptedMinimizationWidget,
    )

    original = msm.build.assess_protonation
    calls = []

    def observed(*args, **kwargs):
        calls.append(1)
        return original(*args, **kwargs)

    monkeypatch.setattr(msm.build, "assess_protonation", observed)
    with msv.MolSysView(transport=InterruptedMinimizationWidget()) as owner:
        owner.load(source)
        owner.shapes.add_sphere(atom_indices=[1], tag="anchor")
        owner._ready = True
        owner.widget.interrupted = True
        with pytest.raises(SystemEditSyncError) as error:
            owner.addons.molsysmt.build.reconcile_protonation(pH=12.0, in_place=True)
        assert error.value.science_completed and error.value.scientific_result is None
        assert owner.molsys.get_n_atoms() == 590 and len(calls) == 1
        xyz = puw.get_value(owner.molsys.structures.coordinates, to_unit="nm").copy()
        storage = owner.molsys.structures._coordinates
        owner.addons.molsysmt.sync_view()
        np.testing.assert_array_equal(
            puw.get_value(owner.molsys.structures.coordinates, to_unit="nm"), xyz
        )
        assert owner.molsys.structures._coordinates is storage and len(calls) == 1
        assert owner.addons.molsysmt.get_sync_status()["state"] == "synchronized"


def test_managed_protonation_postpublication_failure_is_uncertain(view, monkeypatch):
    from molsysviewer.system_edits import SystemEditPendingError

    original = msm.build.ProtonationAssessment.apply

    def interrupted(assessment, *args, **kwargs):
        original(assessment, *args, **kwargs)
        raise OSError("after native protonation publication")

    monkeypatch.setattr(msm.build.ProtonationAssessment, "apply", interrupted)
    with pytest.raises(OSError, match="after native protonation publication"):
        view.addons.molsysmt.build.reconcile_protonation(pH=12.0, in_place=True)
    assert view.molsys.get_n_atoms() == 590
    assert view.addons.molsysmt.get_sync_status()["state"] == "uncertain"
    with pytest.raises(SystemEditPendingError):
        view.addons.molsysmt.sync_view()


def test_assessment_and_managed_noop_keep_unassessed_chemistry_explicit():
    molsys = _system(
        [("UNL", (["C1", "H99"], ["C", "H"], [("C1", "H99", 1)]))], n_frames=2
    )
    with msv.new_view(molsys) as view:
        before = snapshot(view)
        report = view.addons.molsysmt.build.assess_protonation(pH=12.0).to_dict()
        assert report["status"] == "unassessed"
        assert not report["coverage"]["complete"]
        assert len(report["removed_atom_indices"]) == 0
        unchanged(view, before)
        assert (
            view.addons.molsysmt.build.reconcile_protonation(pH=12.0, in_place=True)
            is None
        )
        same(view.molsys, before[1])
        assert view.export_state() == before[2]
        assert view.addons.molsysmt.get_sync_status()["target_revision"] == 0


@pytest.mark.parametrize("pending", [False, True])
def test_managed_native_prepublication_rejection_preserves_source_and_pending_maps(
    view, monkeypatch, pending
):
    if pending:
        view.addons.molsysmt.structure.translate(
            translation="[0.1,0,0] nm", in_place=True, update_view=False
        )
    before = snapshot(view)

    def unavailable(assessment, *args, **kwargs):
        raise MemoryError("native candidate allocation unavailable before publication")

    monkeypatch.setattr(msm.build.ProtonationAssessment, "apply", unavailable)
    with pytest.raises(MemoryError, match="before publication"):
        view.addons.molsysmt.build.reconcile_protonation(pH=12.0, in_place=True)
    same(view.molsys, before[1])
    if before[2] is not None:
        assert view.export_state() == before[2]
    status = view.addons.molsysmt.get_sync_status()
    for field in (
        "state",
        "target_revision",
        "integration_revision",
        "pending_operations",
    ):
        assert status[field] == before[3][field]
    assert (list(view.history._undo), list(view.history._redo)) == before[4]
    assert view.widget.initial_messages == before[5]


@pytest.mark.parametrize("update_view", [False, True])
def test_managed_protonation_keeps_surviving_observations_and_historical_coverage(
    view, update_view
):
    target = view.molsys
    keep = retained_indices(target, 12.0)
    removed = next(i for i in range(target.get_n_atoms()) if i not in keep)
    records = [
        dict(
            structure_index=frame,
            interaction_type="contact",
            participants=[
                dict(role="first", atom_indices=[atom]),
                dict(role="second", atom_indices=[keep[-1]]),
            ],
        )
        for frame in range(3)
        for atom in [keep[0], removed]
    ]
    target.interactions = {
        **target.interactions,
        "observations": msm.Interactions.from_records(
            records,
            n_atoms=596,
            n_structures=3,
            evaluated_structure_indices=[0, 1, 2],
            method="receiving.stored-contact-axis",
        ),
    }
    expected = msm.build.reconcile_protonation(target.copy(), pH=12.0)
    view.addons.molsysmt.build.reconcile_protonation(
        pH=12.0, in_place=True, update_view=update_view
    )
    assert len(target.interactions["observations"].occurrence_structures) == 3
    same(
        target.interactions["observations"].to_dict(),
        expected.interactions["observations"].to_dict(),
    )
    if not update_view:
        view.addons.molsysmt.sync_view()
    same(
        target.interactions["observations"].to_dict(),
        expected.interactions["observations"].to_dict(),
    )
    np.testing.assert_array_equal(
        target.interactions["observations"].evaluated_structure_indices, [0, 1, 2]
    )
