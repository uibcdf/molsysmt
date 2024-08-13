from ...exceptions import ArgumentError
import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.input_arguments import can_be_selection
from molsysmt._private.variables import make_coordinates_like

methods_where_bool = [
]

methods_where_none = [
    'molsysmt.thirds.nglview.add_arrows.add_arrows'
]

methods_where_xyz = [
    'molsysmt.thirds.nglview.add_arrows.add_arrows'
]

methods_where_can_be_selection = [
    'molsysmt.thirds.nglview.add_arrows.add_arrows'
]

def digest_end(end, caller=None):

    if caller in methods_where_bool:
        if isinstance(end, bool):
            return end

    if caller in methods_where_none:
        if end is None:
            return None

    if caller in methods_where_xyz:
        try:
            return make_coordinates_like(end)
        except:
            pass

    if caller in methods_where_can_be_selection:
        if can_be_selection(end):
            return end

    raise ArgumentError('end', value=end, caller=caller, message=None)

