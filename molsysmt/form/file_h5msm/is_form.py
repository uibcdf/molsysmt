from pathlib import PosixPath
import h5py
import os

def is_form(item):
    """
    Checking whether an item is an instance of form file:h5msm.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form file:h5msm, False otherwise.
    """

    output = False

    if isinstance(item, PosixPath):
        item = item.absolute().__str__()

    if isinstance(item, str):
        if item.endswith('.h5msm'):

            if os.path.isfile(item):

                with h5py.File(item, "r") as file:
                    if 'type' in file.attrs:
                        output = (file.attrs['type']=='h5msm')

            else:

                output = True

    return output


