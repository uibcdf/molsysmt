from molsysmt._private_tools.exceptions import WrongFormError

def is_mmtf_MMTFDecoder(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'mmtf.api.mmtf_reader.MMTFDecoder')

    return output

def _checking_form(item, check=True):

    if check:
        if not is_molsysmt_MolSys(item):
            raise WrongFormError('molsysmt.MolSys')
    pass

