from os.path import basename as _basename
from mdtraj.formats.xtc import XTCTrajectoryFile as _mdtraj_XTCTrajectoryFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_XTCTrajectoryFile: form_name,
    'mdtraj.XTCTrajectoryFile': form_name
    }


