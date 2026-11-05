"""Receive the published naming cutover without interpreting science in the addon."""

import inspect

import molsysviewer as msv
import pytest

import molsysmt as msm
from tests.molsysviewer_molsysmt.test_build_assignment_tools import (
    same,
    snapshot,
    unchanged,
)


def path(root, dotted):
    for name in dotted.split("."):
        root = getattr(root, name)
    return root


@pytest.mark.parametrize(
    "name",
    [
        "element.group.get_1_letter_code_from_name",
        "element.group.get_group_type_from_group_name",
        "element.group.get_bonded_atom_pairs",
        "element.group.amino_acid.get_standard_name",
        "element.group.amino_acid.is_amino_acid",
        "element.group.amino_acid.get_bonded_atom_pairs",
        "element.group.amino_acid.get_expected_heavy_atoms",
        "element.group.amino_acid.get_expected_hydrogens",
    ],
)
def test_changed_explicit_tools_match_native_parameters_and_digestion(name):
    with msv.new_view() as view:
        method = path(view.addons.molsysmt, name)
        assert inspect.signature(method) == inspect.signature(path(msm, name))
        assert method.digestion_plan is not None
        assert "naming_scheme :" in inspect.getdoc(method)
        assert view.molsys is None


def test_retired_code_path_is_absent_without_an_addon_alias():
    with msv.new_view() as view:
        group = view.addons.molsysmt.element.group
        assert "get_1_letter_code_from_name" in dir(group)
        assert "get_1_letter_code_from_name" not in dir(group.amino_acid)
        assert not hasattr(group.amino_acid, "get_1_letter_code_from_name")
        assert not hasattr(msm.element.group.amino_acid, "get_1_letter_code_from_name")


@pytest.mark.parametrize(
    "name,scheme,expected",
    [
        ("GLH", "amber", "E"),
        ("GLH", "legacy", "Q"),
        ("XLE", "sequence", "J"),
        ("MSE", "ccd", "M"),
    ],
)
@pytest.mark.parametrize("skip", [False, True])
def test_explicit_code_context_preserves_the_native_interpretation(
    name, scheme, expected, skip
):
    with msv.new_view() as view:
        method = view.addons.molsysmt.element.group.get_1_letter_code_from_name
        assert method(name, scheme, skip) == expected
        assert method(name, naming_scheme=scheme, skip_digestion=skip) == expected
        assert view.molsys is None


def test_missing_or_conflicting_context_retains_native_error_without_fallback():
    with msv.new_view() as view:
        method = view.addons.molsysmt.element.group.get_1_letter_code_from_name
        for name, scheme in [("GLH", None), ("HID", "ccd"), ("ALA", "unknown")]:
            with pytest.raises(Exception) as native:
                msm.element.group.get_1_letter_code_from_name(name, scheme)
            with pytest.raises(type(native.value)) as actual:
                method(name, scheme)
            assert str(actual.value) == str(native.value)


@pytest.mark.parametrize(
    "name,arguments",
    [
        ("element.group.get_group_type_from_group_name", {"group_name": "HID"}),
        ("element.group.amino_acid.get_standard_name", {"group_name": "GLH"}),
        ("element.group.amino_acid.is_amino_acid", {"name": "HID"}),
        ("element.group.amino_acid.get_expected_heavy_atoms", {"group_name": "GLH"}),
        ("element.group.amino_acid.get_expected_hydrogens", {"group_name": "GLH"}),
        (
            "element.group.get_bonded_atom_pairs",
            {"group_name": "GLH", "atom_names": ["CA", "CB"]},
        ),
        (
            "element.group.amino_acid.get_bonded_atom_pairs",
            {"group_name": "GLH", "atom_names": ["CA", "CB"]},
        ),
    ],
)
@pytest.mark.parametrize("scheme", ["amber", "ccd", "legacy"])
def test_template_and_predicate_context_errors_or_values_remain_native(
    name, arguments, scheme
):
    with msv.new_view() as view:
        native, method = path(msm, name), path(view.addons.molsysmt, name)
        parameters = {**arguments, "naming_scheme": scheme}
        try:
            expected = native(**parameters)
        except Exception as error:
            with pytest.raises(type(error)) as actual:
                method(**parameters)
            assert str(actual.value) == str(error)
        else:
            same(method(**parameters), expected)


def test_loaded_peptide_construction_uses_stored_context_and_preserves_ownership():
    molecular = msm.build.build_peptide("GLH", from_naming_scheme="amber")
    with msv.new_view(molecular) as view:
        method = view.addons.molsysmt.build.build_peptide
        native = inspect.signature(msm.build.build_peptide)
        assert inspect.signature(method) == native.replace(
            parameters=list(native.parameters.values())[1:]
        )
        before = snapshot(view)
        expected = msm.build.build_peptide(view.molsys)
        output = method()
        same(output, expected)
        assert "GLH" in msm.get(output, element="group", group_name=True)
        unchanged(view, before)
        with pytest.raises(Exception) as error:
            msm.build.build_peptide(view.molsys, from_naming_scheme="ccd")
        with pytest.raises(type(error.value)):
            method(from_naming_scheme="ccd")
        unchanged(view, before)
