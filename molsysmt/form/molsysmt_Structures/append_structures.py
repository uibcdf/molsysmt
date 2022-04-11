from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def append_structures(item, step=None, time=None, coordinates=None, box=None, check=True):

    if check:

        digest_item(item, 'molsysmt.Structures')
        step = digest_step(step)
        time = digest_time(time)
        coordinates = digest_coordinates(coordinates)
        box = digest_box(box)

    item.append_structures(step=step, time=time, coordinates=coordinates, box=box)

    pass

