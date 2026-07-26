import numpy as np
import pandas as pd
import pytest
from importlib import import_module
from importlib.resources import files

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.form.file_pdb.has_atoms_with_alternate_locations import (
    has_atoms_with_alternate_locations,
)


PDB_WITH_ALTERNATE_LOCATIONS = str(files('molsysmt.data.pdb').joinpath('1bnf.pdb'))


def _pdb_atom_line(serial, atom_name, group_name, chain_id, group_id,
                   coordinates, element, charge='  ', insertion_code=' '):
    x, y, z = coordinates
    return (
        f"ATOM  {serial:>5} {atom_name:<4} {group_name:>3} {chain_id:1}"
        f"{group_id:>4}{insertion_code:1}   {x:>8.3f}{y:>8.3f}{z:>8.3f}"
        f"{1.0:>6.2f}{10.0:>6.2f}{'':10}{element:>2}{charge:>2}\n"
    )


def _pdb_link_line(atom1, group1, chain1, group_id1,
                   atom2, group2, chain2, group_id2):
    line = [' '] * 80
    line[0:6] = 'LINK  '
    line[12:16] = f'{atom1:<4}'
    line[17:20] = f'{group1:>3}'
    line[21] = chain1
    line[22:26] = f'{group_id1:>4}'
    line[42:46] = f'{atom2:<4}'
    line[47:50] = f'{group2:>3}'
    line[51] = chain2
    line[52:56] = f'{group_id2:>4}'
    line[73:78] = f'{2.0:>5.2f}'
    return ''.join(line) + '\n'


def _pdb_ssbond_line(chain1, group_id1, chain2, group_id2):
    line = [' '] * 80
    line[0:6] = 'SSBOND'
    line[7:10] = f'{1:>3}'
    line[11:14] = 'CYS'
    line[15] = chain1
    line[17:21] = f'{group_id1:>4}'
    line[25:28] = 'CYS'
    line[29] = chain2
    line[31:35] = f'{group_id2:>4}'
    line[73:78] = f'{2.0:>5.2f}'
    return ''.join(line) + '\n'


def _with_pdb_scalar_fields(molsys):
    output = molsys.copy()
    output.topology.atoms['atom_id'] = ['7', '7', 'label', '7']
    output.structures.occupancy = np.array(
        [
            [0.11, 0.22, 0.33, 0.44],
            [0.51, 0.62, 0.73, 0.84],
            [0.91, 0.82, 0.73, 0.64],
        ]
    )
    output.structures.b_factor = puw.quantity(
        np.array(
            [
                [0.010, 0.020, 0.030, 0.040],
                [0.050, 0.060, 0.070, 0.080],
                [0.090, 0.100, 0.110, 0.120],
            ]
        ),
        'nm**2',
    )
    return output


def test_native_pdb_roundtrip_uses_canonical_serials_and_preserves_scalar_fields(
    rich_molsys,
):
    source = _with_pdb_scalar_fields(rich_molsys)

    pdb_text = msm.convert(
        source,
        to_form='string:pdb_text',
        selection=[2, 0],
        structure_indices=[2, 0],
    )
    restored = msm.convert(
        pdb_text,
        to_form='molsysmt.MolSys',
        get_missing_bonds=False,
    )

    atom_lines = [line for line in pdb_text.splitlines() if line.startswith('ATOM')]
    assert [line[6:11].strip() for line in atom_lines[:2]] == ['1', '2']
    assert restored.topology.atoms['atom_id'].tolist() == ['1', '2']
    assert restored.structures.structure_id.tolist() == ['50', '10']
    np.testing.assert_allclose(
        puw.get_value(restored.structures.coordinates, to_unit='nm'),
        puw.get_value(source.structures.coordinates, to_unit='nm')[[2, 0]][:, [0, 2]],
        atol=5.1e-5,
    )
    np.testing.assert_allclose(
        restored.structures.occupancy,
        source.structures.occupancy[[2, 0]][:, [0, 2]],
        atol=0.0051,
    )
    np.testing.assert_allclose(
        puw.get_value(restored.structures.b_factor, to_unit='nm**2'),
        puw.get_value(source.structures.b_factor, to_unit='nm**2')[[2, 0]][:, [0, 2]],
        atol=5.1e-5,
    )
    assert restored.topology._get_chemical_state_bonds()[
        ['atom1_index', 'atom2_index']
    ].values.tolist() == [[0, 1]]


def test_file_pdb_and_handler_share_the_same_subset_contract(rich_molsys, tmp_path):
    source = _with_pdb_scalar_fields(rich_molsys)
    filename = tmp_path / 'subset.pdb'
    msm.convert(
        source,
        to_form='file:pdb',
        output_filename=str(filename),
        selection=[0, 2],
        structure_indices=[2, 0],
    )

    from_file = msm.convert(
        str(filename),
        to_form='molsysmt.MolSys',
        get_missing_bonds=False,
    )
    handler = msm.convert(str(filename), to_form='molsysmt.PDBFileHandler')
    try:
        from_handler = msm.convert(
            handler,
            to_form='molsysmt.MolSys',
            get_missing_bonds=False,
        )
    finally:
        handler.close()

    for restored in (from_file, from_handler):
        assert restored.structures.structure_id.tolist() == ['50', '10']
        np.testing.assert_allclose(
            restored.structures.occupancy,
            source.structures.occupancy[[2, 0]][:, [0, 2]],
            atol=0.0051,
        )


def test_pdb_preflight_inspects_only_the_requested_payload(rich_molsys):
    source = rich_molsys.copy()
    source.topology.atoms['atom_id'] = ['1', '2', 'bad', 'bad']

    _, selected_report = msm.convert(
        source,
        to_form='string:pdb_text',
        selection=[0, 1],
        structure_indices=[0],
        return_report=True,
    )
    _, full_report = msm.convert(
        source,
        to_form='string:pdb_text',
        return_report=True,
    )

    assert 'atom_id' not in {issue.attribute for issue in selected_report.issues}
    assert 'box' not in {issue.attribute for issue in selected_report.issues}
    assert 'atom_id' in {issue.attribute for issue in full_report.issues}
    assert 'box' in {issue.attribute for issue in full_report.issues}


def test_pdb_preflight_reports_invalid_model_ids_and_writer_canonicalizes_them(
    rich_molsys,
):
    source = rich_molsys.copy()
    source.structures.structure_id = np.array(['frame-a', 'frame-a', '10000'])

    pdb_text, report = msm.convert(
        source,
        to_form='string:pdb_text',
        return_report=True,
    )
    restored = msm.convert(
        pdb_text,
        to_form='molsysmt.Structures',
    )

    assert any(
        issue.attribute == 'structure_id' and issue.kind == 'canonicalization'
        for issue in report.issues
    )
    assert restored.structure_id.tolist() == ['1', '2', '3']


def test_strict_pdb_write_rejects_before_creating_a_lossy_file(rich_molsys, tmp_path):
    filename = tmp_path / 'strict.pdb'

    with pytest.raises(msm.NotCompatibleConversionError):
        msm.convert(
            rich_molsys,
            to_form='file:pdb',
            output_filename=str(filename),
            strict=True,
        )

    assert not filename.exists()


def test_pdb_numeric_capacity_is_reported_and_rejected(rich_molsys):
    source = rich_molsys.copy()
    coordinates = puw.get_value(source.structures.coordinates, to_unit='nm').copy()
    coordinates[0, 3, 0] = 2000.0
    source.structures.coordinates = puw.quantity(coordinates, 'nm')

    _, selected_report = msm.convert(
        source,
        to_form='string:pdb_text',
        selection=[0, 1],
        structure_indices=[0],
        return_report=True,
    )
    assert 'coordinates' not in {
        issue.attribute for issue in selected_report.issues
    }

    with pytest.raises(msm.NotCompatibleConversionError, match='fixed-width'):
        msm.convert(
            source,
            to_form='string:pdb_text',
            structure_indices=[0],
        )


def test_native_pdb_write_reports_are_exhaustive_for_both_targets(
    rich_molsys,
    tmp_path,
):
    for target in ('string:pdb_text', str(tmp_path / 'reported.pdb')):
        output, report = msm.convert(
            rich_molsys,
            to_form=target,
            selection=[0, 2],
            structure_indices=[2, 0],
            return_report=True,
        )

        assert output is not None
        assert report.audited_scopes == ('all',)
        assert report.is_exhaustive is True
        assert report.outcome == 'lossy'


def test_pdb_reader_materializes_alternate_locations_as_canonical_atom_sites():
    alternate_locations = msm.get(
        PDB_WITH_ALTERNATE_LOCATIONS,
        alternate_location=True,
    )
    restored = msm.convert(
        PDB_WITH_ALTERNATE_LOCATIONS,
        to_form='molsysmt.MolSys',
        get_missing_bonds=False,
    )

    assert restored.topology.n_atoms == 2747
    assert len(alternate_locations[0]) == 24
    assert alternate_locations[0]['480']['location_id'].tolist() == ['A', 'B']
    assert restored.structures.coordinates.shape == (1, 2747, 3)
    assert len(restored.structures.alternate_location[0]) == 24

    alternate = restored.structures.alternate_location[0][480]
    assert alternate['location_id'].tolist() == ['A', 'B']
    assert alternate['atom_id'].tolist() == ['481', '482']
    np.testing.assert_allclose(alternate['occupancy'], [0.5, 0.5])
    assert str(puw.get_unit(alternate['coordinates'])) == 'nanometer'
    assert str(puw.get_unit(alternate['b_factor'])) == 'nanometer ** 2'
    assert restored.topology.atoms.iloc[480]['atom_id'] == '481'
    np.testing.assert_allclose(
        puw.get_value(restored.structures.coordinates[0, 480], to_unit='nm'),
        puw.get_value(alternate['coordinates'][0], to_unit='nm'),
    )


def test_pdb_alternate_locations_survive_selection_and_native_roundtrip():
    source = msm.convert(
        PDB_WITH_ALTERNATE_LOCATIONS,
        to_form='molsysmt.MolSys',
        selection=[479, 480],
        get_missing_bonds=False,
    )

    assert list(source.structures.alternate_location[0]) == [1]

    pdb_text, report = msm.convert(
        source,
        to_form='string:pdb_text',
        return_report=True,
    )
    assert 'alternate_location' not in {issue.attribute for issue in report.issues}
    atom_lines = [line for line in pdb_text.splitlines() if line.startswith('ATOM  ')]
    assert len(atom_lines) == 3
    assert [line[16] for line in atom_lines] == [' ', 'A', 'B']

    restored = msm.convert(
        pdb_text,
        to_form='molsysmt.MolSys',
        get_missing_bonds=False,
    )
    alternate = restored.structures.alternate_location[0][1]
    assert restored.topology.n_atoms == 2
    assert alternate['location_id'].tolist() == ['A', 'B']
    np.testing.assert_allclose(alternate['occupancy'], [0.5, 0.5])
    np.testing.assert_allclose(
        puw.get_value(alternate['coordinates'], to_unit='nm'),
        puw.get_value(source.structures.alternate_location[0][1]['coordinates'], to_unit='nm'),
        atol=5.1e-5,
    )


def test_file_pdb_reports_presence_of_alternate_locations(tmp_path):
    assert (
        has_atoms_with_alternate_locations(PDB_WITH_ALTERNATE_LOCATIONS)
        is True
    )

    pdb_without_alternates = tmp_path / 'without_alternates.pdb'
    pdb_without_alternates.write_text(
        'ATOM      1 CA   ALA A   1       0.000   0.000   0.000  1.00 10.00           C\n'
        'END\n'
    )
    assert (
        has_atoms_with_alternate_locations(str(pdb_without_alternates))
        is False
    )


def test_pdb_conect_serials_for_variants_map_to_the_canonical_atom_site():
    pdb_text = (
        'ATOM      1 CA  AALA A   1       0.000   0.000   0.000  0.60 10.00           C\n'
        'ATOM      2 CA  BALA A   1       1.000   0.000   0.000  0.40 11.00           C\n'
        'ATOM      3 C    ALA A   1       0.000   1.000   0.000  1.00 12.00           C\n'
        'CONECT    2    3\n'
        'END\n'
    )

    restored = msm.convert(
        pdb_text,
        to_form='molsysmt.MolSys',
        get_missing_bonds=False,
    )

    assert restored.topology.n_atoms == 2
    assert restored.topology._get_chemical_state_bonds()[
        ['atom1_index', 'atom2_index']
    ].values.tolist() == [[0, 1]]


def test_pdb_multimodel_alternate_locations_share_a_canonical_atom_axis():
    pdb_text = (
        'MODEL        1\n'
        'ATOM      1 CA  AALA A   1       0.000   0.000   0.000  0.60 10.00           C\n'
        'ATOM      2 CA  BALA A   1       1.000   0.000   0.000  0.40 11.00           C\n'
        'ATOM      3 C    ALA A   1       0.000   1.000   0.000  1.00 12.00           C\n'
        'ENDMDL\n'
        'MODEL        2\n'
        'ATOM      1 CA  AALA A   1       2.000   0.000   0.000  0.30 13.00           C\n'
        'ATOM      2 CA  BALA A   1       3.000   0.000   0.000  0.70 14.00           C\n'
        'ATOM      3 C    ALA A   1       2.000   1.000   0.000  1.00 15.00           C\n'
        'ENDMDL\n'
        'END\n'
    )

    restored = msm.convert(
        pdb_text,
        to_form='molsysmt.MolSys',
        get_missing_bonds=False,
    )

    assert restored.topology.n_atoms == 2
    assert restored.structures.coordinates.shape == (2, 2, 3)
    assert restored.structures.structure_id.tolist() == ['1', '2']
    assert [list(item) for item in restored.structures.alternate_location] == [[0], [0]]
    assert restored.structures.alternate_location[0][0]['location_id'].tolist() == [
        'A',
        'B',
    ]
    restored.structures.coordinates = puw.quantity(
        np.zeros((2, 2, 3), dtype=float), 'nm'
    )
    msm.build.solve_atoms_with_alternate_location(restored)
    np.testing.assert_allclose(
        puw.get_value(restored.structures.coordinates[:, 0], to_unit='nm'),
        [[0.0, 0.0, 0.0], [0.3, 0.0, 0.0]],
    )

    roundtrip = msm.convert(
        msm.convert(restored, to_form='string:pdb_text'),
        to_form='molsysmt.MolSys',
        get_missing_bonds=False,
    )
    assert roundtrip.structures.coordinates.shape == (2, 2, 3)
    assert [list(item) for item in roundtrip.structures.alternate_location] == [[0], [0]]


def test_pdb_formal_charge_and_link_are_imported_as_explicit_chemical_state_data():
    pdb_text = (
        _pdb_atom_line(1, 'ZN', 'ZN', 'A', 1, (0.0, 0.0, 0.0), 'ZN', '2+')
        + _pdb_atom_line(2, 'ND1', 'HIS', 'A', 2, (2.0, 0.0, 0.0), 'N')
        + _pdb_link_line('ZN', 'ZN', 'A', 1, 'ND1', 'HIS', 'A', 2)
        + 'END\n'
    )

    restored = msm.convert(
        pdb_text, to_form='molsysmt.MolSys', get_missing_bonds=False
    )

    formal_charge = restored.topology._get_chemical_state_atom_attribute(
        'formal_charge'
    )
    assert formal_charge.iloc[0] == 2
    assert pd.isna(formal_charge.iloc[1])
    bonds = restored.topology._get_chemical_state_bonds()
    assert bonds[['atom1_index', 'atom2_index']].values.tolist() == [[0, 1]]
    assert bonds['bond_type'].tolist() == ['covalent']
    assert bonds['evidence'].tolist() == ['explicit']
    assert restored.topology._reference_chemical_state.connectivity_completeness == 'partial'

    roundtrip = msm.convert(
        msm.convert(restored, to_form='string:pdb_text'),
        to_form='molsysmt.MolSys',
        get_missing_bonds=False,
    )
    assert roundtrip.topology._get_chemical_state_atom_attribute(
        'formal_charge'
    ).iloc[0] == 2


def test_pdb_ssbond_is_imported_as_an_explicit_covalent_bond():
    pdb_text = (
        _pdb_ssbond_line('A', 1, 'B', 2)
        + _pdb_atom_line(1, 'SG', 'CYS', 'A', 1, (0.0, 0.0, 0.0), 'S')
        + 'TER\n'
        + _pdb_atom_line(2, 'SG', 'CYS', 'B', 2, (2.0, 0.0, 0.0), 'S')
        + 'END\n'
    )

    restored = msm.convert(
        pdb_text, to_form='molsysmt.MolSys', get_missing_bonds=False
    )
    bonds = restored.topology._get_chemical_state_bonds()

    assert bonds[['atom1_index', 'atom2_index']].values.tolist() == [[0, 1]]
    assert bonds['evidence'].tolist() == ['explicit']


def test_pdb_bioassembly_is_parsed_remapped_and_roundtripped(tmp_path):
    pdb_text = (
        'REMARK 350 BIOMOLECULE: 1\n'
        'REMARK 350 APPLY THE FOLLOWING TO CHAINS: A\n'
        'REMARK 350   BIOMT1   1  1.000000  0.000000  0.000000        1.00000\n'
        'REMARK 350   BIOMT2   1  0.000000  1.000000  0.000000        0.00000\n'
        'REMARK 350   BIOMT3   1  0.000000  0.000000  1.000000        0.00000\n'
        + _pdb_atom_line(1, 'CA', 'ALA', 'A', 1, (0.0, 0.0, 0.0), 'C')
        + 'TER\n'
        + _pdb_atom_line(2, 'CA', 'ALA', 'B', 1, (2.0, 0.0, 0.0), 'C')
        + 'END\n'
    )

    restored = msm.convert(
        pdb_text, to_form='molsysmt.MolSys', get_missing_bonds=False
    )
    bioassembly = restored.structures.bioassembly['1']
    assert bioassembly['chain_indices'] == [0]
    np.testing.assert_allclose(bioassembly['rotations'][0], np.eye(3))
    np.testing.assert_allclose(
        puw.get_value(bioassembly['translations'][0], to_unit='nm'),
        [0.1, 0.0, 0.0],
    )

    filename = tmp_path / 'bioassembly.pdb'
    filename.write_text(pdb_text)
    handler = msm.convert(str(filename), to_form='molsysmt.PDBFileHandler')
    try:
        for source in (str(filename), pdb_text, handler):
            structures = msm.convert(
                source,
                to_form='molsysmt.Structures',
                selection=[0],
            )
            assert structures.bioassembly['1']['chain_indices'] == [0]
    finally:
        handler.close()

    assert restored.extract(atom_indices=[1]).structures.bioassembly is None
    selected = restored.extract(atom_indices=[0])
    assert selected.structures.bioassembly['1']['chain_indices'] == [0]

    roundtrip = msm.convert(
        msm.convert(selected, to_form='string:pdb_text'),
        to_form='molsysmt.MolSys',
        get_missing_bonds=False,
    )
    assert roundtrip.structures.bioassembly['1']['chain_indices'] == [0]
    np.testing.assert_allclose(
        puw.get_value(
            roundtrip.structures.bioassembly['1']['translations'][0],
            to_unit='nm',
        ),
        [0.1, 0.0, 0.0],
    )


def test_pdb_writer_accepts_native_list_of_bioassembly_translations(
    hp35_bcif_gz_file,
):
    source = msm.convert(
        str(hp35_bcif_gz_file),
        to_form='molsysmt.MolSys',
    )
    translations = source.structures.bioassembly['1']['translations']

    assert isinstance(translations, list)
    assert len(translations) == 1

    pdb_text = msm.convert(source, to_form='string:pdb_text')

    assert 'REMARK 350 BIOMOLECULE: 1' in pdb_text
    assert 'REMARK 350   BIOMT1   1' in pdb_text


def test_all_nine_pdb_read_routes_have_exhaustive_content_aware_reports(tmp_path):
    pdb_text = (
        _pdb_atom_line(1, 'N', 'ALA', 'A', 1, (0.0, 0.0, 0.0), 'N')
        + _pdb_atom_line(2, 'CA', 'ALA', 'A', 1, (1.0, 0.0, 0.0), 'C')
        + 'END\n'
    )
    filename = tmp_path / 'audited.pdb'
    filename.write_text(pdb_text)
    handler = msm.convert(str(filename), to_form='molsysmt.PDBFileHandler')
    try:
        for source in (str(filename), pdb_text, handler):
            for target in (
                'molsysmt.MolSys',
                'molsysmt.Topology',
                'molsysmt.Structures',
            ):
                _, report = msm.convert(
                    source,
                    to_form=target,
                    get_missing_bonds=False,
                    return_report=True,
                )
                assert report.audited_scopes == ('all',)
                assert report.is_exhaustive is True
                assert report.outcome == (
                    'equivalent' if target == 'molsysmt.MolSys' else 'lossy'
                )
    finally:
        handler.close()


def test_pdb_reader_report_limits_insertion_code_loss_to_the_selected_payload():
    pdb_text = (
        _pdb_atom_line(1, 'CA', 'ALA', 'A', 1, (0.0, 0.0, 0.0), 'C')
        + _pdb_atom_line(
            2, 'CA', 'GLY', 'A', 2, (1.0, 0.0, 0.0), 'C', insertion_code='A'
        )
        + 'END\n'
    )

    _, selected_report = msm.convert(
        pdb_text,
        to_form='molsysmt.MolSys',
        selection=[0],
        get_missing_bonds=False,
        return_report=True,
    )
    _, full_report = msm.convert(
        pdb_text,
        to_form='molsysmt.MolSys',
        get_missing_bonds=False,
        return_report=True,
    )

    assert 'group_id' not in {issue.attribute for issue in selected_report.issues}
    assert any(
        issue.attribute == 'group_id' and issue.kind == 'adapter_limitation'
        for issue in full_report.issues
    )


def test_pdb_openmm_discovered_bonds_are_marked_as_inferred(monkeypatch):
    pdb_text = (
        _pdb_atom_line(1, 'N', 'ALA', 'A', 1, (0.0, 0.0, 0.0), 'N')
        + _pdb_atom_line(2, 'CA', 'ALA', 'A', 1, (1.0, 0.0, 0.0), 'C')
        + 'END\n'
    )
    converter = import_module(
        'molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_MolSys'
    )
    monkeypatch.setattr(
        converter,
        '_get_bonded_atom_pairs_from_openmm_pdb',
        lambda item: [(0, 1)],
    )

    restored = msm.convert(
        pdb_text, to_form='molsysmt.MolSys', get_missing_bonds=True
    )
    bonds = restored.topology._get_chemical_state_bonds()

    assert bonds[['atom1_index', 'atom2_index']].values.tolist() == [[0, 1]]
    assert bonds['evidence'].tolist() == ['inferred']


def test_pdb_report_exposes_ambiguous_explicit_bond_endpoints():
    pdb_text = (
        _pdb_link_line('CA', 'ALA', 'A', 1, 'CA', 'ALA', 'A', 1)
        + _pdb_atom_line(1, 'CA', 'ALA', 'A', 1, (0.0, 0.0, 0.0), 'C')
        + 'TER\n'
        + _pdb_atom_line(2, 'CA', 'ALA', 'A', 1, (2.0, 0.0, 0.0), 'C')
        + 'END\n'
    )

    restored, report = msm.convert(
        pdb_text,
        to_form='molsysmt.MolSys',
        get_missing_bonds=False,
        return_report=True,
    )

    assert restored.topology.n_bonds == 0
    assert any(
        issue.attribute == 'bonded_atoms'
        and issue.kind == 'adapter_limitation'
        for issue in report.issues
    )


def test_pdb_formal_charge_capacity_is_reported_and_rejected(rich_molsys):
    source = rich_molsys.copy()
    source.topology._set_chemical_state_atom_attribute(
        'formal_charge', pd.array([10, 0, 0, 0], dtype='Int16')
    )

    with pytest.raises(msm.NotCompatibleConversionError, match='magnitudes'):
        msm.convert(source, to_form='string:pdb_text')

    with pytest.raises(msm.NotCompatibleConversionError):
        msm.convert(source, to_form='string:pdb_text', strict=True)

    _, report = msm.convert(
        source,
        to_form='string:pdb_text',
        selection=[1, 2],
        return_report=True,
    )
    assert 'formal_charge' not in {issue.attribute for issue in report.issues}


def test_pdb_report_exposes_malformed_charge_conect_and_bioassembly_records():
    pdb_text = (
        'REMARK 350 BIOMOLECULE: 1\n'
        'REMARK 350 APPLY THE FOLLOWING TO CHAINS: A\n'
        'REMARK 350   BIOMT1   1  1.000000  0.000000  0.000000        0.00000\n'
        + _pdb_atom_line(
            1, 'CA', 'ALA', 'A', 1, (0.0, 0.0, 0.0), 'C', charge='X+'
        )
        + 'CONECT    1   99\n'
        + 'END\n'
    )

    restored, report = msm.convert(
        pdb_text,
        to_form='molsysmt.MolSys',
        get_missing_bonds=False,
        return_report=True,
    )

    assert restored.topology.n_bonds == 0
    assert restored.structures.bioassembly is None
    issues = {(issue.attribute, issue.kind) for issue in report.issues}
    assert ('formal_charge', 'adapter_limitation') in issues
    assert ('bonded_atoms', 'adapter_limitation') in issues
    assert ('bioassembly', 'adapter_limitation') in issues


def test_pdb_report_does_not_silently_interpret_repeated_conect_as_bond_order():
    pdb_text = (
        _pdb_atom_line(1, 'C1', 'LIG', 'A', 1, (0.0, 0.0, 0.0), 'C')
        + _pdb_atom_line(2, 'C2', 'LIG', 'A', 1, (1.0, 0.0, 0.0), 'C')
        + 'CONECT    1    2    2\n'
        + 'END\n'
    )

    restored, report = msm.convert(
        pdb_text,
        to_form='molsysmt.MolSys',
        get_missing_bonds=False,
        return_report=True,
    )

    assert restored.topology.n_bonds == 1
    assert any(
        issue.attribute == 'bond_order' and issue.kind == 'adapter_limitation'
        for issue in report.issues
    )
