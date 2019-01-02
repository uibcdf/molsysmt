from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]


is_form = {
    'smi': form_name,
    'SMI': form_name
    }
