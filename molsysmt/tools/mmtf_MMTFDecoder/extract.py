from molsysmt.tools.mmtf_MMTFDecoder.is_mmtf_MMTFDecoder import is_mmtf_MMTFDecoder
from molsysmt._private_tools.exceptions import WrongFormError, WrongStepError
from molsysmt._private_tools.step import digest_step
from molsysmt._private_tools.time import digest_time
from molsysmt._private_tools.coordinates import digest_coordinates
from molsysmt._private_tools.box import digest_box

def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, check=True):

    if check:

        try:
            is_mmtf_MMTFDecoder(item)
        except:
            raise WrongFormError('mmtf.MMTFDecoder')

        try:
            coordinates = digest_coordinates(coordinates)
        except:
            raise WrongCoordinatesError()

        try:
            box = digest_box(box)
        except:
            raise WrongBoxError()


    if check:
        from molsysmt.tools.mmtf_MMTFDecoder.is_mmtf_MMTFDecoder import _checking_form
        _checking_form(item, check=check)

    if (atom_indices is 'all') and (structure_indices is 'all'):
        if copy_if_all:
            from copy import deepcopy
            tmp_item = deepcopy(item)
        else:
            tmp_item = item
    else:
        raise NotImplementedError()

    return tmp_item

