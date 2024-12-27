from molsysmt._private.digestion import digest

@digest(form='string:alphafold_id')
def to_mmcif_PdbxContainers_DataContainer(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from bcifreader import BinaryCifReader
    import urllib.request
    import json

    uniprot_id = item.split('-')[-2]

    api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"

    request = urllib.request.Request(api_url, headers={"accept": "application/json"})

    with urllib.request.urlopen(request) as response:
        if response.status != 200:
            raise Exception(f"Error accessing the API: {response.status}")

        response_data = response.read()

    aux_json = json.loads(response_data)
    fullbcifurl = aux_json[0]['bcifUrl']

    binary_cif_reader = BinaryCifReader()
    containers = binary_cif_reader.deserialize(fullbcifurl)

    if len(containers)>1:
        print('Warning! The file has more than a DataContainer')

    tmp_item = containers[0]

    return tmp_item


