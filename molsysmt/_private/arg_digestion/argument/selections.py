from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.variables import is_all

def digest_selections(selections, syntax="MolSysMT", caller=None):

    from .selection import digest_selection
    if isinstance(selections, (list, tuple)):
        return [digest_selection(ii, syntax=syntax, caller=caller) for ii in selections]
    elif is_all(selections):
        return selections

    raise ArgumentError('selections', value=selections, caller=caller)

