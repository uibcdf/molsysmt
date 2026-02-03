import os
from molsysmt._private.arg_digestion import arg_digest

@arg_digest()
def close(filename):

    absolute_path = os.path.abspath(filename)

    from molsysmt.file import files_handled

    file_handler = files_handled.pop(absolute_path)
    file_handler.close()

    del file_handler

    pass

