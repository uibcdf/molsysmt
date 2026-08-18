from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_id')
def to_file_fasta(item, output_filename=None, skip_digestion=False):
    """
    Converting from string:pdb_id to file:fasta.


    Parameters
    ----------
    item : molecular system
        Argument item.
    output_filename : str or pathlib.Path, default=None
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

    url = 'https://www.rcsb.org/fasta/entry/'+item
    request = urllib.request.Request(url)
    
    with urllib.request.urlopen(request) as response:
        tmp_item = response.read().decode('utf-8')

    with open(output_filename, 'w') as fff:
        fff.write(tmp_item)

    return output_filename
