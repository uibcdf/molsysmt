from numpy import ndarray
from argdigest.core.caller import caller_matches, caller_startswith

from molsysmt._private.smonitor import ArgumentError


def digest_atom_ff_type(atom_ff_type, caller=None):
    """Validating per-atom force-field type labels."""

    boolean_callers = ('get', 'compare', 'iterator')
    if any(caller_matches(caller, name) for name in boolean_callers):
        if isinstance(atom_ff_type, bool):
            return atom_ff_type
    elif caller_startswith(caller, 'molsysmt.form.') and caller.count('.to_') == 2:
        return atom_ff_type

    if atom_ff_type is None or isinstance(atom_ff_type, str):
        return atom_ff_type
    if isinstance(atom_ff_type, list):
        return atom_ff_type
    if isinstance(atom_ff_type, tuple):
        return list(atom_ff_type)
    if isinstance(atom_ff_type, ndarray):
        return atom_ff_type.tolist()

    raise ArgumentError('atom_ff_type', value=atom_ff_type, caller=caller, message=None)
