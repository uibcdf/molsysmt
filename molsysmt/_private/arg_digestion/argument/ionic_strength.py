import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError

def digest_ionic_strength(ionic_strength, caller=None):

    if puw.is_quantity(ionic_strength):
        if puw.check(ionic_strength, dimensionality={'[L]': -3, '[mol]': 1}):
            return puw.standardize(ionic_strength)


    raise ArgumentError('ionic_strength', value=ionic_strength, caller=caller, message=None)

