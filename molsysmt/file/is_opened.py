import os
from molsysmt._private.arg_digestion import arg_digest

@arg_digest()
def is_opened(filename):

    absolute_path = os.path.abspath(filename)

    from molsysmt.file import files_handled

    return absolute_path in files_handled

