import numpy as np
from molsysmt import pyunitwizard as puw
from ...exceptions import ArgumentError
from molsysmt._private.variables import is_iterable

functions_with_boolean = (
        )

functions_with_list_as_output = (
    'add_harmonic_bond_force',
        )

def digest_bond_length(bond_length, caller=None):

    if caller is not None:
        if caller.endswith(functions_with_list_as_output):
            if puw.is_quantity(bond_length):
                if puw.check(bond_length, dimensionality={'[L]':1}):
                    value, unit = puw.get_value_and_unit(bond_length)
                    if is_iterable(value):
                        return [puw.quantity(ii, unit, standardized=True) for item in value]
                    else:
                        return [puw.quantity(value, unit, standardized=True)]
            elif is_iterable(bond_length):
                for aux in bond_length:
                    output = []
                    if puw.check(bond_length, dimensionality={'[L]':1}):
                        output.append(puw.standardize(aux))
                    else:
                        raise ArgumentError('bond_length', value=aux, caller=caller, message=None)
                return output

    if puw.is_quantity(bond_length):
        if puw.check(bond_length, dimensionality={'[L]':1}):
            return puw.standardize(bond_length)

    raise ArgumentError('bond_length', value=bond_length, caller=caller, message=None)

