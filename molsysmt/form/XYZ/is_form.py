from molsysmt import pyunitwizard as puw
import numpy as np

def is_form(item):

    output = False

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

