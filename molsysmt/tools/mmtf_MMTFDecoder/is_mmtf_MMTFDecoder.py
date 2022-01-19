from molsysmt._private_tools.exceptions import ItemWithWrongForm

def is_mmtf_MMTFDecoder(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'mmtf.MMTFDecoder')

    return output

def _checking_form(item, check_form=True):

    if check_form:
        if not is_mmtf_MMTFDecoder(item):
            raise ItemWithWrongForm('mmtf.MMTFDecoder')

    pass

