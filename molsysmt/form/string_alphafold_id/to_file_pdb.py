from molsysmt._private.digestion import digest

@digest(form='string:alphafold_id')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):

    import urllib.request
    from urllib.request import urlretrieve
    import json
    from ..file_pdb import extract

    uniprot_id = item.split('-')[-2]

    api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"

    request = urllib.request.Request(api_url, headers={"accept": "application/json"})

    with urllib.request.urlopen(request) as response:
        if response.status != 200:
            raise Exception(f"Error accessing the API: {response.status}")

        response_data = response.read()

    aux_json = json.loads(response_data)
    fullpdburl = aux_json[0]['pdbUrl']

    output = None

    if output_filename is None:
        output_filename = fullpdburl.split("/")[-1]

    urlretrieve(fullpdburl, output_filename)

    tmp_item = output_filename
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            output_filename=tmp_item, copy_if_all=False, skip_digestion=True)

    return tmp_item

