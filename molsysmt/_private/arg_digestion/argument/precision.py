from molsysmt._private.smonitor import ArgumentError


def digest_precision(precision, caller=None):

    if precision is None:
        return None

    if isinstance(precision, str):
        p_lower = precision.lower()
        if p_lower in ['double', 'float64']:
            return 'double'
        if p_lower in ['single', 'float32']:
            return 'single'

    raise ArgumentError('precision', value=precision, caller=caller, message=None)
