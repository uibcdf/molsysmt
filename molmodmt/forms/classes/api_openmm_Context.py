from os.path import basename as _basename
from simtk.openmm import Context as _openmm_Context

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_Context : form_name,
    'openmm.Context' : form_name
}

