from molsysmt.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from shutil import copy as copy_file

@arg_digest(form='file:crd')
def copy(item, output_filename=None, progress_bar=False, skip_digestion=False):

    if output_filename is None:
        output_filename = item

    copy_file(item, output_filename)
    tmp_item = output_filename

    return tmp_item

