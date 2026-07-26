"""Testing exhaustive reports for direct native projection routes."""

import pytest

import molsysmt as msm
from molsysmt._private.conversion_report import (
    get_conversion_audit_scopes,
    is_conversion_audit_exhaustive,
)


@pytest.mark.parametrize(
    ('source_form', 'target_form'),
    [
        ('molsysmt.MolSys', 'molsysmt.Topology'),
        ('molsysmt.MolSys', 'molsysmt.Structures'),
        ('molsysmt.StructuresDict', 'molsysmt.MolSys'),
        ('molsysmt.StructuresDict', 'molsysmt.Topology'),
    ],
)
def test_direct_native_projection_profiles_are_statically_exhaustive(
    source_form,
    target_form,
):
    assert get_conversion_audit_scopes(source_form, target_form) == ('all',)
    assert is_conversion_audit_exhaustive(source_form, target_form)


@pytest.mark.parametrize(
    ('target_form', 'lost_attribute', 'scope'),
    [
        ('molsysmt.Topology', 'coordinates', 'structures'),
        ('molsysmt.Structures', 'atom_name', 'topology'),
    ],
)
def test_molsys_projection_reports_present_unsupported_domains(
    rich_molsys,
    target_form,
    lost_attribute,
    scope,
):
    _, report = msm.convert(
        rich_molsys,
        to_form=target_form,
        return_report=True,
    )

    assert report.audited_scopes == ('all',)
    assert report.is_exhaustive
    assert report.outcome == 'lossy'
    issues = {issue.attribute: issue for issue in report.issues}
    assert issues[lost_attribute].scope == scope

    with pytest.raises(
        msm.NotCompatibleConversionError,
        match=lost_attribute,
    ):
        msm.convert(rich_molsys, to_form=target_form, strict=True)


def test_structuresdict_to_molsys_reports_equivalent_exhaustive_projection(
    rich_molsys,
):
    source = msm.convert(
        rich_molsys.structures,
        to_form='molsysmt.StructuresDict',
    )

    target, report = msm.convert(
        source,
        to_form='molsysmt.MolSys',
        selection=[2, 0],
        structure_indices=[2, 0],
        return_report=True,
    )

    assert report.audited_scopes == ('all',)
    assert report.is_exhaustive
    assert report.outcome == 'equivalent'
    assert target.topology.n_atoms == target.structures.n_atoms == 2
    assert target.structures.n_structures == 2


def test_structuresdict_to_topology_reports_structural_loss(rich_molsys):
    source = msm.convert(
        rich_molsys.structures,
        to_form='molsysmt.StructuresDict',
    )

    _, report = msm.convert(
        source,
        to_form='molsysmt.Topology',
        return_report=True,
    )

    assert report.audited_scopes == ('all',)
    assert report.is_exhaustive
    assert report.outcome == 'lossy'
    issues = {issue.attribute: issue for issue in report.issues}
    assert issues['coordinates'].scope == 'structures'

    with pytest.raises(msm.NotCompatibleConversionError, match='coordinates'):
        msm.convert(source, to_form='molsysmt.Topology', strict=True)
