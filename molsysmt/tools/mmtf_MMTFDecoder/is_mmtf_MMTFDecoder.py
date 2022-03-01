from molsysmt._private_tools.exceptions import WrongFormError

def is_mmtf_MMTFDecoder(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'mmtf.api.mmtf_reader.MMTFDecoder')

    return output

def _checking_form(item, check_form=True):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise WrongFormError('mmtf.MMTFDecoder')

    pass

