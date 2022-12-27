from .file_handler import FileHandler
import os
from molsysmt._private.exceptions import FileAlreadyHandledError

def open(filename, mode='auto'):

    absolute_path = os.path.abspath(filename)

    from molsysmt.file import handler

    if absolute_path in handler:

        raise FileAlreadyHandledError

    handler[absolute_path]=FileHandler(absolute_path, mode)

    pass

