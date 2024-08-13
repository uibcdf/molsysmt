import numpy as np
from .variables import is_iterable_of_integers

def can_be_selection(input_argument):

    output = False

    if isinstance(input_argument, str):
        output = True
    elif is_iterable_of_integers(input_argument):
        output = True

    return output

