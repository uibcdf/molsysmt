"""Tests for MolSys to BioPython SeqRecord conversion."""

import molsysmt as msm


def test_conversion_returns_sequence_record(met_enkephalin_h5msm_molsys):
    """Converting a complete peptide to a SeqRecord."""
    from Bio.SeqRecord import SeqRecord

    record = msm.convert(met_enkephalin_h5msm_molsys, to_form='biopython.SeqRecord')

    assert isinstance(record, SeqRecord)
    assert str(record.seq) == 'YGGFM'


def test_conversion_honors_atom_selection(met_enkephalin_h5msm_molsys):
    """Converting atoms from selected groups to the corresponding sequence."""
    atom_indices = msm.select(
        met_enkephalin_h5msm_molsys,
        selection='group_index in [1, 3]',
    )

    record = msm.convert(
        met_enkephalin_h5msm_molsys,
        to_form='biopython.SeqRecord',
        selection=atom_indices,
    )

    assert str(record.seq) == 'GF'


def test_conversion_omits_non_peptide_groups(t4_h5msm_molsys):
    """Ignoring ligands and solvent when converting a protein to sequence."""
    record = msm.convert(t4_h5msm_molsys, to_form='biopython.SeqRecord')
    n_amino_acids = msm.get(
        t4_h5msm_molsys,
        element='system',
        n_amino_acids=True,
    )

    assert len(record.seq) == n_amino_acids
