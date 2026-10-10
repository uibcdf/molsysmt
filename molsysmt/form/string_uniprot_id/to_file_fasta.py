from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:uniprot_id")
def to_file_fasta(item, atom_indices="all", output_filename=None, skip_digestion=False):
    """
    Converting from string:uniprot_id to file:fasta.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:fasta
        Resulting object in file:fasta form.


    Notes
    -----
    Without an output filename, the adapter generates a file and owns it until
    writing and closing succeed. Failure or interruption retires that generated
    file; successful output belongs to the caller. Explicit output paths are
    never removed on failure and may contain partial writes. Cleanup errors
    propagate. The high-level conversion dispatcher requires an explicit output
    filename for file targets.

    .. versionadded:: 1.0.0
    """

    import os
    import tempfile
    import urllib.request
    from pathlib import Path

    if item.startswith("uniprot_id:"):
        accession = item.split("uniprot_id:", 1)[1]
    else:
        accession = item

    url = f"https://www.uniprot.org/uniprot/{accession}.fasta"

    req = urllib.request.Request(url)
    req.add_header("User-Agent", "MolSysMT/1.0 (https://github.com/uibcdf/MolSysMT)")

    with urllib.request.urlopen(req) as response:
        fasta_content = response.read().decode("utf-8")

    generated_output = output_filename is None
    if generated_output:
        fd, output_filename = tempfile.mkstemp(suffix=".fasta")
        try:
            try:
                f = os.fdopen(fd, "w")
            except BaseException:
                os.close(fd)
                raise
            with f:
                f.write(fasta_content)
        except BaseException:
            Path(output_filename).unlink(missing_ok=True)
            raise
    else:
        with open(output_filename, "w") as f:
            f.write(fasta_content)

    return output_filename
