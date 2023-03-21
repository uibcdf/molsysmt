from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='file:xtc')
def copy(item, output_filename=None):

    if output_filename is None:
        output_filename = item

    from shutil import copy as copy_file
    copy_file(item, output_filename)
    tmp_item = output_filename

    return tmp_item
