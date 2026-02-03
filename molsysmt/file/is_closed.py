import os
from molsysmt._private.digestion import arg_digest

@arg_digest()
def is_closed(filename):

    absolute_path = os.path.abspath(filename)

    from molsysmt.file import files_handled

    return absolute_path not in files_handled

