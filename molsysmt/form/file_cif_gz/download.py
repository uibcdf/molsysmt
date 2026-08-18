from molsysmt._private.download import download_with_retries
from molsysmt._private.files_and_directories import temp_filename


def download(pdb_id=None, output_filename=None, tempfile=False, wwPDB_Partner='RCSB PDB', skip_digestion=False, retries=5, timeout=30, backoff_base=2.0):
    """
    Performing download on form file:cif.gz.


    Parameters
    ----------
    pdb_id : object, default=None
        Argument pdb_id.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    tempfile : object, default=False
        Argument tempfile.
    wwPDB_Partner : object, default='RCSB PDB'
        Argument wwPDB_Partner.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    retries : object, default=5
        Argument retries.
    timeout : object, default=30
        Argument timeout.
    backoff_base : object, default=2.0
        Argument backoff_base.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """

    if pdb_id.startswith('pdb_id:'):
        pdb_id = pdb_id.split(':')[-1]
    elif pdb_id.startswith('pdb_'):
        pdb_id = pdb_id[-4:]

    if wwPDB_Partner != 'RCSB PDB':
        raise NotImplementedError("Only 'RCSB PDB' is supported at the moment.")

    if output_filename is None:
        if tempfile:
            output_filename = temp_filename(extension="cif.gz")
        else:
            output_filename = f"{pdb_id}.cif.gz"

    return download_with_retries(
        url="https://files.rcsb.org/download/{pdb_id}.cif.gz".format(pdb_id=pdb_id),
        output_filename=output_filename,
        resource=f"{pdb_id}.cif.gz",
        provider=wwPDB_Partner,
        caller="molsysmt.form.file_cif_gz.download",
        retries=retries,
        timeout=timeout,
        backoff_base=backoff_base,
    )
