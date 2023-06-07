from pathlib import PosixPath

def is_form(item):

    output = False

    if isinstance(item, PosixPath):
        item = item.absolute().__str__()

    if isinstance(item, str):
        if item.endswith('.h5') or item.endswith('.hdf5'):
            output = True

    return output

