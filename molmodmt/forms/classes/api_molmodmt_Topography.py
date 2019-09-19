from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt.native.topography import Topography as _molmodmt_Topography

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molmodmt_Topography : form_name,
    'molmodmt.Topography': form_name
}


def duplicate(item):

    tmp_item = _molmodmt_Topography()

    return item

