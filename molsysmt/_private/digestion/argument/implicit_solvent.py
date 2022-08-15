from molsysmt._private.exceptions import ArgumentError

def digest_implicit_solvent(implicit_solvent, caller=None):

    if isinstance(implicit_solvent, str):
        return implicit_solvent

    raise ArgumentError('implicit_solvent', value=implicit_solvent, caller=caller, message=None)

