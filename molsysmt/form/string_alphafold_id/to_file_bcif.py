from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:alphafold_id")
def to_file_bcif(
    item,
    atom_indices="all",
    structure_indices="all",
    output_filename=None,
    skip_digestion=False,
):
    """
    Converting from string:alphafold_id to file:bcif.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:bcif
        Resulting object in file:bcif form.


    Notes
    -----
    Download and extraction use owned staging beside the destination. Failure
    before publication preserves an existing destination and retires staging.
    The parent directory must be writable. Successful output belongs to the
    caller. Cleanup errors propagate, including after publication; publication
    is not rolled back if retiring the empty staging directory fails.

    .. versionadded:: 1.0.0
    """

    import json
    import os
    import urllib.request
    from tempfile import TemporaryDirectory
    from urllib.request import urlretrieve

    from ..file_bcif.extract import extract

    uniprot_id = item.split("-")[-2]

    api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"

    request = urllib.request.Request(api_url, headers={"accept": "application/json"})

    with urllib.request.urlopen(request) as response:
        if response.status != 200:
            raise Exception(f"Error accessing the API: {response.status}")

        response_data = response.read()

    aux_json = json.loads(response_data)
    fullbcifurl = aux_json[0]["bcifUrl"]

    if output_filename is None:
        output_filename = fullbcifurl.split("/")[-1]

    destination_directory = os.path.dirname(os.path.abspath(output_filename))
    with TemporaryDirectory(
        prefix=".molsysmt-convert-", dir=destination_directory
    ) as scratch:
        staged_filename = os.path.join(scratch, "download.bcif")
        urlretrieve(fullbcifurl, staged_filename)
        tmp_item = extract(
            staged_filename,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            output_filename=staged_filename,
            copy_if_all=False,
            skip_digestion=True,
        )
        os.replace(tmp_item, output_filename)

    return output_filename
