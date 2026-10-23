"""Receiving independent molecular copies, conversions and file preflight."""

import inspect

import molsysviewer as msv
import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import MolSys

pytest.importorskip("molsysviewer.system_edits")
puw = msm.pyunitwizard


@pytest.fixture
def view():
    with msv.demo["pentalanine"] as source:
        with msv.new_view(source.molsys, structure_indices=[0, 8, 3]) as result:
            analysis = msm.Interactions.from_records(
                [
                    {
                        "structure_index": index,
                        "interaction_type": "hbond",
                        "participants": [
                            {"role": role, "atom_indices": [atom]}
                            for atom, role in enumerate(
                                ("donor", "hydrogen", "acceptor")
                            )
                        ],
                    }
                    for index in [0, 2]
                ],
                n_atoms=result.molsys.get_n_atoms(),
                n_structures=3,
                evaluated_structure_indices=[0, 1, 2],
                method="receiving.conversion",
            )
            result.interactions.attach(analysis, name="first", assume_aligned=True)
            result.interactions.attach(
                analysis.remap(), name="second", assume_aligned=True
            )
            result.regions.add(selection=[0, 1, 2], tag="source-region")
            yield result


def _coordinates(molsys):
    return puw.get_value(
        msm.get(molsys, element="atom", coordinates=True), to_unit="nm"
    )


def _same_molecular_result(actual, expected):
    assert type(actual) is type(expected)
    assert msm.get(actual, n_atoms=True) == msm.get(expected, n_atoms=True)
    np.testing.assert_array_equal(_coordinates(actual), _coordinates(expected))
    if isinstance(actual, MolSys):
        assert list(actual.interactions) == list(expected.interactions)
        for name in actual.interactions:
            np.testing.assert_equal(
                actual.interactions[name].to_dict(),
                expected.interactions[name].to_dict(),
            )


@pytest.mark.parametrize("name", ["copy", "convert", "get_conversion_report"])
def test_native_signature_documentation_and_alias(view, name):
    native = inspect.signature(getattr(msm.basic, name))
    expected = native.replace(parameters=list(native.parameters.values())[1:])
    bound = getattr(view.addons.molsysmt.basic, name)
    assert inspect.signature(bound) == expected
    assert bound.digestion_plan is not None
    assert getattr(view.addons.molsysmt, name) == bound
    assert "current view.molsys" in inspect.getdoc(bound)
    assert "\nmolecular_system :" not in inspect.getdoc(bound)
    assert "not adopted" in inspect.getdoc(bound)
    assert "update_view" not in expected.parameters


@pytest.mark.parametrize("name", ["copy", "convert"])
def test_native_default_copy_is_independent_and_does_not_adopt(view, name):
    target = view.molsys
    state = view.export_state()
    status = view.addons.molsysmt.get_sync_status()
    native = getattr(msm.basic, name)(target)
    actual = getattr(view.addons.molsysmt.basic, name)()
    _same_molecular_result(actual, native)
    assert actual is not target
    assert actual.structures is not target.structures
    assert actual.topology is not target.topology
    msm.set(actual, element="atom", selection=[0], atom_name="COPY")
    assert msm.get(target, element="atom", selection=[0], atom_name=True) != ["COPY"]
    msm.set(
        actual,
        structure_indices=[0],
        coordinates=msm.get(
            actual, element="atom", structure_indices=[0], coordinates=True
        )
        + puw.quantity(0.2, "nm"),
    )
    assert len(actual.interactions["first"].evaluated_structure_indices) == 2
    assert len(target.interactions["first"].evaluated_structure_indices) == 3
    assert view.molsys is target
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status() == status


@pytest.mark.parametrize("indices", [[2, 0], [2, 0, 2]])
def test_convert_subset_preserves_native_structures_participants_and_maps(
    view, indices
):
    args = dict(selection=[0, 1, 2, 3], structure_indices=indices)
    expected = msm.convert(view.molsys, **args)
    state = view.export_state()
    actual = view.addons.molsysmt.convert(**args)
    _same_molecular_result(actual, expected)
    assert actual.get_n_atoms() == 4
    assert actual.structures.n_structures == len(indices)
    assert view.export_state() == state


def test_converter_options_keep_native_live_reference_policy(view):
    target = view.molsys
    actual = view.addons.molsysmt.convert(copy_if_all=False)
    expected = msm.convert(target, copy_if_all=False)
    assert (actual is target) == (expected is target)
    assert actual is target
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


def test_multiple_target_forms_keep_order_types_reports_and_scope(view):
    args = dict(
        to_form=["molsysmt.MolSys", "molsysmt.Structures"],
        structure_indices=[2, 0],
        return_report=True,
    )
    expected, expected_reports = msm.convert(view.molsys, **args)
    outputs, reports = view.addons.molsysmt.convert(**args)
    assert isinstance(outputs, list) and len(outputs) == 2
    assert reports == expected_reports
    for actual, native in zip(outputs, expected):
        _same_molecular_result(actual, native)
    assert [report.to_form for report in reports] == args["to_form"]


@pytest.mark.parametrize("existing", [False, True])
def test_preflight_does_not_create_or_overwrite_files_or_change_scene(
    view, tmp_path, existing
):
    destination = tmp_path / "inspect.h5msm"
    if existing:
        msm.convert(view.molsys, to_form=destination)
        original_bytes = destination.read_bytes()
    state = view.export_state()
    status = view.addons.molsysmt.get_sync_status()
    storage = view.molsys.structures._coordinates
    args = dict(to_form=[destination, "molsysmt.Structures"], structure_indices=[2, 0])
    expected = msm.get_conversion_report(view.molsys, **args)
    reports = view.addons.molsysmt.get_conversion_report(**args)
    assert reports == expected
    assert reports[0].to_form == "file:h5msm"
    assert destination.exists() is existing
    if existing:
        assert destination.read_bytes() == original_bytes
    assert view.molsys.structures._coordinates is storage
    assert view.export_state() == state
    assert view.addons.molsysmt.get_sync_status() == status


@pytest.mark.parametrize("file_route", ["path", "format_and_filename"])
def test_h5msm_file_roundtrip_preserves_native_named_analyses_and_selected_structures(
    view, tmp_path, file_route
):
    state = view.export_state()
    target = view.molsys
    actual_file = tmp_path / "bound.h5msm"
    native_file = tmp_path / "native.h5msm"
    args = dict(selection=[0, 1, 2, 3], structure_indices=[2, 0, 2], return_report=True)
    if file_route == "path":
        expected_path, expected_report = msm.convert(
            target, to_form=native_file, **args
        )
        path, report = view.addons.molsysmt.convert(to_form=actual_file, **args)
    else:
        expected_path, expected_report = msm.convert(
            target,
            to_form="file:h5msm",
            output_filename=native_file,
            **args,
        )
        path, report = view.addons.molsysmt.convert(
            to_form="file:h5msm",
            output_filename=actual_file,
            **args,
        )
    assert type(path) is type(expected_path)
    assert str(path) == str(actual_file)
    assert report == expected_report
    actual = msm.convert(path)
    expected = msm.convert(expected_path)
    _same_molecular_result(actual, expected)
    assert list(actual.interactions) == ["first", "second"]
    assert actual.structures.n_structures == 3
    assert len(actual.interactions["first"].evaluated_structure_indices) == 3
    assert view.molsys is target and view.export_state() == state


def test_strict_loss_rejection_preserves_native_exception_and_source(view):
    # A real structure annotation cannot be represented by StructuresDict.
    view.molsys.structures.bioassembly = {"1": []}
    state = view.export_state()
    args = dict(to_form="molsysmt.StructuresDict", strict=True)
    report = view.addons.molsysmt.get_conversion_report(to_form=args["to_form"])
    assert report.is_lossy
    with pytest.raises(Exception) as native:
        msm.convert(view.molsys, **args)
    with pytest.raises(type(native.value)):
        view.addons.molsysmt.convert(**args)
    assert view.export_state() == state
    assert view.molsys.structures.bioassembly == {"1": []}
    assert view.addons.molsysmt.get_sync_status()["state"] == "synchronized"


@pytest.mark.parametrize(
    "name,args",
    [
        ("convert", {"structure_indices": [10000]}),
        ("convert", {"to_form": "molsysmt.MolSys", "copy_if_al": False}),
        ("convert", {"strict": "yes"}),
        ("get_conversion_report", {"structure_indices": [-1]}),
        ("copy", {"output_filename": "not-a-copy.pdb"}),
    ],
)
def test_native_rejection_without_scientific_or_scene_edit(view, name, args):
    status = view.addons.molsysmt.get_sync_status()
    with pytest.raises(Exception) as native:
        getattr(msm.basic, name)(view.molsys, **args)
    with pytest.raises(type(native.value)):
        getattr(view.addons.molsysmt, name)(**args)
    assert view.addons.molsysmt.get_sync_status() == status


def test_convert_rejects_override_without_file_output(view, tmp_path):
    path = tmp_path / "override.h5msm"
    with pytest.raises(TypeError, match="bound to view.molsys"):
        view.addons.molsysmt.convert(to_form=path, molecular_system=view.molsys)
    assert not path.exists()


def test_pending_edits_are_read_without_projecting_or_repeating_science(view):
    tools = view.addons.molsysmt
    values = msm.get(
        view.molsys, element="atom", structure_indices=[2], coordinates=True
    )
    tools.basic.set(
        structure_indices=[2],
        coordinates=values + puw.quantity(0.2, "nm"),
        update_view=False,
    )
    before = tools.get_sync_status()
    expected = msm.copy(view.molsys)
    _same_molecular_result(tools.copy(), expected)
    _same_molecular_result(tools.convert(), expected)
    assert tools.get_conversion_report() == msm.get_conversion_report(view.molsys)
    assert tools.get_sync_status() == before
    assert before["state"] == "pending"


def test_cached_operations_follow_replacement_and_closed_view_cannot_write(
    view, tmp_path
):
    tools = view.addons.molsysmt
    bound = [tools.copy, tools.convert, tools.get_conversion_report]
    with msv.demo["dialanine"] as source:
        view.load(source.molsys, mode="replace")
    assert bound[0]().get_n_atoms() == view.molsys.get_n_atoms()
    assert bound[1]().get_n_atoms() == view.molsys.get_n_atoms()
    assert bound[2]() == msm.get_conversion_report(view.molsys)
    view.close()
    path = tmp_path / "closed.h5msm"
    for method in bound:
        with pytest.raises(RuntimeError, match="closed view"):
            method(skip_digestion=True)
    with pytest.raises(RuntimeError, match="closed view"):
        bound[1](to_form=path)
    assert not path.exists()


def test_converter_option_validation_preserves_native_outcome(view, tmp_path):
    native_file = tmp_path / "native-compression.h5msm"
    bound_file = tmp_path / "bound-compression.h5msm"
    args = dict(to_form="file:h5msm", compression="gzip")
    # The native provider currently rejects this explicit default. Receive the
    # outcome without requiring that limitation to remain in future providers.
    try:
        native = msm.convert(view.molsys, output_filename=native_file, **args)
    except Exception as error:
        with pytest.raises(type(error)):
            view.addons.molsysmt.convert(output_filename=bound_file, **args)
        assert not native_file.exists() and not bound_file.exists()
    else:
        actual = view.addons.molsysmt.convert(output_filename=bound_file, **args)
        _same_molecular_result(msm.convert(actual), msm.convert(native))
