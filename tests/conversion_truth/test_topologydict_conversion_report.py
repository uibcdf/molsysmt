"""Testing exhaustive native Topology-to-TopologyDict preflight reports."""

import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.conversion_report import (
    _TOPOLOGY_TO_TOPOLOGY_DICT_PROFILE,
    get_conversion_audit_scopes,
    is_conversion_audit_exhaustive,
)
from molsysmt.native import Topology


def test_profile_partitions_the_declared_topology_contract():
    from molsysmt.form.molsysmt_Topology.attributes import attributes

    declared = {name for name, available in attributes.items() if available}
    profile = _TOPOLOGY_TO_TOPOLOGY_DICT_PROFILE
    classified = (
        profile['directly_preserved']
        | profile['derived_without_loss']
        | set(profile['covered_by_dependencies'])
        | set(profile['loss_candidates'])
    )

    assert classified == declared


def test_static_route_coverage_is_exhaustive():
    source = 'molsysmt.Topology'
    target = 'molsysmt.TopologyDict'

    assert get_conversion_audit_scopes(source, target) == ('all',)
    assert is_conversion_audit_exhaustive(source, target) is True


def test_minimal_topology_reports_equivalent_exhaustive_conversion():
    source = Topology(n_atoms=1, skip_digestion=True)

    _, report = msm.convert(
        source,
        to_form='molsysmt.TopologyDict',
        return_report=True,
    )

    assert report.audited_scopes == ('all',)
    assert report.is_exhaustive is True
    assert report.outcome == 'equivalent'
    assert report.issues == ()


def test_rich_state_losses_are_scoped_and_strictly_rejected(rich_molsys):
    source = rich_molsys.topology.copy()
    state = source._reference_chemical_state
    state.state_id = 'state-A'
    atom_columns = {
        'formal_charge': pd.array([1, 0, 0, -1], dtype='Int16'),
        'is_aromatic': pd.array([False, True, False, False], dtype='boolean'),
        'n_unpaired_electrons': pd.array([0, 1, 0, 0], dtype='UInt8'),
        'n_implicit_hydrogens': pd.array([0, 1, 0, 0], dtype='UInt8'),
        'allows_implicit_hydrogens': pd.array(
            [False, True, False, False],
            dtype='boolean',
        ),
        'stereochemistry': pd.array(
            ['unspecified', 'R', 'unspecified', 'unspecified'],
            dtype='string',
        ),
    }
    for column, values in atom_columns.items():
        source._set_chemical_state_atom_attribute(column, values)

    bonds = source._get_chemical_state_bonds()
    bond_columns = {
        'bond_id': pd.array(['b0', 'b1', 'b2'], dtype='string'),
        'fractional_bond_order': pd.array([1.5, pd.NA, pd.NA], dtype='Float64'),
        'is_aromatic': pd.array([True, False, False], dtype='boolean'),
        'is_conjugated': pd.array([True, False, False], dtype='boolean'),
        'stereochemistry': pd.array(['E', pd.NA, pd.NA], dtype='string'),
        'stereo_atom1_index': pd.array([0, pd.NA, pd.NA], dtype='Int64'),
        'stereo_atom2_index': pd.array([1, pd.NA, pd.NA], dtype='Int64'),
        'donor_atom_index': pd.array([0, pd.NA, pd.NA], dtype='Int64'),
        'acceptor_atom_index': pd.array([1, pd.NA, pd.NA], dtype='Int64'),
        'joins_components': pd.array([True, False, False], dtype='boolean'),
        'evidence': pd.array(['explicit', pd.NA, pd.NA], dtype='string'),
    }
    for column, values in bond_columns.items():
        bonds[column] = values

    _, report = msm.convert(
        source,
        to_form='molsysmt.TopologyDict',
        return_report=True,
    )

    affected = {issue.attribute for issue in report.issues}
    assert set(_TOPOLOGY_TO_TOPOLOGY_DICT_PROFILE['loss_candidates']) <= affected
    assert report.audited_scopes == ('all',)
    assert report.is_exhaustive is True
    assert report.outcome == 'lossy'
    assert all(issue.scope == 'chemical_state' for issue in report.issues)
    assert all(issue.kind == 'schema_limitation' for issue in report.issues)

    with pytest.raises(msm.NotCompatibleConversionError, match='formal_charge'):
        msm.convert(
            source,
            to_form='molsysmt.TopologyDict',
            strict=True,
        )


def test_aromatic_flag_is_only_preserved_without_formal_order():
    builder = msm.MolSysBuilder()
    atom_1 = builder.add_atom(atom_name='C')
    atom_2 = builder.add_atom(atom_name='C')
    builder.add_group([atom_1, atom_2], group_name='LIG')
    builder.add_bond(atom_1, atom_2, bond_order='aromatic')
    source = builder.build().topology

    _, report = msm.convert(
        source,
        to_form='molsysmt.TopologyDict',
        return_report=True,
    )
    assert 'bond_is_aromatic' not in {
        issue.attribute for issue in report.issues
    }

    bonds = source._get_chemical_state_bonds()
    bonds['bond_order'] = pd.array([1], dtype='UInt8')
    _, report = msm.convert(
        source,
        to_form='molsysmt.TopologyDict',
        return_report=True,
    )
    assert 'bond_is_aromatic' in {
        issue.attribute for issue in report.issues
    }


def test_multiple_states_report_inventory_collapse():
    source = Topology(n_atoms=1, skip_digestion=True)
    source._append_chemical_state(state_id='alternate')

    _, report = msm.convert(
        source,
        to_form='molsysmt.TopologyDict',
        return_report=True,
    )

    issues = {
        (issue.attribute, issue.kind, issue.scope)
        for issue in report.issues
    }
    assert (
        'chemical_state_index',
        'state_collapse',
        'chemical_state',
    ) in issues
