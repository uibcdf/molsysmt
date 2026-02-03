import os
from molsysmt._private.digestion import arg_digest

@arg_digest()
def get_mode(filename):

    from molsysmt.file import files_handled

    absolute_path = os.path.abspath(filename)

    if absolute_path in files_handled:
        return files_handled[absolute_path].mode
    else:
        return None

