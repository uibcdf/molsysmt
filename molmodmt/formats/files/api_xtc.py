from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'xtc': form_name,
    'XTC': form_name
    }

def to_mdtraj_Trajectory(item):

    from mdtraj import load as _mdtraj_load
    tmp_form = _mdtraj_load(item)
    del(_mdtraj_load)
    return tmp_form

    pass

def to_native_Native(item):

    pass
