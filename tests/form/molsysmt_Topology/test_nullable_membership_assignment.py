"""Public stable-membership edits preserve nullable storage and independent rows."""

import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError


@pytest.mark.parametrize("form", ["molsysmt.MolSys", "molsysmt.Topology"])
@pytest.mark.parametrize(
    "element,attribute,table,values",
    [
        ("atom", "group_index", "atoms", [0, 0, 1, 1]),
        ("atom", "chain_index", "atoms", [0, 0, 1, 1]),
        ("group", "molecule_index", "groups", [0, 1]),
        ("molecule", "entity_index", "molecules", [0, 1]),
    ],
)
def test_public_complete_then_selected_missing_assignment_keeps_native_schema(
    nullable_membership_molsys, form, element, attribute, table, values
):
    molsys = nullable_membership_molsys
    source = molsys if form == "molsysmt.MolSys" else molsys.topology
    target = getattr(molsys.topology, table)
    others = target.drop(columns=[attribute]).copy(deep=True)
    msm.set(source, element=element, selection=[0], **{attribute: [None]})
    assert pd.isna(target.loc[0, attribute])
    msm.set(source, element=element, **{attribute: values})
    assert str(target[attribute].dtype) == "Int64"
    msm.set(
        source,
        element=element,
        selection=[len(values) - 1, 0],
        **{attribute: [None, 1]},
    )
    assert pd.isna(target.loc[len(values) - 1, attribute])
    assert target.loc[0, attribute] == 1
    assert str(target[attribute].dtype) == "Int64"
    pd.testing.assert_frame_equal(target.drop(columns=[attribute]), others)


@pytest.mark.parametrize("native", [False, True])
def test_reported_three_step_edit_remains_valid(nullable_membership_molsys, native):
    molsys = nullable_membership_molsys
    source = molsys.topology if native else molsys
    msm.set(source, element="atom", selection=[0], group_index=[None])
    msm.set(source, element="atom", group_index=[0, 0, 0, 0])
    msm.set(source, element="atom", selection=[0], group_index=[None])
    assert molsys.topology.atoms["group_index"].isna().tolist() == [
        True,
        False,
        False,
        False,
    ]


@pytest.mark.parametrize("native", [False, True])
@pytest.mark.parametrize("subset", [False, True])
@pytest.mark.parametrize(
    "element,attribute,table",
    [
        ("atom", "group_index", "atoms"),
        ("atom", "chain_index", "atoms"),
        ("group", "molecule_index", "groups"),
        ("molecule", "entity_index", "molecules"),
    ],
)
def test_invalid_membership_is_refused_before_publication(
    nullable_membership_molsys, native, subset, element, attribute, table
):
    molsys = nullable_membership_molsys
    source = molsys.topology if native else molsys
    target = getattr(molsys.topology, table)
    before = target.copy(deep=True)
    values = [0, 0.5] if subset else [0, 0.5] + [0] * (len(target) - 2)
    with pytest.raises(ArgumentError):
        msm.set(
            source,
            element=element,
            selection=[0, 1] if subset else "all",
            **{attribute: values},
        )
    pd.testing.assert_frame_equal(target, before)


@pytest.mark.parametrize("native", [False, True])
@pytest.mark.parametrize("subset", [False, True])
@pytest.mark.parametrize(
    "element,attribute,table",
    [
        ("atom", "group_index", "atoms"),
        ("atom", "chain_index", "atoms"),
        ("group", "molecule_index", "groups"),
        ("molecule", "entity_index", "molecules"),
    ],
)
def test_invalid_length_keeps_the_original_membership_column(
    nullable_membership_molsys, native, subset, element, attribute, table
):
    molsys = nullable_membership_molsys
    source = molsys.topology if native else molsys
    target = getattr(molsys.topology, table)
    before = target.copy(deep=True)
    values = [0, 0, 0] if subset else [0] * (len(target) + 1)
    with pytest.raises(ArgumentError):
        msm.set(
            source,
            element=element,
            selection=[0, 1] if subset else "all",
            **{attribute: values},
        )
    pd.testing.assert_frame_equal(target, before)


@pytest.mark.parametrize(
    "element,attribute,table,values,expected",
    [
        ("atom", "molecule_index", "groups", [None, None, 1, 1], [True, False]),
        ("atom", "entity_index", "molecules", [None, None, 1, 1], [True, False]),
        ("group", "entity_index", "molecules", [None, 1], [True, False]),
        ("molecule", "chain_index", "atoms", [None, 1], [True, True, False, False]),
        ("chain", "entity_index", "molecules", [None, 1], [True, False]),
    ],
)
def test_parent_projection_keeps_missing_values_and_nullable_storage(
    nullable_membership_molsys, element, attribute, table, values, expected
):
    molsys = nullable_membership_molsys
    msm.set(molsys, element=element, **{attribute: values})
    column = getattr(molsys.topology, table)[attribute]
    assert str(column.dtype) == "Int64"
    assert column.isna().tolist() == expected
    assert column.dropna().tolist() == [1] * expected.count(False)


def test_missing_chain_membership_preserves_declared_chain_inventory(
    nullable_membership_molsys,
):
    molsys = nullable_membership_molsys
    before = molsys.topology.chains.copy(deep=True)
    msm.set(molsys, element="atom", chain_index=[None, None, 1, 1])
    assert molsys.topology.atoms["chain_index"].isna().tolist() == [
        True,
        True,
        False,
        False,
    ]
    pd.testing.assert_frame_equal(molsys.topology.chains, before)


def test_unsupported_chain_to_molecule_assignment_keeps_its_public_refusal(
    nullable_membership_molsys,
):
    molsys = nullable_membership_molsys
    before = molsys.topology.groups.copy(deep=True)
    with pytest.raises(ArgumentError):
        msm.set(molsys, element="chain", molecule_index=[None, 1])
    pd.testing.assert_frame_equal(molsys.topology.groups, before)
