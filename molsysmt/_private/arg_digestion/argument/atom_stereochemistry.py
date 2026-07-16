import pandas as pd

from molsysmt._private.smonitor import ArgumentError

_VALUES = {'R', 'S', 'r', 's', 'unspecified', 'unknown'}


def digest_atom_stereochemistry(atom_stereochemistry, caller=None):
    if isinstance(atom_stereochemistry, bool):
        return atom_stereochemistry
    if isinstance(atom_stereochemistry, str) and atom_stereochemistry in _VALUES:
        return atom_stereochemistry
    try:
        values = list(atom_stereochemistry)
    except TypeError as error:
        raise ArgumentError(
            'atom_stereochemistry', value=atom_stereochemistry, caller=caller, message=None
        ) from error
    if all(value is None or value is pd.NA or value in _VALUES for value in values):
        return values
    raise ArgumentError('atom_stereochemistry', value=atom_stereochemistry, caller=caller, message=None)
