from pathlib import PosixPath

def is_form(item):

    output = False

    output = False

    if isinstance(item, PosixPath):
        item = item.absolute().__str__()

    if isinstance(item, str):
        if item.endswith('.psf'):
            output = True

    return output

