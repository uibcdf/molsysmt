import re
import requests

pattern= re.compile('[0-9][a-zA-Z_0-9]{3}')

def is_form(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'builtins.str')

    if output:
        if item.startswith('pdb_id:'):
            output = True
        else:

            output = False

            if type(item)==str:
                if pattern.match(item):
                    try:
                        request = requests.get('https://files.rcsb.org/download/{}.pdb'.format(item), stream=True)
                        if request.status_code == 200:
                            output = True
                    except:
                        output = False

    return output

