"""Comparing declared component metadata without changing source storage."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import MolSys

puw = msm.pyunitwizard
FIELDS = ("component_id", "component_name", "component_type")


@pytest.fixture(params=["standard", "nondefault"])
def component_policy(request):
    units = (
        ["nm", "ps", "elementary_charge"]
        if request.param == "standard"
        else ["pm", "fs", "coulomb"]
    )
    with puw.context(standard_units=units):
        before = tuple(
            str(puw.get_unit(puw.standardize(puw.quantity(1, unit))))
            for unit in ("nm", "ps", "elementary_charge")
        )
        yield
        assert (
            tuple(
                str(puw.get_unit(puw.standardize(puw.quantity(1, unit))))
                for unit in ("nm", "ps", "elementary_charge")
            )
            == before
        )


@pytest.fixture
def source(component_policy):
    molsys = MolSys(n_atoms=3, n_components=2)
    msm.set(molsys, element="atom", component_index=[0, 0, 1])
    msm.set(
        molsys,
        element="component",
        component_id=[101, "W"],
        component_name=["fragment", None],
        component_type=["small molecule", "water"],
    )
    return molsys


@pytest.fixture(params=["native", "h5msm"])
def equivalent(source, request, tmp_path):
    if request.param == "native":
        return msm.copy(source)
    path = tmp_path / "components.h5msm"
    msm.h5msm.write(source, path)
    return msm.h5msm.read(path)


def _metadata(molsys):
    return msm.get(molsys, element="component", **dict.fromkeys(FIELDS, True))


@pytest.mark.parametrize("include_none", [False, True])
@pytest.mark.parametrize("output_type", ["boolean", "dictionary"])
def test_component_type_flags_preserve_equality_and_negation(
    source, equivalent, include_none, output_type
):
    expected = [["101", "W"], ["fragment", None], ["small molecule", "water"]]
    assert _metadata(source) == _metadata(equivalent) == expected
    tables = [
        item.chemical_states._states[0].components for item in (source, equivalent)
    ]
    snapshots = [table.copy(deep=True) for table in tables]

    for flag in (True, False):
        result = msm.compare(
            source,
            equivalent,
            component_type=flag,
            include_none=include_none,
            output_type=output_type,
        )
        assert result == (
            {"component_type": flag} if output_type == "dictionary" else flag
        )

    assert _metadata(source) == _metadata(equivalent) == expected
    for item, table, snapshot in zip((source, equivalent), tables, snapshots):
        assert item.chemical_states._states[0].components is table
        pd.testing.assert_frame_equal(table, snapshot)


@pytest.mark.parametrize("attribute", FIELDS)
@pytest.mark.parametrize("output_type", ["boolean", "dictionary"])
def test_component_comparison_detects_real_label_differences(
    source, equivalent, attribute, output_type
):
    before = _metadata(source)
    msm.set(equivalent, element="component", selection=[1], **{attribute: ["changed"]})
    for flag in (True, False):
        result = msm.compare(
            source,
            equivalent,
            **{attribute: flag},
            include_none=True,
            output_type=output_type,
        )
        expected = not flag
        assert result == (
            {attribute: expected} if output_type == "dictionary" else expected
        )
    assert _metadata(source) == before


def test_explicit_flag_accepts_the_reported_unknown_component_control(component_policy):
    molsys = MolSys(n_atoms=1)
    assert msm.compare(molsys, molsys, n_atoms=True, output_type="dictionary") == {
        "n_atoms": True
    }
    assert msm.compare(
        molsys, molsys, component_type=True, include_none=True, output_type="dictionary"
    ) == {"component_type": True}
    assert msm.compare(molsys, molsys, n_atoms=True, output_type="dictionary") == {
        "n_atoms": True
    }


@pytest.mark.parametrize("flag", [True, False])
def test_boolean_comparison_flags_do_not_become_setter_labels(source, flag):
    before = _metadata(source)
    with pytest.raises(msm.ArgumentError) as refusal:
        msm.set(source, element="component", component_type=flag)
    assert refusal.value.extra["argument"] == "component_type"
    assert _metadata(source) == before
    assert msm.get(source, element="component", component_type=True) == before[2]


@pytest.mark.parametrize("value", [0, 1, np.bool_(True), object()])
def test_unsupported_component_type_requests_keep_public_diagnostics(source, value):
    before = _metadata(source)
    with pytest.raises(msm.ArgumentError) as refusal:
        msm.compare(source, source, component_type=value)
    assert refusal.value.extra["argument"] == "component_type"
    assert refusal.value.extra["caller"] == "molsysmt.basic.compare.compare"
    assert _metadata(source) == before
