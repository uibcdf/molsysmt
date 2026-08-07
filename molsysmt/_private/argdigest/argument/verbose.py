from molsysmt._private.smonitor import ArgumentError

def digest_verbose(verbose, caller=None):

    if isinstance(verbose, bool):
        return verbose

    raise ArgumentError('verbose', value=verbose, caller=caller, message=None)

