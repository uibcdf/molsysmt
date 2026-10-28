"""Reading source-preserving FASTA records without an optional sequence engine."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import FormatError


@signal(tags=["api", "form"])
@arg_digest(form="file:fasta")
def read_records(item, *, skip_digestion=False):
    """Reading a UTF-8 FASTA file while retaining original record text.

    Parameters
    ----------
    item : str or pathlib.Path
        Path in file:fasta form (``.fa`` or ``.fasta``). The file is read as
        strict UTF-8 with newline translation disabled and is never modified.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    dict
        ``molsysmt.fasta_source@1`` document described by `parse_records`,
        with ``source=str(item)``. Original newlines and decoded-character
        source spans are retained. The source path is a label, not identity
        authentication. No normalization or chemical admission is performed.

    Raises
    ------
    ArgumentError
        If item is not a supported FASTA path.
    FormatError
        If decoding fails or nonblank content precedes a header. A decoding
        failure retains its UnicodeDecodeError cause.
    OSError
        If the source cannot be opened or read, including a missing file.

    Notes
    -----
    This resident reader requires neither Biopython nor a molecular topology.
    Ordinary conversions to SeqRecord retain their existing normalized contract.
    File byte offsets are not inferred from decoded-character spans.

    See Also
    --------
    molsysmt.form.file_fasta.parse_records
        Inspecting the text and complete result schema without file I/O.

    Examples
    --------
    >>> import molsysmt as msm
    >>> import tempfile
    >>> from pathlib import Path
    >>> with tempfile.TemporaryDirectory() as folder:
    ...     path = Path(folder) / 'input.fasta'
    ...     _ = path.write_bytes(b'>a\\r\\n acD \\r\\n')
    ...     result = msm.form.file_fasta.read_records(path)
    >>> result['records'][0]['sequence']
    ' acD '

    .. admonition:: User guide

       See :ref:`Tutorial_Form_file_fasta` for inspecting submitted records.

    .. versionadded:: 1.0.0
    """
    from ._source_records import parse_source_records

    try:
        with open(item, encoding="utf-8", newline="") as stream:
            text = stream.read()
    except UnicodeDecodeError as error:
        raise FormatError(reason="FASTA source must be valid UTF-8.") from error
    return parse_source_records(text, str(item))
