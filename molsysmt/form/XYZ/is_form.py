from molsysmt import pyunitwizard as puw
import numpy as np
from pathlib import PurePath

def is_form(item):

    output = False

    # An XYZ item is an array of coordinates carrying a unit. A string never is: '3 nm' is
    # a valid quantity for PyUnitWizard, so `is_quantity` hands it to pint to parse, and
    # `get_form` asks every detector in turn -- which made detecting the form of a file
    # path pay for a failed unit parse. Rule it out before asking.
    if isinstance(item, (str, PurePath)):
        return output

    if puw.is_quantity(item):
        if  puw.are_compatible(item, puw.unit('nm')):

            shape = np.shape(item)

            if len(shape)==3 and shape[-1]==3:
                output = True
            elif len(shape)==2 and shape[-1]==3:
                output = True
            elif len(shape)==1 and shape[-1]==3:
                output = True

    return output

