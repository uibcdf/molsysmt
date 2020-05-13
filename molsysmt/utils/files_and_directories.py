import tempfile

def tmp_file(dir=None, extension=None):

    if not extension.startswith("."):
        extension="."+extension

    return tempfile.NamedTemporaryFile(suffix=extension, dir=dir, delete=False)


def tmp_filename(dir=None, extension=None):

    if not extension.startswith("."):
        extension="."+extension

    file=tempfile.NamedTemporaryFile(suffix=extension, dir=dir, delete=True)
    filename = file.name
    file.close()
    return filename


def tmp_directory():

    return tempfile.mkdtemp()

