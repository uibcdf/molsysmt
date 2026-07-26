"""Testing native conversion-report scopes and schema losses."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.attribute import (
    is_chemical_state_attribute,
    is_structural_attribute,
    is_topological_attribute,
)


def _add_reduced_schema_losses(molsys):
    output = molsys.copy()
    msm.set(
        output,
        element='atom',
        selection=[0],
        formal_charge=[1],
    )
    msm.set(
        output,
        element='bond',
        selection=[0],
        fractional_bond_order=[1.5],
    )
    velocities = np.ones_like(
        puw.get_value(output.structures.coordinates, to_unit='nm')
    )
    output.structures.set_velocities(
        value=puw.quantity(velocities, 'nm/ps'),
        skip_digestion=True,
    )
    return output


def test_molsysdict_report_audits_native_scopes_and_detects_schema_losses(
    rich_molsys,
):
    source = _add_reduced_schema_losses(rich_molsys)

    _, report = msm.convert(
        source,
        to_form='molsysmt.MolSysDict',
        return_report=True,
    )

    assert report.audited_scopes == ('all',)
    assert report.is_exhaustive is True
    assert report.outcome == 'lossy'
    issues = {issue.attribute: issue for issue in report.issues}
    assert issues['formal_charge'].scope == 'chemical_state'
    assert issues['formal_charge'].kind == 'schema_limitation'
    assert issues['fractional_bond_order'].scope == 'chemical_state'
    assert issues['velocities'].scope == 'structures'


def test_strict_molsysdict_conversion_rejects_detected_nonchemical_loss(
    rich_molsys,
):
    source = _add_reduced_schema_losses(rich_molsys)

    with pytest.raises(msm.NotCompatibleConversionError, match='velocities'):
        msm.convert(
            source,
            to_form='molsysmt.MolSysDict',
            strict=True,
        )


def test_structuresdict_report_uses_structures_scope(rich_molsys):
    _, report = msm.convert(
        rich_molsys.structures,
        to_form='molsysmt.StructuresDict',
        return_report=True,
    )

    assert report.audited_scopes == ('all',)
    assert report.is_exhaustive is True
    assert report.outcome == 'equivalent'


def test_structuresdict_report_exhaustively_detects_bioassembly_loss(rich_molsys):
    source = rich_molsys.structures.copy()
    source.bioassembly = {
        '1': [
            {
                'chain_indices': [0],
                'rotations': [np.eye(3)],
                'translations': [np.zeros(3)],
            }
        ]
    }

    _, report = msm.convert(
        source,
        to_form='molsysmt.StructuresDict',
        return_report=True,
    )

    assert report.audited_scopes == ('all',)
    assert report.is_exhaustive is True
    assert report.outcome == 'lossy'
    assert [(issue.attribute, issue.scope) for issue in report.issues] == [
        ('bioassembly', 'structures')
    ]

    with pytest.raises(msm.NotCompatibleConversionError, match='bioassembly'):
        msm.convert(
            source,
            to_form='molsysmt.StructuresDict',
            strict=True,
        )


def test_topologydict_report_exhaustively_detects_rich_state_loss(rich_molsys):
    source = rich_molsys.topology.copy()
    msm.set(source, element='atom', selection=[0], formal_charge=[1])
    msm.set(
        source,
        element='bond',
        selection=[0],
        fractional_bond_order=[1.5],
    )

    _, report = msm.convert(
        source,
        to_form='molsysmt.TopologyDict',
        return_report=True,
    )

    assert report.audited_scopes == ('all',)
    assert report.is_exhaustive is True
    assert report.outcome == 'lossy'
    affected = {issue.attribute for issue in report.issues}
    assert {
        'formal_charge',
        'fractional_bond_order',
        'connectivity_completeness',
    } <= affected
    assert 'chemical_state_id' not in affected

    with pytest.raises(msm.NotCompatibleConversionError, match='formal_charge'):
        msm.convert(
            source,
            to_form='molsysmt.TopologyDict',
            strict=True,
        )


def test_atom_inventory_attributes_bridge_topology_and_structures():
    for attribute in ('atom_index', 'n_atoms'):
        assert is_topological_attribute(attribute)
        assert is_structural_attribute(attribute)
        assert not is_chemical_state_attribute(attribute)


def test_structuresdict_preserves_native_thermodynamic_series(rich_molsys):
    source = rich_molsys.structures.copy()
    source.temperature = puw.quantity(np.array([290.0, 295.0, 300.0]), 'K')
    source.potential_energy = puw.quantity(
        np.array([-10.0, -9.0, -8.0]), 'kJ/mol'
    )
    source.kinetic_energy = puw.quantity(
        np.array([2.0, 2.5, 3.0]), 'kJ/mol'
    )

    target, report = msm.convert(
        source,
        to_form='molsysmt.StructuresDict',
        return_report=True,
    )

    assert report.outcome == 'equivalent'
    assert np.allclose(puw.get_value(target['temperature'], to_unit='K'), [290, 295, 300])
    assert np.allclose(
        puw.get_value(target['potential_energy'], to_unit='kJ/mol'),
        [-10, -9, -8],
    )
    assert np.allclose(
        puw.get_value(target['kinetic_energy'], to_unit='kJ/mol'),
        [2, 2.5, 3],
    )
    assert np.allclose(
        puw.get_value(msm.get(target, total_energy=True), to_unit='kJ/mol'),
        [-8, -6.5, -5],
    )

    rebuilt = msm.convert(target, to_form='molsysmt.Structures')
    assert np.allclose(
        puw.get_value(rebuilt.temperature, to_unit='K'),
        [290, 295, 300],
    )
    assert np.allclose(
        puw.get_value(rebuilt.potential_energy, to_unit='kJ/mol'),
        [-10, -9, -8],
    )
    assert np.allclose(
        puw.get_value(rebuilt.kinetic_energy, to_unit='kJ/mol'),
        [2, 2.5, 3],
    )


def test_ordinary_conversion_bypasses_preflight_report(rich_molsys, monkeypatch):
    from molsysmt._private import conversion_report

    def fail_if_called(*args, **kwargs):
        raise AssertionError('conversion preflight should have been bypassed')

    monkeypatch.setattr(
        conversion_report,
        'build_conversion_report',
        fail_if_called,
    )

    output = msm.convert(rich_molsys, to_form='molsysmt.MolSys')
    assert msm.get_form(output) == 'molsysmt.MolSys'


def test_molsys_native_projections_are_exhaustive_and_reject_loss_in_strict_mode(
    rich_molsys,
):
    for to_form, lost_attribute in (
        ('molsysmt.Topology', 'coordinates'),
        ('molsysmt.Structures', 'atom_name'),
    ):
        _, report = msm.convert(
            rich_molsys,
            to_form=to_form,
            return_report=True,
        )

        assert report.audited_scopes == ('all',)
        assert report.is_exhaustive is True
        assert report.outcome == 'lossy'
        assert lost_attribute in {issue.attribute for issue in report.issues}

        with pytest.raises(msm.NotCompatibleConversionError, match=lost_attribute):
            msm.convert(rich_molsys, to_form=to_form, strict=True)


def test_builder_preserves_native_topology_and_structures_but_not_mechanics(
    rich_molsys,
):
    source = _add_reduced_schema_losses(rich_molsys)

    builder, report = msm.convert(
        source,
        to_form='molsysmt.MolSysBuilder',
        return_report=True,
    )

    assert report.is_exhaustive is True
    assert report.outcome == 'equivalent'
    formal_charge = msm.get(builder, formal_charge=True)
    assert formal_charge[0] == 1
    assert all(pd.isna(value) for value in formal_charge[1:])
    fractional_bond_order = msm.get(builder, fractional_bond_order=True)
    assert fractional_bond_order[0] == 1.5
    assert all(pd.isna(value) for value in fractional_bond_order[1:])
    assert puw.get_value(msm.get(builder, velocities=True), to_unit='nm/ps').shape == (
        3,
        4,
        3,
    )

    rebuilt, rebuilt_report = msm.convert(
        builder,
        to_form='molsysmt.MolSys',
        return_report=True,
    )
    assert rebuilt_report.is_exhaustive is True
    assert rebuilt_report.outcome == 'equivalent'
    rebuilt_formal_charge = msm.get(rebuilt, formal_charge=True)
    assert rebuilt_formal_charge[0] == 1
    assert all(pd.isna(value) for value in rebuilt_formal_charge[1:])

    source.molecular_mechanics.partial_charge = np.array([0.1, 0.2, -0.2, -0.1])
    source.molecular_mechanics.forcefield = 'test-forcefield'
    _, mechanics_report = msm.convert(
        source,
        to_form='molsysmt.MolSysBuilder',
        return_report=True,
    )
    assert mechanics_report.outcome == 'lossy'
    assert {'partial_charge', 'forcefield'} <= {
        issue.attribute for issue in mechanics_report.issues
    }
    with pytest.raises(msm.NotCompatibleConversionError, match='partial_charge'):
        msm.convert(source, to_form='molsysmt.MolSysBuilder', strict=True)


def test_builder_reports_explicit_multistate_structure_association_loss(rich_molsys):
    source = rich_molsys.copy()
    source.topology._append_chemical_state(state_id='alternate')
    source._set_structure_chemical_state_indices([0, 1, 1])

    builder, report = msm.convert(
        source,
        to_form='molsysmt.MolSysBuilder',
        return_report=True,
    )

    assert report.is_exhaustive is True
    assert report.outcome == 'lossy'
    issues = {(issue.attribute, issue.kind) for issue in report.issues}
    assert ('structure_chemical_state_index', 'state_association_loss') in issues
    assert msm.get(builder, n_chemical_states=True) == 2

    with pytest.raises(
        msm.NotCompatibleConversionError,
        match='structure_chemical_state_index',
    ):
        msm.convert(source, to_form='molsysmt.MolSysBuilder', strict=True)


def test_builder_and_molsysdict_selection_canonicalizes_atoms_and_orders_structures(
    rich_molsys,
):
    builder = msm.convert(rich_molsys, to_form='molsysmt.MolSysBuilder')
    selected_dict, report = msm.convert(
        builder,
        to_form='molsysmt.MolSysDict',
        selection=[2, 0],
        structure_indices=[2, 0],
        return_report=True,
    )

    assert report.is_exhaustive is True
    assert report.outcome == 'lossy'
    payload = selected_dict.to_dict(copy=False)
    assert [atom['atom_id'] for atom in payload['topology']['atoms']] == [
        '100',
        '102',
    ]
    assert payload['structures']['structure_id'] == [50, 10]

    rebuilt, rebuilt_report = msm.convert(
        selected_dict,
        to_form='molsysmt.MolSysBuilder',
        return_report=True,
    )
    assert rebuilt_report.is_exhaustive is True
    assert rebuilt_report.outcome == 'equivalent'
    assert msm.get(rebuilt, element='atom', atom_id=True) == ['100', '102']
    assert msm.get(rebuilt, structure_id=True) == ['50', '10']


def test_structuresdict_native_routes_are_exhaustive_and_subset_safe(rich_molsys):
    source = msm.convert(
        rich_molsys.structures,
        to_form='molsysmt.StructuresDict',
    )

    molsys, report = msm.convert(
        source,
        to_form='molsysmt.MolSys',
        selection=[2, 0],
        structure_indices=[2, 0],
        return_report=True,
    )
    assert report.is_exhaustive is True
    assert report.outcome == 'equivalent'
    assert msm.get(molsys, n_atoms=True) == 2
    assert msm.get(molsys, structure_id=True) == ['50', '10']
    assert puw.get_value(msm.get(molsys, coordinates=True), to_unit='nm').shape == (
        2,
        2,
        3,
    )

    topology, topology_report = msm.convert(
        source,
        to_form='molsysmt.Topology',
        selection=[2, 0],
        return_report=True,
    )
    assert topology.n_atoms == 2
    assert topology_report.is_exhaustive is True
    assert topology_report.outcome == 'lossy'
    assert 'coordinates' in {
        issue.attribute for issue in topology_report.issues
    }
    with pytest.raises(msm.NotCompatibleConversionError, match='coordinates'):
        msm.convert(source, to_form='molsysmt.Topology', strict=True)
