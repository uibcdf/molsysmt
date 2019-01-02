from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'h5': form_name,
    'hdf5': form_name
    }

def to_mdtraj(item):
    return to_mdtraj_Trajectory(item)

def to_mdtraj_Trajectory(item):

    from mdtraj import load_hdf5 as _mdtraj_load
    tmp_form = _mdtraj_load(item)
    del(_mdtraj_load)
    return tmp_form

    pass

def to_native_Native(item):

    from moldynmt.native import Native as _Native
    tmp_form = to_mdtraj(item)
    return _Native(tmp_form)

    pass
