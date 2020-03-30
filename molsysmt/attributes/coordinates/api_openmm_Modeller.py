from os.path import basename as _basename
from simtk.openmm.app.modeller import Modeller as _openmm_Modeller

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_Modeller : form_name,
    'openmm.Modeller' : form_name
}

def to_openmm(item):
    return item

def to_mdtraj_Trajectory(item):

    # mdtraj uses nanometers: see http://mdtraj.org/development/api/generated/mdtraj.Trajectory.html

    from simtk.unit import nanometers as _nanometers
    from numpy import array as _nparray

    tmp_attribute = item.value_in_units(_nanometers)
    tmp_attribute = _nparray(tmp_attribute)

    return tmp_item

