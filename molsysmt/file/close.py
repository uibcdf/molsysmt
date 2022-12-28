import os
from molsysmt._private.digestion import digest

@digest()
def close(filename):

    absolute_path = os.path.abspath(filename)

    from molsysmt.file import files_handled

    file_handler = files_handled.pop(absolute_path)
    file_handler.close()

    del file_handler

    pass

