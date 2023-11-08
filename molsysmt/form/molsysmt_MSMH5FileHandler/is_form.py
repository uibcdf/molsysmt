
def is_form(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'molsysmt.native.h5msm_file_handler.H5MSMFileHandler')

    return output

