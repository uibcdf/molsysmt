from os.path import basename as _basename
from os import remove as _remove

form_name=_basename(__file__).split('.')[0][4:]+':id'

is_form = {
    'chembl:id': form_name,
    'ChEMBL:id': form_name
    }

def to_UniProt_id(form_id):
    pass
