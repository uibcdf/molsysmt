from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from shutil import copy as copy_file

@digest(form='file:crd')
def copy(item, output_filename=None, progress_bar=False):

    if output_filename is None:
        output_filename = item

    copy_file(item, output_filename)
    tmp_item = output_filename

    return tmp_item

