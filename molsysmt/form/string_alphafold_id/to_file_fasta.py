from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:alphafold_id")
def to_file_fasta(item, output_filename=None, skip_digestion=False):
    """
    Rejecting the unavailable direct AlphaFold FASTA export.

    This registered compatibility route has no implemented sequence writer.
    It refuses before network or filesystem access. A model's represented
    sequence must not be silently replaced with the full UniProt sequence.

    Parameters
    ----------
    item : molecular system
        AlphaFold model identifier in ``string:alphafold_id`` form.
    output_filename : str or pathlib.Path, default=None
        Requested output path. It is never created or changed by this route.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Raises
    ------
    NotImplementedConversionError
        Always; a model-aware FASTA writer is not implemented.

    Examples
    --------
    >>> from molsysmt._private.smonitor import NotImplementedConversionError
    >>> from molsysmt.form.string_alphafold_id.to_file_fasta import to_file_fasta
    >>> try:
    ...     to_file_fasta('AF-P05067-F1')
    ... except NotImplementedConversionError:
    ...     print('Model-aware FASTA export is unavailable')
    Model-aware FASTA export is unavailable

    .. versionadded:: 1.0.0
    """

    from molsysmt._private.smonitor import NotImplementedConversionError

    raise NotImplementedConversionError(
        "string:alphafold_id",
        "file:fasta",
        caller="molsysmt.form.string_alphafold_id.to_file_fasta",
        message="Direct AlphaFold FASTA export is unavailable; no file was written.",
    )
