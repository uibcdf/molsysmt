from molsysmt._private.download import download_with_retries
from molsysmt._private.files_and_directories import temp_filename


def download(pdb_id=None, output_filename=None, tempfile=False, wwPDB_Partner='RCSB PDB', skip_digestion=False, retries=5, timeout=30, backoff_base=2.0):
    """Downloading a remote bcif file from a wwPDB partner."""

    if pdb_id.startswith('pdb_id:'):
        pdb_id = pdb_id.split(':')[-1]
    elif pdb_id.startswith('pdb_'):
        pdb_id = pdb_id[-4:]

    if wwPDB_Partner != 'RCSB PDB':
        raise NotImplementedError("Only 'RCSB PDB' is supported at the moment.")

    if output_filename is None:
        if tempfile:
            output_filename = temp_filename(extension="bcif")
        else:
            output_filename = f"{pdb_id}.bcif"

    return download_with_retries(
        url="https://models.rcsb.org/{pdb_id}.bcif".format(pdb_id=pdb_id),
        output_filename=output_filename,
        resource=f"{pdb_id}.bcif",
        provider=wwPDB_Partner,
        caller="molsysmt.form.file_bcif.download",
        retries=retries,
        timeout=timeout,
        backoff_base=backoff_base,
    )
