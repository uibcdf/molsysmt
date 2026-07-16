"""Tests for one-letter amino-acid string to SeqRecord conversion."""

import molsysmt as msm


def test_conversion_returns_requested_subsequence():
    """Converting selected sequence positions to a SeqRecord."""
    from Bio.SeqRecord import SeqRecord

    record = msm.convert(
        'YGGFM',
        to_form='biopython.SeqRecord',
        selection=[0, 2, 4],
    )

    assert isinstance(record, SeqRecord)
    assert str(record.seq) == 'YGM'
