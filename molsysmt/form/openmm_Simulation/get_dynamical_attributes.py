"""Getting dynamical attributes from an OpenMM Simulation."""

import types

from molsysmt import pyunitwizard as puw
from molsysmt._private.arg_digestion import arg_digest


form = 'openmm.Simulation'


@arg_digest(form=form)
def get_integrator_from_system(item, skip_digestion=False):
    class_name = item.integrator.__class__.__name__
    if class_name.startswith('Langevin'):
        return 'Langevin'
    return None


@arg_digest(form=form)
def get_friction_from_system(item, skip_digestion=False):
    getter = getattr(item.integrator, 'getFriction', None)
    if getter is None:
        return None
    return puw.quantity(puw.get_value(getter()), '1/ps')


__all__ = [
    name
    for name, obj in globals().items()
    if isinstance(obj, types.FunctionType) and name.startswith('get_')
]
