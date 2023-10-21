from pathlib import PosixPath
import h5py

def is_form(item):

    output = False

    if isinstance(item, PosixPath):
        item = item.absolute().__str__()

    if isinstance(item, str):
        if item.endswith('.msmh5'):

            with h5py.File(item, "r") as file:
                if 'type' in file.attrs:
                    output = (file.attrs['type']=='msmh5')

    return output

