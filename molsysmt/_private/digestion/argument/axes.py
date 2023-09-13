import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError


def digest_axes(axes, caller=None):

    if caller=='molsysmt.structure.align_principal_axes.align_principal_axes':

        if isinstance(axes, (list, tuple)):
            axes = np.array(axes, dtype=np.float64)

        if isinstance(axes, np.ndarray):
            if (len(axes.shape)==2) and (axes.shape[0]==3) and (axes.shape[1]==3):
                axes = axes.astype(np.float64)
                return axes

    raise ArgumentError('axes', value=axes, caller=caller, message=None)

