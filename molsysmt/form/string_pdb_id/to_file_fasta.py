from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_id')
def to_file_fasta(item, output_filename=None, skip_digestion=False):

    import urllib.request

    url = 'https://www.rcsb.org/fasta/entry/'+item
    request = urllib.request.Request(url)
    
    with urllib.request.urlopen(request) as response:
        tmp_item = response.read().decode('utf-8')

    with open(output_filename, 'w') as fff:
        fff.write(tmp_item)

    return output_filename
