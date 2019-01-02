from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0][4:].replace('_',':')

is_form = {
    'xxx:id': form_name,
    'XXX:id': form_name
    }

