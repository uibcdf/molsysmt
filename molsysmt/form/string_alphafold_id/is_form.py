import urllib.request
import json

def is_form(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'builtins.str')

    if output:
        if item.startswith('alphafold_id:'):
            output = True
        else:
            output = False
            if type(item)==str:
                if item.startswith('AF-'):
                    try:
                        uniprot_id = item.split('-')[-2]
                        api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
                        request = urllib.request.Request(api_url, headers={"accept": "application/json"})
                        with urllib.request.urlopen(request) as response:
                            if response.status != 200:
                                raise Exception(f"Error accessing the API: {response.status}")
                            response_data = response.read()
                        aux_json = json.loads(response_data)
                        entryId = aux_json[0]['entryId']
                        if item==entryId:
                            output = True
                    except:
                        output = False

    return output

