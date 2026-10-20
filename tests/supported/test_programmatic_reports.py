"""Check useful data outputs against public visual reports and real registries."""

import importlib

import pandas as pd
import pytest
from argdigest import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.form_tier import FORM_TIERS
from molsysmt._private.smonitor import ArgumentChoiceError, ArgumentError


@pytest.mark.parametrize("name", ["forms", "conversions", "syntaxes", "dependencies"])
def test_plain_outputs_preserve_visual_data_axes_and_order(name):
    report = getattr(msm.supported, name)
    expected = report().data
    plain = report(output_type="dataframe")
    pd.testing.assert_frame_equal(plain, expected)
    record = report(output_type="dictionary")
    assert set(record) == {"index", "columns", "data"}
    pd.testing.assert_frame_equal(pd.DataFrame(**record), plain)
    assert report(output_type="dataframe") is not plain


def test_public_form_enumeration_agrees_with_the_declared_tier_registry(monkeypatch):
    monkeypatch.setattr(msm.configure, "show_all_capabilities", True)
    names = msm.supported.forms(output_type="list")
    assert len(names) == len(set(names))
    assert set(names) == set(FORM_TIERS)
    table = msm.supported.forms(output_type="dataframe")
    assert names == table["Form"].tolist()
    for category in ("file", "class", "string"):
        expected = table.loc[table["Type"] == category, "Form"].tolist()
        assert msm.supported.forms(category, output_type="list") == expected


def test_mutating_programmatic_metadata_cannot_edit_the_form_declaration():
    first = msm.supported.forms(output_type="dataframe")
    index = next(i for i, value in first["Info"].items() if isinstance(value, list))
    original = first.at[index, "Info"][:]
    first.at[index, "Info"].append("mutated consumer metadata")
    second = msm.supported.forms(output_type="dataframe")
    assert second.at[index, "Info"] == original
    record = msm.supported.forms(output_type="dictionary")
    record["data"][0][0] = "not a declared form"
    assert "not a declared form" not in msm.supported.forms(output_type="list")


@pytest.mark.parametrize("orientation", ["from", "to"])
def test_literal_conversion_routes_and_empty_axes(orientation):
    source = ["molsysmt.MolSys", "molsysmt.MolSys"]
    target = ["molsysmt.Topology", "unknown:destination"]
    table = msm.supported.conversions(
        source, target, as_rows=orientation, output_type="dataframe"
    )
    expected = pd.DataFrame([[True, False]], index=["molsysmt.MolSys"], columns=target)
    if orientation == "to":
        expected = expected.T
    pd.testing.assert_frame_equal(table, expected)
    empty = msm.supported.conversions(
        [], target, as_rows=orientation, output_type="dataframe"
    )
    assert empty.shape == ((0, 2) if orientation == "from" else (2, 0))
    assert (empty.columns if orientation == "from" else empty.index).tolist() == target
    record = msm.supported.conversions(
        source, [], as_rows=orientation, output_type="dictionary"
    )
    assert len(record["index"] if orientation == "from" else record["columns"]) == 1


def test_filters_and_compatibility_syntax_module_keep_the_output_contract():
    table = msm.supported.conversions(
        to_viewer="NGLView", from_form_type="file", output_type="dataframe"
    )
    assert table.columns.tolist() == ["nglview.NGLWidget"]
    assert set(table.index) == set(msm.supported.forms("file", output_type="list"))
    importlib.import_module("molsysmt.supported.syntaxes")
    assert "Syntax" in msm.supported.syntaxes(output_type="dictionary")["columns"]


@pytest.mark.parametrize("name", ["forms", "conversions", "syntaxes", "dependencies"])
def test_invalid_outputs_and_unknown_keywords_are_validated(name):
    report = getattr(msm.supported, name)
    with pytest.raises(ArgumentError, match="output_type"):
        report(output_type="unsupported")
    with pytest.raises(UnknownArgumentError):
        report(undeclared_filter=True)


def test_programmatic_reports_do_not_construct_a_styler(monkeypatch):
    def reject_rendering(table):
        raise AssertionError("A data report must not construct its visual wrapper.")

    monkeypatch.setattr(pd.DataFrame, "style", property(reject_rendering))
    assert "molsysmt.MolSys" in msm.supported.forms(output_type="list")
    for name in ("forms", "conversions", "syntaxes", "dependencies"):
        assert isinstance(getattr(msm.supported, name)(output_type="dictionary"), dict)


@pytest.mark.parametrize(
    "options",
    [{"from_viewer": "unknown"}, {"as_rows": "sideways"}, {"to_form_type": "unknown"}],
)
def test_invalid_conversion_filters_have_actionable_choice_errors(options):
    with pytest.raises(ArgumentChoiceError):
        msm.supported.conversions(**options)
