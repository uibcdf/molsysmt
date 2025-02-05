from molsysmt import pyunitwizard as puw
from .variables import is_iterable

def is_quantity_with_value_iterable(item):

    output = False

    if puw.is_quantity(item):
        value = puw.get_value(item)
        if is_iterable(value):
            output = True

    return output

def is_iterable_with_all_quantities(item):

    output = False

    if not puw.is_quantity(item): 
        if is_iterable(item):
            if all([puw.is_quantity(element) for element in item]):
                output = True

    return output
