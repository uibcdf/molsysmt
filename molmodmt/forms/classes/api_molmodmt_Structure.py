from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt.native.structure import Structure as _molmodmt_Structure

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molmodmt_Structure : form_name,
    'molmodmt.Structure' : form_name
}


def duplicate(item):

    tmp_item = _molmodmt_Structure()

    return tmp_item

###### Get

## system

def get_form_from_system(item, indices=None, frame_indices=None):

    from molmodmt import get_form
    return get_form(item)

