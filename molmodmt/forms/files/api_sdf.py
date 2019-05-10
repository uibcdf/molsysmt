from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'sdf': form_name,
    'SDF': form_name
    }
