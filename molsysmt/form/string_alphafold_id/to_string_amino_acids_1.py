from molsysmt._private.digestion import digest

@digest(form='string:alphafold_id')
def to_string_amino_acids_1(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):

    from molsysmt._private.files_and_directories import temp_filename
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
    tmp_item = aux_json[0]['uniprotSequence']

    return tmp_item

