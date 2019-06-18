from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'h5': form_name,
    'hdf5': form_name
    }

def to_mdtraj(item, selection='all', syntaxis='mdtraj'):
    return to_mdtraj_Trajectory(item)

def to_mdtraj_Trajectory(item, selection='all', syntaxis='mdtraj'):

    from mdtraj import load_hdf5 as _mdtraj_load
    tmp_form = _mdtraj_load(item)
    del(_mdtraj_load)
    return tmp_form


def to_molmodmt_MolMod(item, selection='all', frames=None, syntaxis='mdtraj'):

    from molmodmt.native.io_molmod import from_xtc as _from_h5
    return _from_h5(item, topology=topology, selection=selection, frames=frames, syntaxis=syntaxis)

