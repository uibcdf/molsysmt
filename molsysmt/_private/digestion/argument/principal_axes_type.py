import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError

functions = [
        'molsysmt.structure.get_principal_axes.get_principal_axes',
        'molsysmt.structure.align_principal_axes.align_principal_axes'
        ]

options = [
        'inertia',
        'geometric'
        ]

def digest_principal_axes_type(principal_axes_type, caller=None):

    if caller in functions:

        if isinstance(principal_axes_type, str):
            if principal_axes_type in options:
                return principal_axes_type

    raise ArgumentError('principal_axes_type', value=principal_axes_type, caller=caller, message=None)

