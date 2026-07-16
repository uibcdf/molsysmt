"""Testing canonical chemical-state fidelity for mmCIF containers."""

import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.form.mmcif_PdbxContainers_DataContainer._bond_state import (
    BondAccumulator,
    metadata_from_chem_comp_bond,
)
from molsysmt._private.conversion_report import build_conversion_report


def test_chem_comp_bond_order_and_aromaticity_are_independent():
    attributes = {
        'comp_id': 0,
        'atom_id_1': 1,
        'atom_id_2': 2,
        'value_order': 3,
        'pdbx_aromatic_flag': 4,
    }

    double = metadata_from_chem_comp_bond(['LIG', 'C1', 'O1', 'DOUB', 'N'], attributes)
    aromatic = metadata_from_chem_comp_bond(['LIG', 'C1', 'C2', 'AROM', 'Y'], attributes)

    assert double == {'bond_type': 'covalent', 'evidence': 'explicit', 'bond_order': 2}
    assert aromatic['is_aromatic'] is True
    assert 'bond_order' not in aromatic


def test_explicit_metadata_upgrades_inference_and_conflicts_fail_closed():
    bonds = BondAccumulator()
    bonds.add((2, 0), bond_type='covalent', evidence='inferred')
    bonds.add((0, 2), bond_order=1, bond_type='covalent', evidence='explicit')
    bonds.add((0, 2), bond_order=2, bond_type='covalent', evidence='explicit')

    table = bonds.to_dataframe()
    assert table.loc[0, 'evidence'] == 'explicit'
    assert pd.isna(table.loc[0, 'bond_order'])
    assert bonds.has_inference is True
    assert bonds.has_conflict is True


def test_altloc_remap_preserves_whole_bond_records():
    bonds = BondAccumulator()
    bonds.add((1, 3), bond_order=2, is_aromatic=True, evidence='explicit')

    remapped = bonds.remap([0, 1, 2], replacements={3: 2}).to_dataframe()

    assert remapped[['atom1_index', 'atom2_index']].values.tolist() == [[1, 2]]
    assert remapped.loc[0, 'bond_order'] == 2
    assert bool(remapped.loc[0, 'is_aromatic']) is True
    assert remapped.loc[0, 'evidence'] == 'explicit'


def test_real_container_preserves_orders_aromaticity_and_evidence(hp35_bcif_gz_file):
    container = msm.convert(
        str(hp35_bcif_gz_file),
        to_form='mmcif.PdbxContainers.DataContainer',
    )
    topology = msm.convert(container, to_form='molsysmt.Topology')

    assert set(topology.bonds['bond_order'].dropna().astype(int)) == {1, 2}
    assert topology.bonds['is_aromatic'].fillna(False).any()
    assert set(topology.bonds['evidence'].dropna()) == {'explicit', 'inferred'}
    assert topology._reference_chemical_state.connectivity_completeness == 'partial'


def test_unknown_order_code_is_reported_and_strictly_rejected():
    pytest.importorskip('mmcif')
    from mmcif.api.DataCategory import DataCategory
    from mmcif.api.PdbxContainers import DataContainer

    container = DataContainer('synthetic')
    container.append(DataCategory(
        'chem_comp_bond',
        attributeNameList=['comp_id', 'atom_id_1', 'atom_id_2', 'value_order'],
        rowList=[['LIG', 'C1', 'C2', 'UNKNOWN']],
    ))

    report = build_conversion_report(
        container,
        'mmcif.PdbxContainers.DataContainer',
        'molsysmt.Topology',
    )

    assert report.outcome == 'lossy'
    assert [issue.attribute for issue in report.issues] == ['bond_order']
    with pytest.raises(msm.NotCompatibleConversionError, match='Strict conversion'):
        msm.convert(container, to_form='molsysmt.Topology', strict=True)
