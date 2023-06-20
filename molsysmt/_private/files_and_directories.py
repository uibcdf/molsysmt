import tempfile
from pathlib import PosixPath


def temp_filename(dir=None, extension=None):

    if not extension.startswith("."):
        extension = "."+extension

    file = tempfile.NamedTemporaryFile(suffix=extension, dir=dir, delete=True)
    filename = file.name
    file.close()
    return filename


def temp_directory():

    return tempfile.mkdtemp()

def str_filename(filename):

    if isinstance(filename, PosixPath):
        return str(filename)
    else:
        return filename
