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

def digest_top(top, caller=None):

    if caller in methods_where_bool:
        if isinstance(top, bool):
            return top

    if caller in methods_where_none:
        if top is None:
            return None

    if caller in methods_where_xyz:
        try:
            return make_coordinates_like(top)
        except:
            pass

    if caller in methods_where_can_be_selection:
        if can_be_selection(top):
            return top

    raise ArgumentError('top', value=top, caller=caller, message=None)

