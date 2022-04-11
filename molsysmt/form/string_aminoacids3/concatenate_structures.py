from .is_string_aminoacids3 import is_string_aminoacids3
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def concatenate_structures(item, step=None, time=None, coordinates=None, box=None, check=True):

    if check:

        digest_item(item, 'string:aminoacids3')
        step = digest_step(step)
        time = digest_time(time)
        coordinates = digest_coordinates(coordinates)
        box = digest_box(box)

    raise NotImplementedMethodError()

