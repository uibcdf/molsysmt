"""Inspecting submitted FASTA records before normalization or admission."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "form"])
@arg_digest()
def parse_records(fasta_text, *, source_label=None, skip_digestion=False):
    """Parsing FASTA text while retaining every source record and character.

    Parameters
    ----------
    fasta_text : str
        Decoded FASTA text. Only CR, LF and CRLF delimit lines. Record headers
        start with ``>`` in the first column; every other character is retained.
    source_label : str or None, default=None
        Opaque source label carried unchanged in the result. It does not verify
        identity or correspondence with a molecular system.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    dict
        JSON-compatible ``molsysmt.fasta_source@1`` document with ``schema``,
        ``source``, verbatim blank ``preamble`` and ordered ``records``. Each
        record contains ``record_index`` (zero-based occurrence, not identity),
        full ``header`` without ``>`` or its line terminator, ``sequence``
        formed by joining sequence lines without terminators, ``raw_record``
        including original terminators, and ``source_span=[start, stop]``.
        Spans are half-open decoded-character offsets into `fasta_text`, not
        byte offsets. Empty input gives no records; empty/repeated headers
        and sequences are retained independently. Every call returns fresh
        dictionaries and lists.

    Raises
    ------
    ArgumentError
        If fasta_text is not text or source_label is neither text nor None.
    FormatError
        If nonblank content precedes the first header, including a byte-order
        mark, comment or indented header. No unnamed record is discarded.

    Notes
    -----
    The preamble plus all raw records reconstructs the complete input exactly.
    Case, spaces, tabs, leading M, stops and modification symbols are unchanged.
    Comments after a header are sequence content, not silently discarded.
    No biological alphabet, protonation or peptide admissibility is inferred.
    This resident text reader does not create topology/coordinates or require
    Biopython. Existing normalized conversions remain separate operations.

    See Also
    --------
    molsysmt.form.file_fasta.read_records
        Reading strict UTF-8 files without newline translation.

    Examples
    --------
    >>> import molsysmt as msm
    >>> text = '>raw header\\n acD \\nA*\\n>empty\\n'
    >>> result = msm.form.file_fasta.parse_records(text, source_label='submitted')
    >>> [record['sequence'] for record in result['records']]
    [' acD A*', '']
    >>> result['preamble'] + ''.join(r['raw_record'] for r in result['records']) == text
    True

    .. admonition:: User guide

       See :ref:`Tutorial_Form_file_fasta` for source-preserving ingestion.

    .. versionadded:: 1.0.0
    """
    from ._source_records import parse_source_records

    return parse_source_records(fasta_text, source_label)
