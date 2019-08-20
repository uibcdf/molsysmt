from os.path import basename as _basename
from mdtraj.formats.xtc import HDF5TrajectoryFile as _mdtraj_HDF5TrajectoryFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_HDF5TrajectoryFile: form_name,
    'mdtraj.HDF5TrajectoryFile': form_name
    }


