from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:uniprot_id')
def to_file_fasta(item, atom_indices='all', output_filename=None, skip_digestion=False):
    """
    Converting from string:uniprot_id to file.fasta.

    Parameters
    ----------
    item : string:uniprot_id
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file.fasta
        Converted molecular system representation.
    """

    import urllib.request
    import tempfile
    import os

    if item.startswith("uniprot_id:"):
        accession = item.split("uniprot_id:", 1)[1]
    else:
        accession = item

    url = f"https://www.uniprot.org/uniprot/{accession}.fasta"

    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'MolSysMT/1.0 (https://github.com/uibcdf/MolSysMT)')

    with urllib.request.urlopen(req) as response:
        fasta_content = response.read().decode('utf-8')

    if output_filename is None:
        fd, output_filename = tempfile.mkstemp(suffix='.fasta')
        os.close(fd)

    with open(output_filename, 'w') as f:
        f.write(fasta_content)

    return output_filename
