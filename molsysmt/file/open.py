from .file_handler import FileHandler
import os
from molsysmt.exceptions import FileAlreadyHandledError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest()
def open(filename, mode='auto'):

    absolute_path = os.path.abspath(filename)

    from molsysmt.file import files_handled

    if absolute_path in files_handled:

        raise FileAlreadyHandledError(absolute_path)

    files_handled[absolute_path]=FileHandler(absolute_path, mode)

    pass
