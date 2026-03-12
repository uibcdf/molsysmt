from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='string:alphafold_id')
def to_file_fasta(item, output_filename=None, skip_digestion=False):

    import urllib.request

    url = 'https://alphafold.ebi.ac.uk/entry/'+item
    request = urllib.request.Request(url)
    
    with urllib.request.urlopen(request) as response:
        tmp_item = response.read().decode('utf-8')

    # ... remaining logic to parse HTML if needed, but usually AlphaFold has a direct FASTA URL
    # This might need refinement depending on the actual AlphaFold API/HTML structure
    
    return output_filename
