from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:prmtop')
def copy(item, output_filename=None, skip_digestion=False):

    from shutil import copy as copy_file
    copy_file(item, output_filename)
    tmp_item = output_filename

    return tmp_item

