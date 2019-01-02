from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'ddb': form_name,
    'DDB': form_name
    }
