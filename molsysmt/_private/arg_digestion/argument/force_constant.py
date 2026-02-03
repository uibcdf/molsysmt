import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError
from molsysmt._private.variables import is_iterable

functions_with_boolean = (
        )

functions_with_list_as_output = (
    'add_harmonic_bond_force',
        )


def digest_force_constant(force_constant, caller=None):

    if caller is not None:
        if caller.endswith(functions_with_list_as_output):
            if puw.is_quantity(force_constant):
                if puw.check(force_constant, dimensionality={'[M]':1, '[T]':-2, '[mol]':-1}):
                    value, unit = puw.get_value_and_unit(force_constant)
                    if is_iterable(value):
                        return [puw.quantity(ii, unit, standardized=True) for item in value]
                    else:
                        return [puw.quantity(value, unit, standardized=True)]
            elif is_iterable(force_constant):
                for aux in force_constant:
                    output = []
                    if puw.check(aux, dimensionality={'[M]':1, '[T]':-2, '[mol]':-1}):
                        output.append(puw.standardize(aux))
                    else:
                        raise ArgumentError('force_constant', value=aux, caller=caller, message=None)
                return output

    if puw.is_quantity(force_constant):
        if puw.check(force_constant, dimensionality={'[M]':1, '[T]':-2, '[mol]':-1}):
            return puw.standardize(force_constant)

    raise ArgumentError('force_constant', value=force_constant, caller=caller, message=None)

