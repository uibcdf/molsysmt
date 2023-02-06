from .file_handler import FileHandler
import os
from molsysmt._private.exceptions import FileAlreadyHandledError
from molsysmt._private.digestion import digest

@digest()
def open(filename, mode='auto'):

    absolute_path = os.path.abspath(filename)

    from molsysmt.file import files_handled

    if absolute_path in files_handled:

        raise FileAlreadyHandledError

    files_handled[absolute_path]=FileHandler(absolute_path, mode)

    pass

