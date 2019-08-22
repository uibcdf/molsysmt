from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt.native.topology import Topology as _molmodmt_Topology

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molmodmt_Topology : form_name,
    'molmodmt.Topology': form_name
}



