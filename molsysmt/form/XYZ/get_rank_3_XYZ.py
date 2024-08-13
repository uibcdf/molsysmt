from molsysmt import pyunitwizard as puw
from molsysmt._private.variables import make_coordinates_like
import numpy as np

def get_rank_3_XYZ(item):

    try:
        return make_coordinates_like(item, standardized=False)
    except:
        raise ValueError()

