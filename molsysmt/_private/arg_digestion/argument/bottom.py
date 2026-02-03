from ...exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.input_arguments import can_be_selection
from molsysmt._private.variables import make_coordinates_like

methods_where_bool = [
]

methods_where_none = [
    'molsysmt.thirds.nglview.add_cylinders.add_cylinders'
]

methods_where_xyz = [
    'molsysmt.thirds.nglview.add_cylinders.add_cylinders'
]

methods_where_can_be_selection = [
    'molsysmt.thirds.nglview.add_cylinders.add_cylinders'
]

def digest_bottom(bottom, caller=None):

    if caller in methods_where_bool:
        if isinstance(bottom, bool):
            return bottom

    if caller in methods_where_none:
        if bottom is None:
            return None

    if caller in methods_where_xyz:
        try:
            return make_coordinates_like(bottom)
        except:
            pass

    if caller in methods_where_can_be_selection:
        if can_be_selection(bottom):
            return bottom

    raise ArgumentError('bottom', value=bottom, caller=caller, message=None)

