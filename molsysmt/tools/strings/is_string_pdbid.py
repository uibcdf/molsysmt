
def is_string_pdbid(string):

    output = False

    if len(string)==4:
        try:
            import requests
            request = requests.get('https://files.rcsb.org/download/{}.pdb'.format(string))
            if request.status_code == 200:
                output = True
        except:
            output = False

    return output

