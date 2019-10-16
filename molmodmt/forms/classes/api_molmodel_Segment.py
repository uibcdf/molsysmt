from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodel import Segment as _molmodel_Segment

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molmodel_Segment : form_name,
    'molmodel.Segment' : form_name
}

###### Get

## system

def get_form_from_system(item, indices=None, frame_indices=None):

    from molmodmt import _get_form
    return _get_form(item)

