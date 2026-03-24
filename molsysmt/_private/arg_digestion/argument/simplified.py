from molsysmt._private.smonitor import ArgumentError

def digest_simplified(simplified, caller=None):

    if isinstance(simplified, bool):
        return simplified

    raise ArgumentError('simplified', value=simplified, caller=caller, message=None)
