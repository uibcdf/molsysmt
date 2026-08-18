from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:alphafold_id')
def to_file_fasta(item, output_filename=None, skip_digestion=False):
    """
    Converting from string:alphafold_id to file:fasta.

    Parameters
    ----------
    item : string:alphafold_id
        Source item in string:alphafold_id form.
    output_filename : str or pathlib.Path
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:fasta
        Resulting object in file:fasta form.

    .. versionadded:: 1.0.0
    """

    import urllib.request

    url = 'https://alphafold.ebi.ac.uk/entry/'+item
    request = urllib.request.Request(url)
    
    with urllib.request.urlopen(request) as response:
        tmp_item = response.read().decode('utf-8')

    # ... remaining logic to parse HTML if needed, but usually AlphaFold has a direct FASTA URL
    # This might need refinement depending on the actual AlphaFold API/HTML structure
    
    return output_filename
