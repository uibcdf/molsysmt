from os.path import basename as _basename
from simtk.openmm import System as _openmm_System

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_System : form_name,
    'openmm.System' : form_name,
}

from .get.api_get_openmm_System import getting
#from .set.api_set_openmm_System import setting

def get_total_n_atoms(item):
    return item.getNumParticles()

