from molsysmt._private.smonitor import ArgumentError

_VALID_HEAVY_MODES = {'auto', 'force', 'off'}

def digest_heavy_mode(heavy_mode, caller=None):

    if isinstance(heavy_mode, str) and heavy_mode in _VALID_HEAVY_MODES:
        return heavy_mode

    raise ArgumentError('heavy_mode', value=heavy_mode, caller=caller, message=None)
