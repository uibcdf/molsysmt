"""Testing exhaustive native Structures-to-StructuresDict preflight reports."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.conversion_report import (
    _STRUCTURES_TO_STRUCTURES_DICT_PROFILE,
    get_conversion_audit_scopes,
    is_conversion_audit_exhaustive,
)
from molsysmt.native import Structures


def _structures():
    return Structures(
        structure_id=np.array([10]),
        time=puw.quantity(np.array([0.0]), 'ps'),
        coordinates=puw.quantity(np.zeros((1, 2, 3)), 'nm'),
        velocities=puw.quantity(np.ones((1, 2, 3)), 'nm/ps'),
        box=puw.quantity(np.eye(3)[None, :, :], 'nm'),
        b_factor=puw.quantity(np.ones((1, 2)), 'nm**2'),
        alternate_location=np.array([['', '']]),
        occupancy=np.ones((1, 2)),
        skip_digestion=True,
    )


def test_profile_partitions_the_declared_structures_contract():
    from molsysmt.form.molsysmt_Structures.attributes import attributes

    declared = {name for name, available in attributes.items() if available}
    profile = _STRUCTURES_TO_STRUCTURES_DICT_PROFILE
    classified = (
        profile['directly_preserved']
        | profile['derived_without_loss']
        | set(profile['covered_by_dependencies'])
        | set(profile['loss_candidates'])
    )

    assert classified == declared


def test_static_route_coverage_is_exhaustive():
    source = 'molsysmt.Structures'
    target = 'molsysmt.StructuresDict'

    assert get_conversion_audit_scopes(source, target) == ('all',)
    assert is_conversion_audit_exhaustive(source, target) is True


def test_preserved_payload_reports_equivalent_exhaustive_conversion():
    _, report = msm.convert(
        _structures(),
        to_form='molsysmt.StructuresDict',
        return_report=True,
    )

    assert report.audited_scopes == ('all',)
    assert report.is_exhaustive is True
    assert report.outcome == 'equivalent'
    assert report.issues == ()


def test_current_schema_losses_are_complete_and_scoped():
    source = _structures()
    source.bioassembly = {'1': []}
    source.temperature = puw.quantity(np.array([300.0]), 'K')
    source.potential_energy = puw.quantity(np.array([-10.0]), 'kJ/mol')
    source.kinetic_energy = puw.quantity(np.array([2.0]), 'kJ/mol')

    _, report = msm.convert(
        source,
        to_form='molsysmt.StructuresDict',
        return_report=True,
    )

    assert report.audited_scopes == ('all',)
    assert report.is_exhaustive is True
    assert report.outcome == 'lossy'
    assert [
        (issue.attribute, issue.kind, issue.scope)
        for issue in report.issues
    ] == [
        ('bioassembly', 'schema_limitation', 'structures'),
        ('temperature', 'schema_limitation', 'structures'),
        ('potential_energy', 'schema_limitation', 'structures'),
        ('kinetic_energy', 'schema_limitation', 'structures'),
    ]


def test_strict_conversion_rejects_structural_schema_loss():
    source = _structures()
    source.bioassembly = {'1': []}

    with pytest.raises(msm.NotCompatibleConversionError, match='bioassembly'):
        msm.convert(
            source,
            to_form='molsysmt.StructuresDict',
            strict=True,
        )
